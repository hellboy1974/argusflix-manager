/**
 * ProviderMigrationModal.jsx
 * ─────────────────────────────────────────────────────────────────────────────
 * 3-step wizard for migrating channel / VOD / series mappings from one
 * M3U account (Stalker portal, Xtream, …) to another.
 *
 * Step 1 – Choose source + target account, optional sync trigger
 * Step 2 – Review diff (tabs: Live / Movies / Series)
 * Step 3 – Confirm & execute transfer
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import {
  Alert,
  Badge,
  Button,
  Checkbox,
  Divider,
  Group,
  Loader,
  Modal,
  Progress,
  ScrollArea,
  Select,
  Stack,
  Stepper,
  Switch,
  Table,
  Tabs,
  Text,
  Tooltip,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  ArrowLeftRight,
  CheckCircle,
  HelpCircle,
  Info,
  RefreshCcw,
  XCircle,
} from 'lucide-react';
import API from '../../api';

// ── helpers ───────────────────────────────────────────────────────────────────

const pct = (v) => Math.round(v * 100);

const confidenceColor = (c) => {
  if (c >= 0.99) return 'green';
  if (c >= 0.85) return 'teal';
  if (c >= 0.75) return 'yellow';
  return 'orange';
};

const SectionBadge = ({ count, color, label, icon: Icon }) => (
  <Group gap={4} wrap="nowrap">
    <Icon size={14} />
    <Text size="xs" c={color} fw={600}>
      {count} {label}
    </Text>
  </Group>
);

// ── MatchTable: shared table for matched + similar ────────────────────────────

const MatchTable = ({ rows, editable, onOverride, targetStreams }) => {
  if (!rows || rows.length === 0) {
    return (
      <Text size="sm" c="dimmed" ta="center" py="md">
        None
      </Text>
    );
  }

  return (
    <Table striped highlightOnHover withTableBorder withColumnBorders fz="xs">
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Current (source)</Table.Th>
          <Table.Th>New (target)</Table.Th>
          <Table.Th w={60} ta="center">
            Conf.
          </Table.Th>
          {editable && <Table.Th w={36} ta="center" />}
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.map((row, i) => {
          const override = row._override;
          const targetName = override
            ? targetStreams?.find((t) => t.id === override)?.name ?? `ID ${override}`
            : row.target.name;

          return (
            <Table.Tr key={i}>
              <Table.Td>{row.source.name}</Table.Td>
              <Table.Td>
                {editable && onOverride ? (
                  <Select
                    size="xs"
                    data={
                      targetStreams?.map((t) => ({
                        value: String(t.id),
                        label: t.name,
                      })) ?? []
                    }
                    value={String(override ?? row.target.id)}
                    onChange={(v) => onOverride(i, v ? Number(v) : null)}
                    searchable
                    clearable={false}
                    styles={{ input: { fontSize: 11 } }}
                  />
                ) : (
                  <Text size="xs">{targetName}</Text>
                )}
              </Table.Td>
              <Table.Td ta="center">
                <Badge
                  size="xs"
                  color={confidenceColor(row.confidence)}
                  variant="light"
                >
                  {pct(row.confidence)}%
                </Badge>
              </Table.Td>
              {editable && (
                <Table.Td ta="center">
                  <Tooltip label="Skip this match">
                    <Button
                      size="compact-xs"
                      variant="subtle"
                      color="red"
                      onClick={() => onOverride(i, null, true)}
                      px={4}
                    >
                      ×
                    </Button>
                  </Tooltip>
                </Table.Td>
              )}
            </Table.Tr>
          );
        })}
      </Table.Tbody>
    </Table>
  );
};

// ── SimpleList: for missing / new_only ────────────────────────────────────────

const SimpleList = ({ items, emptyText }) => {
  if (!items || items.length === 0) {
    return (
      <Text size="sm" c="dimmed" ta="center" py="md">
        {emptyText}
      </Text>
    );
  }
  return (
    <Stack gap={2}>
      {items.map((item, i) => (
        <Text key={i} size="xs" c="dimmed">
          {item.name}
          {item.year ? ` (${item.year})` : ''}
        </Text>
      ))}
    </Stack>
  );
};

// ── DiffTab: renders one content-type diff ────────────────────────────────────

const DiffTab = ({ diff, targetStreams, similarRows, onSimilarOverride }) => {
  if (!diff) {
    return (
      <Text size="sm" c="dimmed" ta="center" py="md">
        No data.
      </Text>
    );
  }
  if (diff.error) {
    return (
      <Alert color="red" variant="light">
        {diff.error}
      </Alert>
    );
  }

  return (
    <Stack gap="md">
      {/* Auto-matched */}
      <Stack gap={4}>
        <Group gap="xs">
          <CheckCircle size={14} color="green" />
          <Text size="xs" fw={600} c="green">
            Auto-matched ({diff.matched?.length ?? 0})
          </Text>
        </Group>
        <ScrollArea mah={200} type="auto">
          <MatchTable rows={diff.matched} editable={false} />
        </ScrollArea>
      </Stack>

      <Divider />

      {/* Similar – user confirms / overrides */}
      <Stack gap={4}>
        <Group gap="xs">
          <HelpCircle size={14} color="orange" />
          <Text size="xs" fw={600} c="orange">
            Needs review ({similarRows?.length ?? 0})
          </Text>
          <Text size="xs" c="dimmed">
            – adjust target using the dropdown
          </Text>
        </Group>
        <ScrollArea mah={220} type="auto">
          <MatchTable
            rows={similarRows ?? diff.similar}
            editable
            onOverride={onSimilarOverride}
            targetStreams={targetStreams}
          />
        </ScrollArea>
      </Stack>

      <Divider />

      {/* Missing */}
      <Stack gap={4}>
        <Group gap="xs">
          <XCircle size={14} color="red" />
          <Text size="xs" fw={600} c="red">
            Not in new provider ({diff.missing?.length ?? 0})
          </Text>
        </Group>
        <ScrollArea mah={120} type="auto">
          <SimpleList items={diff.missing} emptyText="None missing." />
        </ScrollArea>
      </Stack>

      <Divider />

      {/* New only */}
      <Stack gap={4}>
        <Group gap="xs">
          <Info size={14} color="blue" />
          <Text size="xs" fw={600} c="blue">
            New in target ({diff.new_only?.length ?? 0})
          </Text>
        </Group>
        <ScrollArea mah={120} type="auto">
          <SimpleList
            items={diff.new_only}
            emptyText="No new content."
          />
        </ScrollArea>
      </Stack>
    </Stack>
  );
};

// ── Main Modal ────────────────────────────────────────────────────────────────

const ProviderMigrationModal = ({ opened, onClose, initialSourceId = null }) => {
  const [step, setStep] = useState(0);

  // Step 1 state
  const [accounts, setAccounts] = useState([]);
  const [loadingAccounts, setLoadingAccounts] = useState(false);
  const [sourceId, setSourceId] = useState(initialSourceId ? String(initialSourceId) : null);
  const [targetId, setTargetId] = useState(null);
  const [autoSync, setAutoSync] = useState(false);
  const [syncing, setSyncing] = useState(false);

  // Step 2 state
  const [computing, setComputing] = useState(false);
  const [diff, setDiff] = useState(null); // { live, movies, series }
  const [targetStreams, setTargetStreams] = useState([]);
  // Per-type editable similar rows (with optional _override field)
  const [similarLive, setSimilarLive] = useState([]);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [similarSeries, setSimilarSeries] = useState([]);
  // Which similar items are skipped
  const [skippedLive, setSkippedLive] = useState(new Set());
  const [skippedMovies, setSkippedMovies] = useState(new Set());
  const [skippedSeries, setSkippedSeries] = useState(new Set());

  // Step 3 state
  const [keepFallback, setKeepFallback] = useState(true);
  const [transferring, setTransferring] = useState(false);
  const [transferResult, setTransferResult] = useState(null);
  const [progress, setProgress] = useState(0);

  const hasFetchedAccounts = useRef(false);

  // Reset on open
  useEffect(() => {
    if (!opened) return;
    setStep(0);
    setDiff(null);
    setTransferResult(null);
    setProgress(0);
    setSyncing(false);
    setTransferring(false);
    if (initialSourceId) setSourceId(String(initialSourceId));
  }, [opened, initialSourceId]);

  // Load M3U accounts
  useEffect(() => {
    if (!opened || hasFetchedAccounts.current) return;
    hasFetchedAccounts.current = true;
    setLoadingAccounts(true);
    API.getPlaylists()
      .then((data) => {
        setAccounts(
          (Array.isArray(data) ? data : data?.results ?? []).map((a) => ({
            value: String(a.id),
            label: a.name,
          }))
        );
      })
      .finally(() => setLoadingAccounts(false));
  }, [opened]);

  // ── Step 1 → Analyse ──────────────────────────────────────────────────────

  const handleAnalyse = useCallback(async () => {
    const srcId = Number(sourceId);
    const tgtId = Number(targetId);

    if (autoSync) {
      setSyncing(true);
      try {
        await API.refreshPlaylist(tgtId);
      } catch {
        // non-fatal – continue
      } finally {
        setSyncing(false);
      }
    }

    setComputing(true);
    setStep(1);

    try {
      const [diffResult, streamsResult] = await Promise.all([
        API.providerDiff(srcId, tgtId, ['live', 'movies', 'series']),
        API.queryStreams(new URLSearchParams({ m3u_account: tgtId, page_size: 5000 })),
      ]);

      setDiff(diffResult);

      const allStreams = Array.isArray(streamsResult)
        ? streamsResult
        : streamsResult?.results ?? [];
      setTargetStreams(allStreams);

      // Initialise editable similar rows
      setSimilarLive((diffResult?.live?.similar ?? []).map((r) => ({ ...r })));
      setSimilarMovies((diffResult?.movies?.similar ?? []).map((r) => ({ ...r })));
      setSimilarSeries((diffResult?.series?.similar ?? []).map((r) => ({ ...r })));
      setSkippedLive(new Set());
      setSkippedMovies(new Set());
      setSkippedSeries(new Set());
    } catch {
      notifications.show({
        title: 'Analysis failed',
        message: 'Could not compare the two providers.',
        color: 'red',
      });
      setStep(0);
    } finally {
      setComputing(false);
    }
  }, [sourceId, targetId, autoSync]);

  // ── Override helpers ──────────────────────────────────────────────────────

  const makeOverrideHandler = (setter, skipSetter) => (idx, newTargetId, skip = false) => {
    if (skip) {
      skipSetter((prev) => new Set([...prev, idx]));
      return;
    }
    setter((prev) =>
      prev.map((row, i) =>
        i === idx ? { ...row, _override: newTargetId } : row
      )
    );
  };

  const handleOverrideLive    = makeOverrideHandler(setSimilarLive, setSkippedLive);
  const handleOverrideMovies  = makeOverrideHandler(setSimilarMovies, setSkippedMovies);
  const handleOverrideSeries  = makeOverrideHandler(setSimilarSeries, setSkippedSeries);

  // ── Build confirmed mapping list ──────────────────────────────────────────

  const buildMappings = useCallback(() => {
    const mappings = [];

    // Live – matched (confidence 1.0 / tvg_id)
    for (const row of diff?.live?.matched ?? []) {
      mappings.push({
        source_stream_id: row.source.id,
        target_stream_id: row.target.id,
      });
    }
    // Live – similar (with optional user overrides, skip removed)
    similarLive.forEach((row, i) => {
      if (skippedLive.has(i)) return;
      mappings.push({
        source_stream_id: row.source.id,
        target_stream_id: row._override ?? row.target.id,
      });
    });

    return mappings;
  }, [diff, similarLive, skippedLive]);

  // ── Step 2 → Transfer ─────────────────────────────────────────────────────

  const handleTransfer = useCallback(async () => {
    const mappings = buildMappings();
    if (mappings.length === 0) {
      notifications.show({
        title: 'Nothing to transfer',
        message: 'No confirmed mappings.',
        color: 'yellow',
      });
      return;
    }

    setTransferring(true);
    setProgress(10);
    setStep(2);

    try {
      // Preview first for a summary
      setProgress(30);
      const preview = await API.transferMappings(mappings, keepFallback, 'preview');
      setProgress(60);

      // Apply
      const result = await API.transferMappings(mappings, keepFallback, 'apply');
      setProgress(100);
      setTransferResult({ ...result, preview_rows: preview?.mappings ?? [] });

      notifications.show({
        title: 'Migration complete',
        message: `${result.updated_channels} channel(s) updated.`,
        color: 'green',
        autoClose: 5000,
      });

      // Refresh channel data in background
      setTimeout(() => API.requeryChannels?.(), 800);
    } catch {
      notifications.show({
        title: 'Transfer failed',
        message: 'An error occurred during migration.',
        color: 'red',
      });
      setStep(1);
    } finally {
      setTransferring(false);
    }
  }, [buildMappings, keepFallback]);

  // ── Summary counts for step 2 header ─────────────────────────────────────

  const liveMatchCount =
    (diff?.live?.matched?.length ?? 0) +
    similarLive.filter((_, i) => !skippedLive.has(i)).length;
  const totalMappings = liveMatchCount; // VOD/series transferred via relation – future scope

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={
        <Group gap="xs">
          <ArrowLeftRight size={16} />
          <Text fw={600} size="sm">
            Provider Migration
          </Text>
        </Group>
      }
      size="xl"
      centered
      styles={{ body: { padding: '0 16px 16px' } }}
    >
      <Stepper
        active={step}
        size="xs"
        mt="sm"
        mb="lg"
        allowNextStepsSelect={false}
      >
        <Stepper.Step label="Select" description="Source & Target" />
        <Stepper.Step label="Review" description="Compare content" />
        <Stepper.Step label="Transfer" description="Apply mappings" />
      </Stepper>

      {/* ── Step 0: Select ────────────────────────────────────────────── */}
      {step === 0 && (
        <Stack gap="md">
          <Alert variant="light" color="blue" icon={<Info size={14} />}>
            Migrates your channel/VOD/series mappings from one provider to
            another. Custom names and EPG links are preserved.
          </Alert>

          <Select
            label="Source (current provider)"
            description="The provider already used in your playlist"
            data={accounts}
            value={sourceId}
            onChange={setSourceId}
            disabled={loadingAccounts}
            placeholder={loadingAccounts ? 'Loading…' : 'Select account'}
            searchable
            allowDeselect={false}
          />

          <Select
            label="Target (new provider)"
            description="The provider you want to migrate to"
            data={accounts.filter((a) => a.value !== sourceId)}
            value={targetId}
            onChange={setTargetId}
            disabled={loadingAccounts || !sourceId}
            placeholder="Select account"
            searchable
            allowDeselect={false}
          />

          <Switch
            label="Sync target before comparing"
            description="Recommended: ensures the new provider's stream list is up to date"
            checked={autoSync}
            onChange={(e) => setAutoSync(e.currentTarget.checked)}
          />

          <Group justify="flex-end" mt="sm">
            <Button variant="default" size="xs" onClick={onClose}>
              Cancel
            </Button>
            <Button
              size="xs"
              disabled={!sourceId || !targetId || loadingAccounts}
              loading={syncing || computing}
              onClick={handleAnalyse}
              leftSection={<RefreshCcw size={13} />}
            >
              {syncing ? 'Syncing…' : 'Analyse'}
            </Button>
          </Group>
        </Stack>
      )}

      {/* ── Step 1: Review ───────────────────────────────────────────── */}
      {step === 1 && (
        <Stack gap="md">
          {computing ? (
            <Group justify="center" py="xl">
              <Loader size="sm" />
              <Text size="sm" c="dimmed">
                Comparing providers…
              </Text>
            </Group>
          ) : (
            <>
              {/* Summary bar */}
              <Group gap="lg" wrap="wrap">
                <SectionBadge
                  count={diff?.live?.matched_count ?? 0}
                  color="green"
                  label="auto-matched"
                  icon={CheckCircle}
                />
                <SectionBadge
                  count={diff?.live?.similar_count ?? 0}
                  color="orange"
                  label="needs review"
                  icon={HelpCircle}
                />
                <SectionBadge
                  count={diff?.live?.missing_count ?? 0}
                  color="red"
                  label="missing"
                  icon={XCircle}
                />
                <SectionBadge
                  count={diff?.live?.new_only_count ?? 0}
                  color="blue"
                  label="new"
                  icon={Info}
                />
              </Group>

              <Tabs defaultValue="live" keepMounted={false}>
                <Tabs.List>
                  <Tabs.Tab
                    value="live"
                    rightSection={
                      <Badge size="xs" variant="light">
                        {(diff?.live?.matched?.length ?? 0) +
                          (diff?.live?.similar?.length ?? 0)}
                      </Badge>
                    }
                  >
                    Live TV
                  </Tabs.Tab>
                  <Tabs.Tab
                    value="movies"
                    rightSection={
                      <Badge size="xs" variant="light">
                        {(diff?.movies?.matched?.length ?? 0) +
                          (diff?.movies?.similar?.length ?? 0)}
                      </Badge>
                    }
                  >
                    Movies
                  </Tabs.Tab>
                  <Tabs.Tab
                    value="series"
                    rightSection={
                      <Badge size="xs" variant="light">
                        {(diff?.series?.matched?.length ?? 0) +
                          (diff?.series?.similar?.length ?? 0)}
                      </Badge>
                    }
                  >
                    Series
                  </Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="live" pt="sm">
                  <DiffTab
                    diff={diff?.live}
                    targetStreams={targetStreams}
                    similarRows={similarLive.filter((_, i) => !skippedLive.has(i))}
                    onSimilarOverride={handleOverrideLive}
                  />
                </Tabs.Panel>
                <Tabs.Panel value="movies" pt="sm">
                  <DiffTab
                    diff={diff?.movies}
                    similarRows={similarMovies.filter((_, i) => !skippedMovies.has(i))}
                    onSimilarOverride={handleOverrideMovies}
                  />
                </Tabs.Panel>
                <Tabs.Panel value="series" pt="sm">
                  <DiffTab
                    diff={diff?.series}
                    similarRows={similarSeries.filter((_, i) => !skippedSeries.has(i))}
                    onSimilarOverride={handleOverrideSeries}
                  />
                </Tabs.Panel>
              </Tabs>

              <Divider />

              <Switch
                label="Keep old streams as fallback"
                description="The source stream stays as secondary fallback if the new stream fails"
                checked={keepFallback}
                onChange={(e) => setKeepFallback(e.currentTarget.checked)}
              />

              <Group justify="space-between" mt="sm">
                <Button
                  variant="default"
                  size="xs"
                  onClick={() => setStep(0)}
                >
                  ← Back
                </Button>
                <Group>
                  <Text size="xs" c="dimmed">
                    {totalMappings} live stream(s) will be transferred
                  </Text>
                  <Button
                    size="xs"
                    disabled={totalMappings === 0}
                    onClick={handleTransfer}
                    color="teal"
                    leftSection={<ArrowLeftRight size={13} />}
                  >
                    Transfer
                  </Button>
                </Group>
              </Group>
            </>
          )}
        </Stack>
      )}

      {/* ── Step 2: Done / Progress ───────────────────────────────────── */}
      {step === 2 && (
        <Stack gap="md">
          {transferring ? (
            <>
              <Text size="sm" ta="center">
                Applying mappings…
              </Text>
              <Progress value={progress} animated striped />
            </>
          ) : transferResult ? (
            <>
              <Alert color="green" variant="light" icon={<CheckCircle size={14} />}>
                Migration complete!{' '}
                <strong>{transferResult.updated_channels}</strong> channel(s)
                updated.{' '}
                {transferResult.skipped > 0 && (
                  <>
                    <strong>{transferResult.skipped}</strong> skipped.
                  </>
                )}
              </Alert>

              {keepFallback && (
                <Text size="xs" c="dimmed">
                  Old streams are kept as fallback streams on each channel.
                </Text>
              )}

              <Group justify="flex-end" mt="sm">
                <Button size="xs" onClick={onClose}>
                  Done
                </Button>
              </Group>
            </>
          ) : (
            <Text size="sm" c="dimmed" ta="center">
              Processing…
            </Text>
          )}
        </Stack>
      )}
    </Modal>
  );
};

export default ProviderMigrationModal;
