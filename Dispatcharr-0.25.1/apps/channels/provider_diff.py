"""
apps/channels/provider_diff.py
──────────────────────────────────────────────────────────────────────────────
Provider Migration Assistant – core matching logic.

Compares streams from a *source* M3U account (the one currently mapped in
channels / VOD / series) against a *target* M3U account and produces a diff:

  matched   – high-confidence pairs (exact or tvg_id match)
  similar   – fuzzy-matched pairs that need user confirmation
  missing   – source items not found in the target
  new_only  – target items not yet in any channel / relation

Transfer logic (apply_stream_mappings / apply_vod_mappings) updates the DB
in a single atomic transaction only after the user confirms.
"""

from __future__ import annotations

import re
import difflib
import logging
from dataclasses import dataclass, field
from typing import Optional

from django.db import transaction

logger = logging.getLogger(__name__)

# ── Tunable thresholds ────────────────────────────────────────────────────────
EXACT_CONFIDENCE   = 1.00
TVG_ID_CONFIDENCE  = 0.85
FUZZY_THRESHOLD    = 0.72   # minimum SequenceMatcher ratio to count as "similar"

# Suffixes/tokens stripped before name comparison (order matters – longer first)
_STRIP_TOKENS = re.compile(
    r"\b(UHD|FHD|HEVC|H\.?265|H\.?264|AVC|4K|HD|SD|DE|AT|CH|UK|US|FR|IT|ES|NL|BE|PL|TR|AR|MULTI)\b",
    re.IGNORECASE,
)
_NON_ALNUM = re.compile(r"[^a-z0-9]")


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(name: str) -> str:
    """Lowercase, strip quality/country tokens, keep only alphanumeric chars."""
    name = name.lower().strip()
    name = _STRIP_TOKENS.sub("", name)
    name = _NON_ALNUM.sub("", name)
    return name


def fuzzy_ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class StreamInfo:
    id: int
    name: str
    tvg_id: str
    group: str
    url: str
    # set to True when this stream is referenced by at least one Channel
    in_playlist: bool = False


@dataclass
class VodInfo:
    id: int          # Movie / Series PK
    relation_id: int # M3UMovieRelation / M3USeriesRelation PK
    name: str
    year: Optional[int]
    kind: str        # "movie" | "series"
    in_playlist: bool = False  # always True for source; target has False


@dataclass
class MatchPair:
    source: StreamInfo | VodInfo
    target: StreamInfo | VodInfo
    confidence: float


@dataclass
class ProviderDiffResult:
    matched: list[MatchPair]       = field(default_factory=list)
    similar: list[MatchPair]       = field(default_factory=list)
    missing: list[StreamInfo | VodInfo] = field(default_factory=list)
    new_only: list[StreamInfo | VodInfo] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "matched_count": len(self.matched),
            "similar_count": len(self.similar),
            "missing_count": len(self.missing),
            "new_only_count": len(self.new_only),
        }


# ── Live-stream diff ──────────────────────────────────────────────────────────

def _load_streams(account_id: int) -> list[StreamInfo]:
    from apps.channels.models import Stream
    qs = (
        Stream.objects
        .filter(m3u_account_id=account_id, is_stale=False)
        .values("id", "name", "tvg_id", "url")
        .select_related()  # no-op on .values() but kept for clarity
    )
    # We need channel_group name too
    from apps.channels.models import Stream as StreamModel
    qs2 = (
        StreamModel.objects
        .filter(m3u_account_id=account_id, is_stale=False)
        .select_related("channel_group")
    )
    return [
        StreamInfo(
            id=s.id,
            name=s.name or "",
            tvg_id=s.tvg_id or "",
            group=s.channel_group.name if s.channel_group else "",
            url=s.url or "",
        )
        for s in qs2
    ]


def _get_playlist_stream_ids(account_id: int) -> set[int]:
    """Return IDs of streams (from this account) used in at least one Channel."""
    from apps.channels.models import ChannelStream, Stream
    return set(
        ChannelStream.objects
        .filter(stream__m3u_account_id=account_id)
        .values_list("stream_id", flat=True)
    )


def diff_live_streams(source_account_id: int, target_account_id: int) -> ProviderDiffResult:
    """Compare live streams between two M3U accounts."""
    source_streams = _load_streams(source_account_id)
    target_streams = _load_streams(target_account_id)
    playlist_ids   = _get_playlist_stream_ids(source_account_id)

    for s in source_streams:
        s.in_playlist = s.id in playlist_ids

    # Index target by normalized name and tvg_id for fast lookup
    target_by_norm  = {}
    target_by_tvgid = {}
    for t in target_streams:
        n = normalize(t.name)
        if n and n not in target_by_norm:
            target_by_norm[n] = t
        if t.tvg_id and t.tvg_id not in target_by_tvgid:
            target_by_tvgid[t.tvg_id] = t

    result    = ProviderDiffResult()
    matched_target_ids: set[int] = set()

    for src in source_streams:
        src_norm = normalize(src.name)

        # 1) Exact name match
        if src_norm and src_norm in target_by_norm:
            tgt = target_by_norm[src_norm]
            result.matched.append(MatchPair(src, tgt, EXACT_CONFIDENCE))
            matched_target_ids.add(tgt.id)
            continue

        # 2) tvg_id match
        if src.tvg_id and src.tvg_id in target_by_tvgid:
            tgt = target_by_tvgid[src.tvg_id]
            result.matched.append(MatchPair(src, tgt, TVG_ID_CONFIDENCE))
            matched_target_ids.add(tgt.id)
            continue

        # 3) Fuzzy match against all unmatched targets
        best_ratio = 0.0
        best_tgt   = None
        for tgt in target_streams:
            if tgt.id in matched_target_ids:
                continue
            ratio = fuzzy_ratio(src_norm, normalize(tgt.name))
            if ratio > best_ratio:
                best_ratio = ratio
                best_tgt   = tgt

        if best_tgt and best_ratio >= FUZZY_THRESHOLD:
            result.similar.append(MatchPair(src, best_tgt, round(best_ratio, 3)))
            matched_target_ids.add(best_tgt.id)
        else:
            result.missing.append(src)

    # Anything in target not matched → new_only
    for tgt in target_streams:
        if tgt.id not in matched_target_ids:
            result.new_only.append(tgt)

    return result


# ── VOD (movie) diff ──────────────────────────────────────────────────────────

def _load_movies(account_id: int) -> list[VodInfo]:
    from apps.vod.models import M3UMovieRelation
    qs = (
        M3UMovieRelation.objects
        .filter(m3u_account_id=account_id)
        .select_related("movie")
    )
    return [
        VodInfo(
            id=rel.movie_id,
            relation_id=rel.id,
            name=rel.movie.name or "",
            year=getattr(rel.movie, "year", None),
            kind="movie",
            in_playlist=True,
        )
        for rel in qs
    ]


def diff_movies(source_account_id: int, target_account_id: int) -> ProviderDiffResult:
    source_vod = _load_movies(source_account_id)
    target_vod = _load_movies(target_account_id)
    return _generic_vod_diff(source_vod, target_vod)


# ── Series diff ───────────────────────────────────────────────────────────────

def _load_series(account_id: int) -> list[VodInfo]:
    from apps.vod.models import M3USeriesRelation
    qs = (
        M3USeriesRelation.objects
        .filter(m3u_account_id=account_id)
        .select_related("series")
    )
    return [
        VodInfo(
            id=rel.series_id,
            relation_id=rel.id,
            name=rel.series.name or "",
            year=getattr(rel.series, "year", None),
            kind="series",
            in_playlist=True,
        )
        for rel in qs
    ]


def diff_series(source_account_id: int, target_account_id: int) -> ProviderDiffResult:
    source_s = _load_series(source_account_id)
    target_s = _load_series(target_account_id)
    return _generic_vod_diff(source_s, target_s)


def _generic_vod_diff(source_list: list[VodInfo], target_list: list[VodInfo]) -> ProviderDiffResult:
    target_by_norm: dict[str, VodInfo] = {}
    for t in target_list:
        n = normalize(t.name)
        if n and n not in target_by_norm:
            target_by_norm[n] = t

    result = ProviderDiffResult()
    matched_target_ids: set[int] = set()

    for src in source_list:
        src_norm = normalize(src.name)

        if src_norm and src_norm in target_by_norm:
            tgt = target_by_norm[src_norm]
            result.matched.append(MatchPair(src, tgt, EXACT_CONFIDENCE))
            matched_target_ids.add(tgt.id)
            continue

        # Fuzzy
        best_ratio = 0.0
        best_tgt   = None
        for tgt in target_list:
            if tgt.id in matched_target_ids:
                continue
            ratio = fuzzy_ratio(src_norm, normalize(tgt.name))
            if ratio > best_ratio:
                best_ratio = ratio
                best_tgt   = tgt

        if best_tgt and best_ratio >= FUZZY_THRESHOLD:
            result.similar.append(MatchPair(src, best_tgt, round(best_ratio, 3)))
            matched_target_ids.add(best_tgt.id)
        else:
            result.missing.append(src)

    for tgt in target_list:
        if tgt.id not in matched_target_ids:
            result.new_only.append(tgt)

    return result


# ── Transfer / apply ──────────────────────────────────────────────────────────

def apply_stream_mappings(
    mappings: list[dict],          # [{"source_stream_id": int, "target_stream_id": int}]
    keep_old_as_fallback: bool = True,
) -> dict:
    """
    For every confirmed mapping pair:
      1. Find all Channels whose primary stream (order=0) is source_stream.
      2. Insert target_stream as the new primary (order=0), push others down.
      3. Optionally keep source_stream as a fallback (last in order).
    Returns counts.
    """
    from apps.channels.models import Channel, ChannelStream, Stream

    updated_channels = 0
    skipped          = 0

    with transaction.atomic():
        for m in mappings:
            src_id = m.get("source_stream_id")
            tgt_id = m.get("target_stream_id")
            if not src_id or not tgt_id:
                skipped += 1
                continue

            try:
                target_stream = Stream.objects.get(id=tgt_id)
            except Stream.DoesNotExist:
                logger.warning("transfer_mappings: target stream %s not found", tgt_id)
                skipped += 1
                continue

            # Find all channels that include source_stream
            channel_ids = (
                ChannelStream.objects
                .filter(stream_id=src_id)
                .values_list("channel_id", flat=True)
                .distinct()
            )

            for ch_id in channel_ids:
                cs_qs = ChannelStream.objects.filter(channel_id=ch_id).order_by("order")
                existing = list(cs_qs)

                # Skip if target already in channel
                if any(cs.stream_id == tgt_id for cs in existing):
                    continue

                # Rebuild order: target first, then existing, optionally drop source
                new_order = []
                new_order.append(target_stream)
                for cs in existing:
                    if cs.stream_id == src_id:
                        if keep_old_as_fallback:
                            new_order.append(cs.stream)  # keep at end
                    else:
                        new_order.append(cs.stream)

                # Delete and recreate ChannelStream rows
                cs_qs.delete()
                ChannelStream.objects.bulk_create([
                    ChannelStream(channel_id=ch_id, stream=s, order=idx)
                    for idx, s in enumerate(new_order)
                ])
                updated_channels += 1

    return {
        "updated_channels": updated_channels,
        "skipped": skipped,
    }


# ── Serialisation helpers (used by api_views) ─────────────────────────────────

def _stream_info_to_dict(s: StreamInfo) -> dict:
    return {
        "id": s.id,
        "name": s.name,
        "tvg_id": s.tvg_id,
        "group": s.group,
        "in_playlist": s.in_playlist,
    }


def _vod_info_to_dict(v: VodInfo) -> dict:
    return {
        "id": v.id,
        "relation_id": v.relation_id,
        "name": v.name,
        "year": v.year,
        "kind": v.kind,
    }


def _item_to_dict(item) -> dict:
    if isinstance(item, StreamInfo):
        return _stream_info_to_dict(item)
    return _vod_info_to_dict(item)


def diff_result_to_dict(result: ProviderDiffResult) -> dict:
    return {
        "matched": [
            {
                "source": _item_to_dict(p.source),
                "target": _item_to_dict(p.target),
                "confidence": p.confidence,
            }
            for p in result.matched
        ],
        "similar": [
            {
                "source": _item_to_dict(p.source),
                "target": _item_to_dict(p.target),
                "confidence": p.confidence,
            }
            for p in result.similar
        ],
        "missing": [_item_to_dict(i) for i in result.missing],
        "new_only": [_item_to_dict(i) for i in result.new_only],
        **result.summary(),
    }
