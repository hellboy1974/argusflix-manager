"""
proxy_helper.py – Zentrale Hilfsfunktionen für Proxy-Konfiguration.

Liest die optionale 'proxy_url' aus account.custom_properties und gibt
ein requests-kompatibles proxies-Dict zurück.

Unterstützte URL-Schemata:
    socks5h://user:pass@host:port   (empfohlen – DNS-Auflösung remote)
    socks5://user:pass@host:port
    http://user:pass@host:port
    https://user:pass@host:port

Benötigt PySocks (bereits als Abhängigkeit installiert).
"""

import logging

logger = logging.getLogger(__name__)


def get_proxies_for_account(account) -> dict | None:
    """
    Gibt ein requests-kompatibles proxies-Dict zurück, wenn für den
    Account eine proxy_url konfiguriert ist. Gibt None zurück wenn
    kein Proxy konfiguriert ist (kein Proxy wird verwendet).

    Args:
        account: M3UAccount-Instanz oder ein Objekt mit custom_properties.

    Returns:
        dict mit 'http' und 'https' Schlüsseln, oder None.
    """
    if account is None:
        return None

    custom = getattr(account, 'custom_properties', None) or {}
    proxy_url = custom.get('proxy_url', '').strip() if isinstance(custom, dict) else ''

    if not proxy_url:
        return None

    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }
    logger.debug(f"Using proxy for account '{getattr(account, 'name', '?')}': {_redact_url(proxy_url)}")
    return proxies


def get_proxies_from_url(proxy_url: str | None) -> dict | None:
    """
    Gibt ein proxies-Dict für eine direkte proxy_url zurück.
    Hilfreich wenn kein Account-Objekt verfügbar ist.

    Args:
        proxy_url: SOCKS5H/HTTP Proxy-URL oder None/Leerstring.

    Returns:
        dict mit 'http' und 'https' Schlüsseln, oder None.
    """
    if not proxy_url or not proxy_url.strip():
        return None

    proxy_url = proxy_url.strip()
    return {
        'http': proxy_url,
        'https': proxy_url,
    }


def _redact_url(url: str) -> str:
    """Verbirgt Passwörter in URLs für sichere Log-Ausgaben."""
    try:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        if parsed.password:
            netloc = f"{parsed.username}:***@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            return urlunparse(parsed._replace(netloc=netloc))
    except Exception:
        pass
    return url
