import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  AppShellMain,
  Text,
  Badge,
  Group,
  Button,
  Tabs,
  Card,
  Table,
  ActionIcon,
  Modal,
  TextInput,
  Switch,
  Stack,
  Textarea,
  NumberInput,
  Grid,
  SimpleGrid,
  Accordion,
  Progress,
  List,
  ThemeIcon,
  Select,
  Alert,
  Loader,
  Divider,
  Checkbox,
} from '@mantine/core';
import {
  Terminal,
  Globe,
  Search,
  Plus,
  Trash2,
  Edit2,
  Check,
  AlertTriangle,
  FileText,
  Sliders,
  Play,
  Square,
  RefreshCw,
  Cpu,
  Lock,
  ExternalLink,
  Shield,
  Activity,
  History,
  Key,
} from 'lucide-react';
import { usePluginStore } from '../store/plugins.jsx';
import { showNotification } from '../utils/notificationUtils.js';
import API from '../api';

const KNOWN_PREFIXES = [
  { value: '00:1A:79:', label: '00:1A:79: (Standard MAG)' },
  { value: '74:1A:79:', label: '74:1A:79: (Newer MAG)' },
  { value: 'D4:CF:F9:', label: 'D4:CF:F9: (Newer MAG)' },
  { value: '00:1A:78:', label: '00:1A:78: (Older MAG)' },
  { value: '00:1E:B8:', label: '00:1E:B8: (Infomir)' },
  { value: '00:01:5F:', label: '00:01:5F:' },
  { value: '00:02:F2:', label: '00:02:F2:' },
  { value: '00:03:93:', label: '00:03:93:' },
  { value: '00:03:FF:', label: '00:03:FF:' },
  { value: '00:04:4F:', label: '00:04:4F:' },
  { value: '00:05:69:', label: '00:05:69:' },
  { value: '00:05:9A:', label: '00:05:9A:' },
  { value: '00:07:AB:', label: '00:07:AB:' },
  { value: '00:09:18:', label: '00:09:18:' },
  { value: '00:09:C7:', label: '00:09:C7:' },
  { value: '00:09:DF:', label: '00:09:DF:' },
  { value: '00:0A:27:', label: '00:0A:27:' },
  { value: '00:0C:29:', label: '00:0C:29:' },
  { value: '00:0E:50:', label: '00:0E:50:' },
  { value: '00:0E:8F:', label: '00:0E:8F:' },
  { value: '00:0F:4B:', label: '00:0F:4B:' },
  { value: '00:11:D8:', label: '00:11:D8:' },
  { value: '00:13:E8:', label: '00:13:E8:' },
  { value: '00:14:22:', label: '00:14:22:' },
  { value: '00:15:AD:', label: '00:15:AD:' },
  { value: '00:16:3E:', label: '00:16:3E:' },
  { value: '00:18:82:', label: '00:18:82:' },
  { value: '00:18:BD:', label: '00:18:BD:' },
  { value: '00:19:66:', label: '00:19:66:' },
  { value: '00:19:E0:', label: '00:19:E0:' },
  { value: '00:1A:70:', label: '00:1A:70:' },
  { value: '00:1A:E9:', label: '00:1A:E9:' },
  { value: '00:1B:79:', label: '00:1B:79:' },
  { value: '00:1B:EA:', label: '00:1B:EA:' },
  { value: '00:1C:14:', label: '00:1C:14:' },
  { value: '00:1C:19:', label: '00:1C:19:' },
  { value: '00:1C:42:', label: '00:1C:42:' },
  { value: '00:1C:79:', label: '00:1C:79:' },
  { value: '00:1D:20:', label: '00:1D:20:' },
  { value: '00:1D:79:', label: '00:1D:79:' },
  { value: '00:1D:D5:', label: '00:1D:D5:' },
  { value: '00:1E:79:', label: '00:1E:79:' },
  { value: '00:1E:8A:', label: '00:1E:8A:' },
  { value: '00:1F:16:', label: '00:1F:16:' },
  { value: '00:1F:33:', label: '00:1F:33:' },
  { value: '00:1F:3A:', label: '00:1F:3A:' },
  { value: '00:1F:79:', label: '00:1F:79:' },
  { value: '00:20:91:', label: '00:20:91:' },
  { value: '00:21:5C:', label: '00:21:5C:' },
  { value: '00:22:93:', label: '00:22:93:' },
  { value: '00:23:45:', label: '00:23:45:' },
  { value: '00:24:D4:', label: '00:24:D4:' },
  { value: '00:25:90:', label: '00:25:90:' },
  { value: '00:26:75:', label: '00:26:75:' },
  { value: '00:2A:01:', label: '00:2A:01:' },
  { value: '00:2A:79:', label: '00:2A:79:' },
  { value: '00:30:18:', label: '00:30:18:' },
  { value: '00:40:96:', label: '00:40:96:' },
  { value: '00:50:56:', label: '00:50:56:' },
  { value: '00:60:2F:', label: '00:60:2F:' },
  { value: '00:90:0B:', label: '00:90:0B:' },
  { value: '00:A0:C9:', label: '00:A0:C9:' },
  { value: '00:A1:79:', label: '00:A1:79:' },
  { value: '00:D0:D0:', label: '00:D0:D0:' },
  { value: '00:E0:4C:', label: '00:E0:4C:' },
  { value: '04:D6:AA:', label: '04:D6:AA:' },
  { value: '08:00:27:', label: '08:00:27:' },
  { value: '08:05:81:', label: '08:05:81:' },
  { value: '08:9E:08:', label: '08:9E:08:' },
  { value: '0C:47:C9:', label: '0C:47:C9:' },
  { value: '10:27:BE:', label: '10:27:BE:' },
  { value: '11:33:01:', label: '11:33:01:' },
  { value: '18:C8:E7:', label: '18:C8:E7:' },
  { value: '1A:00:6A:', label: '1A:00:6A:' },
  { value: '1A:00:FB:', label: '1A:00:FB:' },
  { value: '30:87:30:', label: '30:87:30:' },
  { value: '33:44:CF:', label: '33:44:CF:' },
  { value: '55:93:EA:', label: '55:93:EA:' },
  { value: '68:FF:7B:', label: '68:FF:7B:' },
  { value: 'A0:BB:3E:', label: 'A0:BB:3E:' },
  { value: 'BC:2F:D0:', label: 'BC:2F:D0:' },
  { value: 'DC:9A:2F:', label: 'DC:9A:2F:' },
  { value: 'E0:37:17:', label: 'E0:37:17:' }
];

export default function StalkerToolbox() {
  const plugins = usePluginStore((state) => state.plugins);
  const loadingPlugins = usePluginStore((state) => state.loading);
  const fetchPlugins = usePluginStore((state) => state.fetchPlugins);

  // Load plugins list on mount
  useEffect(() => {
    fetchPlugins();
  }, []);

  const plugin = useMemo(() => {
    const normalActive = plugins.find((p) => p.key === 'stalker_toolbox' && p.enabled);
    if (normalActive) return normalActive;

    const hardcodedActive = plugins.find((p) => p.key === 'stalker_toolbox_hardcoded' && p.enabled);
    if (hardcodedActive) return hardcodedActive;

    return plugins.find((p) => p.key === 'stalker_toolbox') || plugins.find((p) => p.key === 'stalker_toolbox_hardcoded');
  }, [plugins]);
  const pluginKey = plugin?.key || 'stalker_toolbox';
  const enabled = plugin?.enabled;
  const settings = plugin?.settings || {};

  // Local settings states (synced when plugin config loads)
  const [portalsList, setPortalsList] = useState([]);
  const [bulkImportText, setBulkImportText] = useState('');
  const [detectiveUrl, setDetectiveUrl] = useState('');
  const [detectiveUrlscanKey, setDetectiveUrlscanKey] = useState('');
  const [detectiveScanSubdomains, setDetectiveScanSubdomains] = useState(false);
  const [detectiveScanPorts, setDetectiveScanPorts] = useState(false);
  
  const [genPrefixes, setGenPrefixes] = useState('00:1A:79:');
  const [genCount, setGenCount] = useState(1000);
  const [genMode, setGenMode] = useState('random');
  const [genSuffixStart, setGenSuffixStart] = useState('');
  const [genSuffixEnd, setGenSuffixEnd] = useState('');
  const [genFilename, setGenFilename] = useState('combo.txt');

  const [selectedPrefixes, setSelectedPrefixes] = useState(['00:1A:79:']);
  const [customPrefixes, setCustomPrefixes] = useState('');

  const reassemblePrefixes = (selected, custom) => {
    const customParts = custom.split(',').map(p => p.trim()).filter(Boolean);
    const combined = [...selected, ...customParts].join(',');
    setGenPrefixes(combined);
  };

  const handlePrefixCheckboxChange = (value, checked) => {
    let updated;
    if (checked) {
      updated = [...selectedPrefixes, value];
    } else {
      updated = selectedPrefixes.filter(p => p !== value);
    }
    setSelectedPrefixes(updated);
    reassemblePrefixes(updated, customPrefixes);
  };

  const handleCustomPrefixChange = (value) => {
    setCustomPrefixes(value);
    reassemblePrefixes(selectedPrefixes, value);
  };

  const handleSelectAllPrefixes = () => {
    const all = KNOWN_PREFIXES.map(kp => kp.value);
    setSelectedPrefixes(all);
    reassemblePrefixes(all, customPrefixes);
  };

  const handleDeselectAllPrefixes = () => {
    setSelectedPrefixes([]);
    reassemblePrefixes([], customPrefixes);
  };

  const [scanPortal, setScanPortal] = useState('');
  const [scanMacStart, setScanMacStart] = useState('00:1A:79:00:00:00');
  const [scanMacEnd, setScanMacEnd] = useState('00:1A:79:00:00:FF');
  const [scanThreads, setScanThreads] = useState(5);
  const [scanCooldown, setScanCooldown] = useState(1.0);

  const [proxiesPaste, setProxiesPaste] = useState('');
  const [proxyUrls, setProxyUrls] = useState('');

  const [syncLive, setSyncLive] = useState(true);
  const [syncVod, setSyncVod] = useState(false);
  const [syncSeries, setSyncSeries] = useState(false);
  const [syncVodLimit, setSyncVodLimit] = useState(100);
  const [syncSeriesLimit, setSyncSeriesLimit] = useState(50);

  const [categoriesModalOpen, setCategoriesModalOpen] = useState(false);
  const [activeCategoriesPortalIdx, setActiveCategoriesPortalIdx] = useState(null);
  const [loadingCategories, setLoadingCategories] = useState(false);
  const [portalCategories, setPortalCategories] = useState({ live: [], vod: [], series: [] });
  const [selectedLiveCats, setSelectedLiveCats] = useState([]);
  const [selectedVodCats, setSelectedVodCats] = useState([]);
  const [selectedSeriesCats, setSelectedSeriesCats] = useState([]);

  // UI operation states
  const [saving, setSaving] = useState(false);
  const [actionRunning, setActionRunning] = useState(null);
  const [logOutput, setLogOutput] = useState('');
  const [portalModalOpen, setPortalModalOpen] = useState(false);
  const [editingPortalIdx, setEditingPortalIdx] = useState(null);
  const [portalNameInput, setPortalNameInput] = useState('');
  const [portalUrlInput, setPortalUrlInput] = useState('');
  const [portalMacInput, setPortalMacInput] = useState('');
  const [portalUaInput, setPortalUaInput] = useState('Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3');
  const [portalActiveInput, setPortalActiveInput] = useState(true);

  // Scan polling state
  const [scanStatus, setScanStatus] = useState({
    running: false,
    portal: null,
    current_mac: null,
    checked: 0,
    total: 0,
    active_found: 0,
    results: [],
  });
  const scanIntervalRef = useRef(null);

  // Parse portals list whenever settings load
  useEffect(() => {
    if (settings.portals_json) {
      try {
        setPortalsList(jsonParse(settings.portals_json));
      } catch (e) {
        setPortalsList([]);
      }
    } else {
      setPortalsList([]);
    }
    setBulkImportText(settings.bulk_import_text || '');
    setDetectiveUrl(settings.detective_url || '');
    setDetectiveUrlscanKey(settings.detective_urlscan_key || '');
    setDetectiveScanSubdomains(!!settings.detective_scan_subdomains);
    setDetectiveScanPorts(!!settings.detective_scan_ports);

    const prefixesStr = settings.gen_prefixes || '00:1A:79:';
    setGenPrefixes(prefixesStr);
    
    const parts = prefixesStr.split(',').map(p => p.trim()).filter(Boolean);
    const knownValues = KNOWN_PREFIXES.map(kp => kp.value);
    const selected = parts.filter(p => knownValues.includes(p));
    const custom = parts.filter(p => !knownValues.includes(p)).join(', ');
    
    setSelectedPrefixes(selected);
    setCustomPrefixes(custom);

    setGenCount(settings.gen_count ?? 1000);
    setGenMode(settings.gen_mode || 'random');
    setGenSuffixStart(settings.gen_suffix_start || '');
    setGenSuffixEnd(settings.gen_suffix_end || '');
    setGenFilename(settings.gen_filename || 'combo.txt');

    setScanPortal(settings.scan_portal || '');
    setScanMacStart(settings.scan_mac_start || '00:1A:79:00:00:00');
    setScanMacEnd(settings.scan_mac_end || '00:1A:79:00:00:FF');
    setScanThreads(settings.scan_threads ?? 5);
    setScanCooldown(settings.scan_cooldown ?? 1.0);

    setProxiesPaste(settings.proxies_paste || '');
    setProxyUrls(settings.proxy_urls || '');

    setSyncLive(settings.sync_live !== false);
    setSyncVod(!!settings.sync_vod);
    setSyncSeries(!!settings.sync_series);
    setSyncVodLimit(settings.sync_vod_limit ?? 100);
    setSyncSeriesLimit(settings.sync_series_limit ?? 50);
  }, [settings]);

  // Handle active scanner status polling
  useEffect(() => {
    if (enabled) {
      // Fetch scan status initially
      fetchScanStatus();
      scanIntervalRef.current = setInterval(fetchScanStatus, 2000);
    }
    return () => {
      if (scanIntervalRef.current) clearInterval(scanIntervalRef.current);
    };
  }, [enabled]);

  const jsonParse = (str) => {
    try {
      return JSON.parse(str);
    } catch {
      return [];
    }
  };

  const fetchScanStatus = async () => {
    if (!enabled) return;
    try {
      const resp = await API.runPluginAction(pluginKey, 'get_scan_status');
      if (resp?.success && resp.result) {
        setScanStatus(resp.result);
      }
    } catch (e) {
      // Silent error
    }
  };

  const handleEnablePlugin = async () => {
    const resp = await API.setPluginEnabled(pluginKey, true);
    if (resp?.success) {
      usePluginStore.getState().updatePlugin(pluginKey, { enabled: true, ever_enabled: true });
      showNotification({
        title: 'Plugin Enabled',
        message: 'Stalker Portal Toolbox plugin enabled successfully.',
        color: 'green',
      });
      fetchPlugins();
    }
  };

  // Generic helper to update backend settings
  const saveFields = async (updatedFields) => {
    setSaving(true);
    try {
      const fullSettings = { ...settings, ...updatedFields };
      const resp = await API.updatePluginSettings(pluginKey, fullSettings);
      if (resp) {
        usePluginStore.getState().updatePlugin(pluginKey, { settings: resp });
        return true;
      }
    } catch (e) {
      showNotification({
        title: 'Error Saving Settings',
        message: e?.message || 'Failed to save plugin settings.',
        color: 'red',
      });
    } finally {
      setSaving(false);
    }
    return false;
  };

  // Run backend action helper
  const executeAction = async (actionId, preSaveSettings = null) => {
    setActionRunning(actionId);
    setLogOutput(`Starting action: ${actionId}...\n`);
    try {
      if (preSaveSettings) {
        const saved = await saveFields(preSaveSettings);
        if (!saved) {
          setActionRunning(null);
          return;
        }
      }
      const resp = await API.runPluginAction(pluginKey, actionId);
      if (resp?.success) {
        const message = resp.result?.message || 'Action executed successfully.';
        setLogOutput((prev) => prev + `[SUCCESS] ${message}\n`);
        showNotification({
          title: 'Stalker Toolbox',
          message: message.split('\n')[0],
          color: 'green',
        });
        // Invalidate plugins to get latest settings (e.g. portals_json after bulk import, or detective_history)
        await fetchPlugins();
      } else {
        const err = resp?.error || 'Action failed.';
        setLogOutput((prev) => prev + `[ERROR] ${err}\n`);
        showNotification({
          title: 'Action Failed',
          message: String(err),
          color: 'red',
        });
      }
    } catch (e) {
      setLogOutput((prev) => prev + `[ERROR] ${e.message || e}\n`);
      showNotification({
        title: 'Error Running Action',
        message: e.message || String(e),
        color: 'red',
      });
    } finally {
      setActionRunning(null);
      // Update scan status immediately if scan started
      if (actionId === 'scan_macs') {
        setTimeout(fetchScanStatus, 1000);
      }
    }
  };

  const handleOpenManageCategories = (idx) => {
    const p = portalsList[idx];
    setActiveCategoriesPortalIdx(idx);
    
    const sel = p.selected_categories || {};
    setSelectedLiveCats(sel.live || null);
    setSelectedVodCats(sel.vod || null);
    setSelectedSeriesCats(sel.series || null);
    
    setPortalCategories({ live: [], vod: [], series: [] });
    setCategoriesModalOpen(true);
    
    fetchPortalCategories(idx);
  };

  const fetchPortalCategories = async (idx) => {
    const p = portalsList[idx];
    setLoadingCategories(true);
    try {
      const resp = await API.runPluginAction(pluginKey, 'fetch_portal_categories', { portal_name: p.name });
      if (resp?.success && resp.result?.status === 'ok') {
        const { live, vod, series } = resp.result;
        setPortalCategories({ live: live || [], vod: vod || [], series: series || [] });
        
        const sel = p.selected_categories || {};
        if (sel.live === undefined || sel.live === null) {
          setSelectedLiveCats((live || []).map(g => g.id));
        }
        if (sel.vod === undefined || sel.vod === null) {
          setSelectedVodCats((vod || []).map(c => c.id));
        }
        if (sel.series === undefined || sel.series === null) {
          setSelectedSeriesCats((series || []).map(s => s.id));
        }
      } else {
        showNotification({
          title: 'Failed to Fetch Categories',
          message: resp?.result?.message || resp?.error || 'Portal connection failed.',
          color: 'red',
        });
        setCategoriesModalOpen(false);
      }
    } catch (e) {
      showNotification({
        title: 'Error Fetching Categories',
        message: e?.message || String(e),
        color: 'red',
      });
      setCategoriesModalOpen(false);
    } finally {
      setLoadingCategories(false);
    }
  };

  const handleSaveCategories = async () => {
    if (activeCategoriesPortalIdx === null) return;
    
    const updatedList = [...portalsList];
    const p = updatedList[activeCategoriesPortalIdx];
    
    updatedList[activeCategoriesPortalIdx] = {
      ...p,
      selected_categories: {
        live: selectedLiveCats || [],
        vod: selectedVodCats || [],
        series: selectedSeriesCats || [],
      }
    };
    
    const portalsJsonStr = JSON.stringify(updatedList, null, 2);
    const success = await saveFields({ portals_json: portalsJsonStr });
    if (success) {
      setPortalsList(updatedList);
      setCategoriesModalOpen(false);
      showNotification({
        title: 'Categories Saved',
        message: `Category selection for portal '${p.name}' saved successfully.`,
        color: 'green',
      });
    }
  };

  // Portals configuration modification helpers
  const handleOpenAddPortal = () => {
    setEditingPortalIdx(null);
    setPortalNameInput('');
    setPortalUrlInput('');
    setPortalMacInput('');
    setPortalUaInput('Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3');
    setPortalActiveInput(true);
    setPortalModalOpen(true);
  };

  const handleOpenEditPortal = (idx) => {
    const p = portalsList[idx];
    setEditingPortalIdx(idx);
    setPortalNameInput(p.name || '');
    setPortalUrlInput(p.url || '');
    setPortalMacInput(p.mac || '');
    setPortalUaInput(p.user_agent || 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3');
    setPortalActiveInput(p.active !== false);
    setPortalModalOpen(true);
  };

  const handleSavePortal = async () => {
    if (!portalNameInput.trim() || !portalUrlInput.trim() || !portalMacInput.trim()) {
      showNotification({
        title: 'Invalid Fields',
        message: 'Name, URL, and MAC address fields are required.',
        color: 'red',
      });
      return;
    }

    const updatedList = [...portalsList];
    const portalData = {
      name: portalNameInput.trim(),
      url: portalUrlInput.trim(),
      mac: portalMacInput.trim().toUpperCase().replace(/-/g, ':'),
      user_agent: portalUaInput.trim(),
      active: portalActiveInput,
      selected_categories: editingPortalIdx !== null ? portalsList[editingPortalIdx]?.selected_categories : null,
      expiry: editingPortalIdx !== null ? portalsList[editingPortalIdx]?.expiry : null,
      status: editingPortalIdx !== null ? portalsList[editingPortalIdx]?.status : null,
      connections: editingPortalIdx !== null ? portalsList[editingPortalIdx]?.connections : null,
    };

    if (editingPortalIdx !== null) {
      updatedList[editingPortalIdx] = portalData;
    } else {
      updatedList.push(portalData);
    }

    const portalsJsonStr = JSON.stringify(updatedList, null, 2);
    const success = await saveFields({ portals_json: portalsJsonStr });
    if (success) {
      setPortalsList(updatedList);
      setPortalModalOpen(false);
      showNotification({
        title: 'Portal Saved',
        message: `Portal '${portalData.name}' saved and synced with server.`,
        color: 'green',
      });
    }
  };

  const handleDeletePortal = async (idx) => {
    const updatedList = portalsList.filter((_, i) => i !== idx);
    const portalsJsonStr = JSON.stringify(updatedList, null, 2);
    const success = await saveFields({ portals_json: portalsJsonStr });
    if (success) {
      setPortalsList(updatedList);
      showNotification({
        title: 'Portal Deleted',
        message: 'Portal config deleted successfully.',
        color: 'green',
      });
    }
  };

  const handleTogglePortalActive = async (idx, val) => {
    const updatedList = portalsList.map((p, i) => i === idx ? { ...p, active: val } : p);
    const portalsJsonStr = JSON.stringify(updatedList, null, 2);
    const success = await saveFields({ portals_json: portalsJsonStr });
    if (success) {
      setPortalsList(updatedList);
    }
  };

  // Detective target helper
  const detectiveHistoryList = useMemo(() => {
    const history = settings.detective_history || {};
    return Object.keys(history).map((url) => ({
      url,
      ...history[url],
    })).sort((a, b) => b.timestamp.localeCompare(a.timestamp));
  }, [settings.detective_history]);

  if (loadingPlugins && !plugin) {
    return (
      <AppShellMain p={16}>
        <Stack align="center" justify="center" h="60vh">
          <Loader size="md" />
          <Text size="sm" c="dimmed">Loading Stalker Portal Toolbox...</Text>
        </Stack>
      </AppShellMain>
    );
  }

  if (!plugin) {
    return (
      <AppShellMain p={16}>
        <Alert color="red" title="Plugin Not Found" icon={<AlertTriangle size={18} />}>
          The backend plugin <code>stalker_toolbox</code> or <code>stalker_toolbox_hardcoded</code> is not installed in Dispatcharr. Please drop the plugin folder into the plugins directory and reload plugins from the Plugins configuration page.
        </Alert>
      </AppShellMain>
    );
  }

  return (
    <AppShellMain p={16}>
      <Group justify="space-between" mb="md" align="center">
        <Stack gap={2}>
          <Group gap="xs">
            <Terminal size={22} color="#F59E0B" />
            <Text fw={700} size="lg">Stalker Portal Toolbox</Text>
            <Badge color="violet" variant="light">v{plugin.version}</Badge>
            {!enabled && <Badge color="red">Disabled</Badge>}
            {enabled && <Badge color="green">Active</Badge>}
          </Group>
          <Text size="xs" c="dimmed">
            Manage multi-portal handshakes, perform forensic detective tests, check SOCKS5 proxies, and scan MAC ranges.
          </Text>
        </Stack>

        {!enabled && (
          <Button size="xs" color="green" leftSection={<Check size={14} />} onClick={handleEnablePlugin}>
            Enable Plugin Now
          </Button>
        )}
      </Group>

      {!enabled ? (
        <Alert color="orange" title="Plugin is currently Disabled" icon={<AlertTriangle size={18} />} mb="md">
          To access the full toolbox options, please enable the plugin using the button above or toggle it on the My Plugins page.
        </Alert>
      ) : (
        <Grid>
          <Grid.Col span={{ base: 12, xl: 9 }}>
            <Tabs defaultValue="portals" variant="outline">
              <Tabs.List mb="md">
                <Tabs.Tab value="portals" leftSection={<Globe size={14} />}>Portals Config</Tabs.Tab>
                <Tabs.Tab value="detective" leftSection={<Search size={14} />}>Portal Detective</Tabs.Tab>
                <Tabs.Tab value="generator" leftSection={<Sliders size={14} />}>MAC Generator</Tabs.Tab>
                <Tabs.Tab value="scanner" leftSection={<Activity size={14} />}>MAC Range Scanner</Tabs.Tab>
                <Tabs.Tab value="proxies" leftSection={<Shield size={14} />}>Proxy Pool</Tabs.Tab>
              </Tabs.List>

              {/* SECTION 1: PORTALS MANAGER */}
              <Tabs.Panel value="portals">
                <Stack gap="md">
                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Group justify="space-between" mb="sm">
                      <Text fw={600} size="sm">Configured Portals</Text>
                      <Group gap="xs">
                        {portalsList.some(p => p.status?.includes('Failed')) && (
                          <Button size="xs" color="red" variant="light" onClick={() => executeAction('prune_offline_portals')} loading={actionRunning === 'prune_offline_portals'}>
                            Prune Offline
                          </Button>
                        )}
                        <Button size="xs" variant="light" leftSection={<Plus size={14} />} onClick={handleOpenAddPortal}>
                          Add Portal
                        </Button>
                      </Group>
                    </Group>

                    {portalsList.length === 0 ? (
                      <Text size="sm" c="dimmed" py="md" align="center">
                        No portals configured. Click Add Portal or use the Bulk Import Paste Bin.
                      </Text>
                    ) : (
                      <Table highlightOnHover verticalSpacing="xs">
                        <Table.Thead>
                          <Table.Tr>
                            <Table.Th style={{ width: 120 }}>Name</Table.Th>
                            <Table.Th>Portal URL</Table.Th>
                            <Table.Th>MAC Address</Table.Th>
                            <Table.Th style={{ width: 160 }}>Expiry / Status</Table.Th>
                            <Table.Th style={{ width: 100 }}>Connections</Table.Th>
                            <Table.Th style={{ width: 80, textAlign: 'center' }}>Active</Table.Th>
                            <Table.Th style={{ width: 100, textAlign: 'right' }}>Actions</Table.Th>
                          </Table.Tr>
                        </Table.Thead>
                        <Table.Tbody>
                          {portalsList.map((p, idx) => (
                            <Table.Tr key={idx} style={{ opacity: p.active !== false ? 1 : 0.5 }}>
                              <Table.Td><Text fw={500} size="sm">{p.name}</Text></Table.Td>
                              <Table.Td><Text size="xs" truncate>{p.url}</Text></Table.Td>
                              <Table.Td><code>{p.mac}</code></Table.Td>
                              <Table.Td>
                                {p.expiry ? (
                                  <Stack gap={2}>
                                    <Text size="xs" fw={500} c={p.expiry.toLowerCase().includes('expire') || p.expiry.toLowerCase().includes('limit') ? 'dimmed' : 'teal'}>
                                      {p.expiry}
                                    </Text>
                                    {p.status && (
                                      <Badge size="xxs" color={p.status === 'Active' ? 'green' : p.status.includes('Failed') ? 'red' : 'orange'} variant="light">
                                        {p.status}
                                      </Badge>
                                    )}
                                  </Stack>
                                ) : (
                                  <Text size="xs" c="dimmed">Not Tested</Text>
                                )}
                              </Table.Td>
                              <Table.Td>
                                <Text size="xs" fontStyle="monospace">
                                  {p.connections || '-'}
                                </Text>
                              </Table.Td>
                              <Table.Td align="center">
                                <Switch
                                  size="xs"
                                  checked={p.active !== false}
                                  onChange={(e) => handleTogglePortalActive(idx, e.currentTarget.checked)}
                                />
                              </Table.Td>
                              <Table.Td align="right">
                                <Group gap={6} justify="flex-end">
                                  <ActionIcon size="sm" variant="subtle" color="violet" onClick={() => handleOpenManageCategories(idx)} title="Manage Categories">
                                    <Sliders size={12} />
                                  </ActionIcon>
                                  <ActionIcon size="sm" variant="subtle" color="blue" onClick={() => handleOpenEditPortal(idx)}>
                                    <Edit2 size={12} />
                                  </ActionIcon>
                                  <ActionIcon size="sm" variant="subtle" color="red" onClick={() => handleDeletePortal(idx)}>
                                    <Trash2 size={12} />
                                  </ActionIcon>
                                </Group>
                              </Table.Td>
                            </Table.Tr>
                          ))}
                        </Table.Tbody>
                      </Table>
                    )}
                  </Card>

                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Text fw={600} size="sm" mb="xs">Playlist Sync Options</Text>
                    <Text size="xs" c="dimmed" mb="sm">
                      Configure which content categories to synchronize from your active Stalker portals and define category fetching limits.
                    </Text>
                    <Stack gap="md">
                      <Grid>
                        <Grid.Col span={{ base: 12, md: 4 }}>
                          <Switch
                            label="Sync Live TV"
                            checked={syncLive}
                            onChange={(e) => setSyncLive(e.currentTarget.checked)}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, md: 4 }}>
                          <Switch
                            label="Sync VOD (Movies)"
                            checked={syncVod}
                            onChange={(e) => setSyncVod(e.currentTarget.checked)}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, md: 4 }}>
                          <Switch
                            label="Sync Series (TV Shows)"
                            checked={syncSeries}
                            onChange={(e) => setSyncSeries(e.currentTarget.checked)}
                          />
                        </Grid.Col>
                      </Grid>

                      <Grid>
                        <Grid.Col span={{ base: 12, sm: 6 }}>
                          <NumberInput
                            label="Max VOD Items per Category"
                            description="Limits fetched movies per category (0 for unlimited)"
                            value={syncVodLimit}
                            onChange={(val) => setSyncVodLimit(Number(val))}
                            min={0}
                            disabled={!syncVod}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, sm: 6 }}>
                          <NumberInput
                            label="Max Series per Category"
                            description="Limits fetched series per category (0 for unlimited)"
                            value={syncSeriesLimit}
                            onChange={(val) => setSyncSeriesLimit(Number(val))}
                            min={0}
                            disabled={!syncSeries}
                          />
                        </Grid.Col>
                      </Grid>
                      <Group justify="flex-end">
                        <Button
                          size="xs"
                          variant="light"
                          loading={saving}
                          onClick={async () => {
                            const saved = await saveFields({
                              sync_live: syncLive,
                              sync_vod: syncVod,
                              sync_series: syncSeries,
                              sync_vod_limit: syncVodLimit,
                              sync_series_limit: syncSeriesLimit,
                            });
                            if (saved) {
                              showNotification({
                                title: 'Settings Saved',
                                message: 'Playlist synchronization settings saved successfully.',
                                color: 'green',
                              });
                            }
                          }}
                        >
                          Save Sync Settings
                        </Button>
                      </Group>
                    </Stack>
                  </Card>

                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Text fw={600} size="sm" mb="xs">Bulk Import Combos</Text>
                    <Text size="xs" c="dimmed" mb="sm">
                      Paste a list of URL and MAC combinations (supports raw forum scrapings containing decoration signs, separator tags, emojis, and labels).
                    </Text>
                    <Textarea
                      placeholder="PORTAL: http://example.com:8080&#10;MAC: 00:1a:79:00:11:22&#10;&#10;Portal: http://test.net/c/&#10;Mac: 00:1A:79:AA:BB:CC"
                      minRows={4}
                      value={bulkImportText}
                      onChange={(e) => setBulkImportText(e.currentTarget.value)}
                      styles={{ input: { fontFamily: 'monospace', fontSize: '12px', backgroundColor: '#18181B' } }}
                      mb="sm"
                    />
                    <Group justify="flex-end">
                      <Button
                        size="xs"
                        variant="filled"
                        color="violet"
                        loading={actionRunning === 'bulk_import_portals'}
                        disabled={actionRunning !== null || !bulkImportText.trim()}
                        onClick={() => executeAction('bulk_import_portals', { bulk_import_text: bulkImportText })}
                      >
                        Run Bulk Import
                      </Button>
                    </Group>
                  </Card>

                  <Group gap="sm">
                    <Button
                      size="sm"
                      variant="outline"
                      color="green"
                      leftSection={<RefreshCw size={14} />}
                      loading={actionRunning === 'test_connections'}
                      disabled={actionRunning !== null || portalsList.length === 0}
                      onClick={() => executeAction('test_connections')}
                    >
                      Test Portal Handshakes
                    </Button>
                    <Button
                      size="sm"
                      variant="filled"
                      color="blue"
                      leftSection={<Play size={14} />}
                      loading={actionRunning === 'sync_channels'}
                      disabled={actionRunning !== null || portalsList.length === 0}
                      onClick={() => executeAction('sync_channels', {
                        sync_live: syncLive,
                        sync_vod: syncVod,
                        sync_series: syncSeries,
                        sync_vod_limit: syncVodLimit,
                        sync_series_limit: syncSeriesLimit,
                      })}
                    >
                      Sync Active Playlists
                    </Button>
                  </Group>
                </Stack>
              </Tabs.Panel>

              {/* SECTION 2: PORTAL DETECTIVE */}
              <Tabs.Panel value="detective">
                <Stack gap="md">
                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Text fw={600} size="sm" mb="sm">Run Forensic Target Scan</Text>
                    <Grid align="flex-end">
                      <Grid.Col span={{ base: 12, md: 6 }}>
                        <TextInput
                          label="Detective Target URL"
                          placeholder="http://stalker-server.net:8080"
                          value={detectiveUrl}
                          onChange={(e) => setDetectiveUrl(e.currentTarget.value)}
                        />
                      </Grid.Col>
                      <Grid.Col span={{ base: 12, md: 6 }}>
                        <TextInput
                          label="urlscan.io API Key (Optional)"
                          placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                          value={detectiveUrlscanKey}
                          onChange={(e) => setDetectiveUrlscanKey(e.currentTarget.value)}
                        />
                      </Grid.Col>
                      <Grid.Col span={{ base: 6, md: 4 }}>
                        <Switch
                          label="Enumerate Subdomains"
                          checked={detectiveScanSubdomains}
                          onChange={(e) => setDetectiveScanSubdomains(e.currentTarget.checked)}
                        />
                      </Grid.Col>
                      <Grid.Col span={{ base: 6, md: 4 }}>
                        <Switch
                          label="Port Scan Server"
                          checked={detectiveScanPorts}
                          onChange={(e) => setDetectiveScanPorts(e.currentTarget.checked)}
                        />
                      </Grid.Col>
                      <Grid.Col span={{ base: 12, md: 4 }}>
                        <Group justify="flex-end">
                          <Button
                            size="xs"
                            color="indigo"
                            loading={actionRunning === 'run_detective'}
                            disabled={actionRunning !== null || !detectiveUrl.trim()}
                            onClick={() => executeAction('run_detective', {
                              detective_url: detectiveUrl,
                              detective_urlscan_key: detectiveUrlscanKey,
                              detective_scan_subdomains: detectiveScanSubdomains,
                              detective_scan_ports: detectiveScanPorts,
                            })}
                          >
                            Investigate Target
                          </Button>
                        </Group>
                      </Grid.Col>
                    </Grid>
                  </Card>

                  {/* Detective History */}
                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Group gap="xs" mb="sm">
                      <History size={16} />
                      <Text fw={600} size="sm">Investigation History ({detectiveHistoryList.length})</Text>
                    </Group>

                    {detectiveHistoryList.length === 0 ? (
                      <Text size="sm" c="dimmed" align="center" py="md">
                        No targets investigated yet. Results will be saved here dynamically.
                      </Text>
                    ) : (
                      <Accordion variant="separated">
                        {detectiveHistoryList.map((item, idx) => (
                          <Accordion.Item key={idx} value={item.url} style={{ backgroundColor: '#18181B' }}>
                            <Accordion.Control>
                              <Group justify="space-between" wrap="nowrap">
                                <Stack gap={1} style={{ minWidth: 0 }}>
                                  <Text size="sm" fw={600} truncate>{item.url}</Text>
                                  <Text size="xs" c="dimmed">Scanned: {item.timestamp}</Text>
                                </Stack>
                                <Group gap={6} style={{ flexShrink: 0 }}>
                                  {item.status_code === 200 ? (
                                    <Badge size="xs" color="green">HTTP 200</Badge>
                                  ) : (
                                    <Badge size="xs" color="orange">HTTP {item.status_code || 'N/A'}</Badge>
                                  )}
                                  {item.ssl_valid === 'Yes' ? (
                                    <Badge size="xs" color="teal">SSL Ok</Badge>
                                  ) : (
                                    <Badge size="xs" color="red">No SSL</Badge>
                                  )}
                                </Group>
                              </Group>
                            </Accordion.Control>
                            <Accordion.Panel>
                              <Stack gap="md" pt="xs">
                                <Grid>
                                  <Grid.Col span={{ base: 12, md: 6 }}>
                                    <Card withBorder p="xs" style={{ backgroundColor: '#1E1E24' }}>
                                      <Text size="xs" fw={700} c="dimmed" mb={4}>SERVER INFO</Text>
                                      <Text size="sm"><b>IP Address:</b> {item.ip_address || 'Unknown'}</Text>
                                      <Text size="sm"><b>Reverse DNS:</b> {item.reverse_dns || 'N/A'}</Text>
                                      <Text size="sm"><b>Software Banner:</b> {item.server_banner || 'Unknown'}</Text>
                                      <Text size="sm"><b>WAF Protections:</b> {item.protections || 'None detected'}</Text>
                                    </Card>
                                  </Grid.Col>
                                  <Grid.Col span={{ base: 12, md: 6 }}>
                                    <Card withBorder p="xs" style={{ backgroundColor: '#1E1E24' }}>
                                      <Text size="xs" fw={700} c="dimmed" mb={4}>OPEN PORTS</Text>
                                      {item.open_ports && Object.keys(item.open_ports).length > 0 ? (
                                        Object.keys(item.open_ports).map((port) => (
                                          <Text size="xs" key={port}>
                                            <b>Port {port}:</b> {item.open_ports[port]}
                                          </Text>
                                        ))
                                      ) : (
                                        <Text size="xs" c="dimmed">No open ports scanning logged.</Text>
                                      )}
                                    </Card>
                                  </Grid.Col>
                                </Grid>

                                <Divider label="STB FINGERPRINT LOGINS (00:1A:79:AB:CD:EF)" labelPosition="center" />
                                <SimpleGrid cols={{ base: 2, sm: 3 }} spacing="xs">
                                  {item.stb_fingerprints && item.stb_fingerprints.map((model, mIdx) => {
                                    const parts = model.split(' -> ');
                                    const name = parts[0];
                                    const status = parts[1] || '';
                                    const works = status.includes('Authorization succeeded') || status.includes('Profile returned') || status.includes('success');
                                    return (
                                      <Card withBorder p="xs" key={mIdx} style={{ backgroundColor: works ? '#1A3624' : '#1E1E24', borderColor: works ? 'green' : undefined }}>
                                        <Text size="xs" fw={700}>{name}</Text>
                                        <Text size="xxs" truncate c={works ? 'green' : 'dimmed'}>{status}</Text>
                                      </Card>
                                    );
                                  })}
                                </SimpleGrid>

                                {item.subdomains && item.subdomains.length > 0 && (
                                  <>
                                    <Divider label="RESOLVED SUBDOMAINS" labelPosition="center" />
                                    <List size="xs" spacing={2}>
                                      {item.subdomains.map((sub, sIdx) => (
                                        <List.Item key={sIdx}><code>{sub}</code></List.Item>
                                      ))}
                                    </List>
                                  </>
                                )}

                                {item.admin_probes && item.admin_probes.length > 0 && (
                                  <>
                                    <Divider label="ADMIN ENDPOINT PROBES" labelPosition="center" />
                                    <List size="xs" spacing={2}>
                                      {item.admin_probes.map((probe, pIdx) => (
                                        <List.Item key={pIdx}><code>{probe}</code></List.Item>
                                      ))}
                                    </List>
                                  </>
                                )}

                                {item.co_hosted_portals && item.co_hosted_portals.length > 0 && (
                                  <>
                                    <Divider label="CO-HOSTED PANELS (urlscan.io)" labelPosition="center" />
                                    <List size="xs" spacing={2}>
                                      {item.co_hosted_portals.map((co, cIdx) => (
                                        <List.Item key={cIdx}>
                                          <Group gap={4}>
                                            <ExternalLink size={10} />
                                            <Text size="xs" component="a" href={co} target="_blank" c="blue">{co}</Text>
                                          </Group>
                                        </List.Item>
                                      ))}
                                    </List>
                                  </>
                                )}
                              </Stack>
                            </Accordion.Panel>
                          </Accordion.Item>
                        ))}
                      </Accordion>
                    )}
                  </Card>
                </Stack>
              </Tabs.Panel>

              {/* SECTION 3: MAC GENERATOR */}
              <Tabs.Panel value="generator">
                <Stack gap="md">
                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Text fw={600} size="sm" mb="xs">Generator Settings</Text>
                    <Text size="xs" c="dimmed" mb="md">
                      Choose which MAC prefixes to use. You can select multiple predefined MAG/IPTV vendor prefixes and/or add your own custom ones. The total combinations will be divided evenly among all active prefixes.
                    </Text>

                    <Stack gap="md">
                      <div>
                        <Group justify="space-between" mb="xs">
                          <Text size="xs" fw={700} c="dimmed">KNOWN MAC PREFIXES</Text>
                          <Group gap="xs">
                            <Button size="xxs" variant="subtle" onClick={handleSelectAllPrefixes}>Select All</Button>
                            <Button size="xxs" variant="subtle" color="red" onClick={handleDeselectAllPrefixes}>Deselect All</Button>
                          </Group>
                        </Group>
                        <Card withBorder p="xs" style={{ backgroundColor: '#18181B', maxHeight: 220, overflowY: 'auto' }}>
                          <SimpleGrid cols={{ base: 1, sm: 2, md: 3, lg: 4 }} spacing="xs">
                            {KNOWN_PREFIXES.map((kp) => (
                              <Checkbox
                                key={kp.value}
                                label={kp.label}
                                checked={selectedPrefixes.includes(kp.value)}
                                onChange={(e) => handlePrefixCheckboxChange(kp.value, e.currentTarget.checked)}
                              />
                            ))}
                          </SimpleGrid>
                        </Card>
                      </div>

                      <Grid align="flex-end">
                        <Grid.Col span={{ base: 12, md: 6 }}>
                          <TextInput
                            label="Custom MAC Prefixes"
                            placeholder="e.g. 00:1A:7C:, 74:1A:78:"
                            description="Optional, separate multiple prefixes with commas"
                            value={customPrefixes}
                            onChange={(e) => handleCustomPrefixChange(e.currentTarget.value)}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, md: 6 }}>
                          <NumberInput
                            label="Total MAC Count"
                            description="Number of total combinations generated in the output file"
                            value={genCount}
                            onChange={(val) => setGenCount(Number(val))}
                            min={1}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, md: 4 }}>
                          <Select
                            label="Generation Mode"
                            data={[
                              { value: 'random', label: 'Random Suffix' },
                              { value: 'ascending', label: 'Sequential Ascending' },
                              { value: 'descending', label: 'Sequential Descending' },
                            ]}
                            value={genMode}
                            onChange={(val) => setGenMode(val || 'random')}
                            allowDeselect={false}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 6, md: 4 }}>
                          <TextInput
                            label="Suffix Start (Optional)"
                            placeholder="e.g. 00:00:00"
                            value={genSuffixStart}
                            onChange={(e) => setGenSuffixStart(e.currentTarget.value)}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 6, md: 4 }}>
                          <TextInput
                            label="Suffix Finish (Optional)"
                            placeholder="e.g. FF:FF:FF"
                            value={genSuffixEnd}
                            onChange={(e) => setGenSuffixEnd(e.currentTarget.value)}
                          />
                        </Grid.Col>
                        <Grid.Col span={{ base: 12 }}>
                          <TextInput
                            label="Output Filename"
                            description="File will be written under /data/ folder."
                            value={genFilename}
                            onChange={(e) => setGenFilename(e.currentTarget.value)}
                          />
                        </Grid.Col>
                      </Grid>
                    </Stack>

                    <Group justify="flex-end" mt="md">
                      <Button
                        size="xs"
                        color="teal"
                        loading={actionRunning === 'run_generator'}
                        disabled={actionRunning !== null || (!selectedPrefixes.length && !customPrefixes.trim())}
                        onClick={() => executeAction('run_generator', {
                          gen_prefixes: genPrefixes,
                          gen_count: genCount,
                          gen_mode: genMode,
                          gen_suffix_start: genSuffixStart,
                          gen_suffix_end: genSuffixEnd,
                          gen_filename: genFilename,
                        })}
                      >
                        Generate MAC List
                      </Button>
                    </Group>
                  </Card>
                </Stack>
              </Tabs.Panel>

              {/* SECTION 4: RANGE SCANNER */}
              <Tabs.Panel value="scanner">
                <Stack gap="md">
                  <Grid>
                    <Grid.Col span={{ base: 12, md: 5 }}>
                      <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                        <Text fw={600} size="sm" mb="sm">Scan Configuration</Text>
                        <Stack gap="sm">
                          <Select
                            label="Scan Target Portal"
                            placeholder="Select portal configuration"
                            data={portalsList.map((p) => ({ value: p.name, label: `${p.name} (${p.url})` }))}
                            value={scanPortal}
                            onChange={(val) => setScanPortal(val || '')}
                            disabled={scanStatus.running}
                          />
                          <TextInput
                            label="Scan MAC Start"
                            value={scanMacStart}
                            onChange={(e) => setScanMacStart(e.currentTarget.value)}
                            disabled={scanStatus.running}
                          />
                          <TextInput
                            label="Scan MAC End"
                            value={scanMacEnd}
                            onChange={(e) => setScanMacEnd(e.currentTarget.value)}
                            disabled={scanStatus.running}
                          />
                          <Grid>
                            <Grid.Col span={6}>
                              <NumberInput
                                label="Threads"
                                value={scanThreads}
                                onChange={(val) => setScanThreads(Number(val))}
                                min={1}
                                max={15}
                                disabled={scanStatus.running}
                              />
                            </Grid.Col>
                            <Grid.Col span={6}>
                              <NumberInput
                                label="Cooldown (s)"
                                value={scanCooldown}
                                onChange={(val) => setScanCooldown(Number(val))}
                                min={0}
                                step={0.1}
                                disabled={scanStatus.running}
                              />
                            </Grid.Col>
                          </Grid>

                          <Group justify="flex-end" mt="sm">
                            {scanStatus.running ? (
                              <Button
                                size="xs"
                                color="red"
                                leftSection={<Square size={14} />}
                                onClick={async () => {
                                  // Call stop_plugin and then discover_plugins to shut scan down
                                  await API.runPluginAction(pluginKey, 'stop_plugin');
                                  showNotification({ title: 'Stopping Scanner', message: 'Scan stop request sent to server.', color: 'orange' });
                                  setTimeout(fetchScanStatus, 1500);
                                }}
                              >
                                Stop Range Scan
                              </Button>
                            ) : (
                              <Button
                                size="xs"
                                color="orange"
                                leftSection={<Play size={14} />}
                                disabled={!scanPortal || !scanMacStart || !scanMacEnd}
                                onClick={() => executeAction('scan_macs', {
                                  scan_portal: scanPortal,
                                  scan_mac_start: scanMacStart,
                                  scan_mac_end: scanMacEnd,
                                  scan_threads: scanThreads,
                                  scan_cooldown: scanCooldown,
                                })}
                              >
                                Start Range Scan
                              </Button>
                            )}
                          </Group>
                        </Stack>
                      </Card>
                    </Grid.Col>

                    <Grid.Col span={{ base: 12, md: 7 }}>
                      <Card withBorder style={{ backgroundColor: '#1E1E24', height: '100%' }}>
                        <Group justify="space-between" mb="xs">
                          <Text fw={600} size="sm">Scanner Activity</Text>
                          {scanStatus.running ? (
                            <Badge color="orange" variant="light">Running</Badge>
                          ) : (
                            <Badge color="gray">Idle</Badge>
                          )}
                        </Group>

                        {scanStatus.running && (
                          <Stack gap="xs" mb="md">
                            <Group justify="space-between">
                              <Text size="xs" c="dimmed">Progress: {scanStatus.checked} / {scanStatus.total} MACs</Text>
                              <Text size="xs" fw={700} c="green">{scanStatus.active_found} Active Found</Text>
                            </Group>
                            <Progress
                              value={scanStatus.total > 0 ? (scanStatus.checked / scanStatus.total) * 100 : 0}
                              color="orange"
                              animated
                            />
                            <Text size="xs"><b>Current MAC probed:</b> <code>{scanStatus.current_mac || 'N/A'}</code></Text>
                          </Stack>
                        )}

                        <Text size="xs" fw={700} mb={6} c="dimmed">ACTIVE SUBSCRIPTIONS DISCOVERED ({scanStatus.results?.length || 0})</Text>
                        <Card withBorder p="xs" style={{ backgroundColor: '#18181B', flex: 1, overflowY: 'auto', maxHeight: 220 }}>
                          {(!scanStatus.results || scanStatus.results.length === 0) ? (
                            <Text size="xs" c="dimmed" align="center" py="xl">
                              No active subscriptions found yet. Details are appended to `/data/stalker_scan_results.txt`.
                            </Text>
                          ) : (
                            <List size="xs" spacing={3}>
                              {scanStatus.results.map((line, rIdx) => (
                                <List.Item key={rIdx} icon={
                                  <ThemeIcon color="green" size={14} radius="xl">
                                    <Check size={10} />
                                  </ThemeIcon>
                                }>
                                  <code>{line}</code>
                                </List.Item>
                              ))}
                            </List>
                          )}
                        </Card>
                      </Card>
                    </Grid.Col>
                  </Grid>
                </Stack>
              </Tabs.Panel>

              {/* SECTION 5: PROXY POOL */}
              <Tabs.Panel value="proxies">
                <Stack gap="md">
                  <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                    <Text fw={600} size="sm" mb="xs">Proxies List (Paste Bin)</Text>
                    <Text size="xs" c="dimmed" mb="sm">
                      Enter proxies one per line. Schemes supported: <code>socks5h://</code>, <code>socks5://</code>, <code>socks4://</code>, <code>http://</code>, <code>https://</code>. Omitted schemes default to socks5h.
                    </Text>
                    <Textarea
                      placeholder="socks5h://user:password@proxy.com:1080&#10;192.168.1.100:8080&#10;http://12.34.56.78:3128"
                      minRows={5}
                      value={proxiesPaste}
                      onChange={(e) => setProxiesPaste(e.currentTarget.value)}
                      styles={{ input: { fontFamily: 'monospace', fontSize: '12px', backgroundColor: '#18181B' } }}
                      mb="sm"
                    />

                    <Text fw={600} size="sm" mb="xs">Proxy list URLs (e.g. GitHub)</Text>
                    <Text size="xs" c="dimmed" mb="sm">
                      Links to raw text files containing proxy addresses (one URL per line). The pool fetches, dedups, and caches these lists for 5 minutes.
                    </Text>
                    <Textarea
                      placeholder="https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
                      minRows={2}
                      value={proxyUrls}
                      onChange={(e) => setProxyUrls(e.currentTarget.value)}
                      styles={{ input: { fontFamily: 'monospace', fontSize: '12px', backgroundColor: '#18181B' } }}
                      mb="md"
                    />

                    <Group justify="flex-end">
                      <Button
                        size="xs"
                        loading={saving}
                        onClick={async () => {
                          const saved = await saveFields({ proxies_paste: proxiesPaste, proxy_urls: proxyUrls });
                          if (saved) {
                            showNotification({
                              title: 'Proxies Saved',
                              message: 'Proxies configuration saved. Ready to route connections.',
                              color: 'green',
                            });
                          }
                        }}
                      >
                        Save Proxy Config
                      </Button>
                    </Group>
                  </Card>
                </Stack>
              </Tabs.Panel>
            </Tabs>
          </Grid.Col>

          {/* RIGHT SIDEBAR: OPERATION LOGS */}
          <Grid.Col span={{ base: 12, xl: 3 }}>
            <Stack gap="md" style={{ height: '100%' }}>
              <Card withBorder style={{ backgroundColor: '#1E1E24', display: 'flex', flexDirection: 'column', height: '100%', minHeight: 300 }}>
                <Group justify="space-between" mb="xs" style={{ flexShrink: 0 }}>
                  <Text fw={600} size="sm">Execution Logs</Text>
                  <ActionIcon size="sm" variant="subtle" onClick={() => setLogOutput('')} title="Clear Logs">
                    <Trash2 size={12} />
                  </ActionIcon>
                </Group>
                <div style={{ flex: 1, position: 'relative' }}>
                  <pre
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      bottom: 0,
                      margin: 0,
                      padding: '8px',
                      backgroundColor: '#18181B',
                      color: '#10B981',
                      fontFamily: 'monospace',
                      fontSize: '11px',
                      overflowY: 'auto',
                      whiteSpace: 'pre-wrap',
                      borderRadius: '4px',
                      border: '1px solid #27272A',
                    }}
                  >
                    {logOutput || 'No active jobs running.'}
                  </pre>
                </div>
              </Card>

              <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                <Text fw={600} size="sm" mb="xs">Handshake Proxy status</Text>
                <Text size="xs" c="dimmed" mb="xs">
                  Proxy server intercepts M3U player streams on port: <b>{settings.proxy_port || 8282}</b>
                </Text>
                <Divider my="sm" />
                <Grid>
                  <Grid.Col span={8}>
                    <TextInput
                      label="Proxy Port"
                      value={settings.proxy_port || 8282}
                      onChange={(e) => saveFields({ proxy_port: Number(e.currentTarget.value) })}
                      size="xs"
                    />
                  </Grid.Col>
                  <Grid.Col span={4} style={{ display: 'flex', alignItems: 'flex-end' }}>
                    <Badge color="teal" size="lg" style={{ height: '30px', width: '100%' }}>ONLINE</Badge>
                  </Grid.Col>
                </Grid>
              </Card>
            </Stack>
          </Grid.Col>
        </Grid>
      )}

      {/* Portal Edit/Add Modal */}
      <Modal
        opened={portalModalOpen}
        onClose={() => setPortalModalOpen(false)}
        title={editingPortalIdx !== null ? 'Edit Stalker Portal' : 'Add Stalker Portal'}
        size="md"
      >
        <Stack gap="sm">
          <TextInput
            label="Portal Name"
            placeholder="e.g. portal_fast"
            value={portalNameInput}
            onChange={(e) => setPortalNameInput(e.currentTarget.value)}
            required
          />
          <TextInput
            label="Portal URL"
            placeholder="http://stalker-panel.xyz:8080"
            value={portalUrlInput}
            onChange={(e) => setPortalUrlInput(e.currentTarget.value)}
            required
          />
          <TextInput
            label="STB MAC Address"
            placeholder="00:1A:79:XX:XX:XX"
            value={portalMacInput}
            onChange={(e) => setPortalMacInput(e.currentTarget.value)}
            required
          />
          <TextInput
            label="Custom User-Agent"
            value={portalUaInput}
            onChange={(e) => setPortalUaInput(e.currentTarget.value)}
          />
          <Switch
            label="Active Portal (Included in handshake tests and syncs)"
            checked={portalActiveInput}
            onChange={(e) => setPortalActiveInput(e.currentTarget.checked)}
            mt="xs"
          />
          <Group justify="flex-end" mt="md">
            <Button size="xs" variant="default" onClick={() => setPortalModalOpen(false)}>
              Cancel
            </Button>
            <Button size="xs" onClick={handleSavePortal} loading={saving}>
              Save Config
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* Manage Categories Modal */}
      <Modal
        opened={categoriesModalOpen}
        onClose={() => setCategoriesModalOpen(false)}
        title={activeCategoriesPortalIdx !== null ? `Manage Categories - ${portalsList[activeCategoriesPortalIdx]?.name}` : 'Manage Categories'}
        size="lg"
      >
        {loadingCategories ? (
          <Stack align="center" justify="center" py="xl">
            <Loader size="md" />
            <Text size="sm" c="dimmed">Connecting to portal and fetching categories list...</Text>
          </Stack>
        ) : (
          <Stack gap="md">
            <Text size="xs" c="dimmed">
              Choose which categories to import during synchronization. Unselected categories will be skipped to keep the import fast.
            </Text>

            <Accordion defaultValue="live" variant="separated">
              {portalCategories.live && portalCategories.live.length > 0 && (
                <Accordion.Item value="live" style={{ backgroundColor: '#18181B' }}>
                  <Accordion.Control>
                    <Group justify="space-between" pr="md">
                      <Text size="sm" fw={600}>Live TV Genres</Text>
                      <Badge color="blue" size="xs">
                        {selectedLiveCats?.length ?? 0} / {portalCategories.live.length} Selected
                      </Badge>
                    </Group>
                  </Accordion.Control>
                  <Accordion.Panel>
                    <Stack gap="sm">
                      <Group gap="xs">
                        <Button size="xxs" variant="subtle" onClick={() => setSelectedLiveCats(portalCategories.live.map(g => g.id))}>Select All</Button>
                        <Button size="xxs" variant="subtle" color="red" onClick={() => setSelectedLiveCats([])}>Deselect All</Button>
                      </Group>
                      <Divider />
                      <div style={{ maxHeight: 220, overflowY: 'auto', padding: '4px' }}>
                        <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="xs">
                          {portalCategories.live.map((g) => (
                            <Checkbox
                              key={g.id}
                              label={g.title}
                              checked={(selectedLiveCats || []).includes(g.id)}
                              onChange={(e) => {
                                if (e.currentTarget.checked) {
                                  setSelectedLiveCats((prev) => [...(prev || []), g.id]);
                                } else {
                                  setSelectedLiveCats((prev) => (prev || []).filter(id => id !== g.id));
                                }
                              }}
                            />
                          ))}
                        </SimpleGrid>
                      </div>
                    </Stack>
                  </Accordion.Panel>
                </Accordion.Item>
              )}

              {portalCategories.vod && portalCategories.vod.length > 0 && (
                <Accordion.Item value="vod" style={{ backgroundColor: '#18181B' }}>
                  <Accordion.Control>
                    <Group justify="space-between" pr="md">
                      <Text size="sm" fw={600}>VOD (Movie) Categories</Text>
                      <Badge color="blue" size="xs">
                        {selectedVodCats?.length ?? 0} / {portalCategories.vod.length} Selected
                      </Badge>
                    </Group>
                  </Accordion.Control>
                  <Accordion.Panel>
                    <Stack gap="sm">
                      <Group gap="xs">
                        <Button size="xxs" variant="subtle" onClick={() => setSelectedVodCats(portalCategories.vod.map(c => c.id))}>Select All</Button>
                        <Button size="xxs" variant="subtle" color="red" onClick={() => setSelectedVodCats([])}>Deselect All</Button>
                      </Group>
                      <Divider />
                      <div style={{ maxHeight: 220, overflowY: 'auto', padding: '4px' }}>
                        <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="xs">
                          {portalCategories.vod.map((c) => (
                            <Checkbox
                              key={c.id}
                              label={c.title}
                              checked={(selectedVodCats || []).includes(c.id)}
                              onChange={(e) => {
                                if (e.currentTarget.checked) {
                                  setSelectedVodCats((prev) => [...(prev || []), c.id]);
                                } else {
                                  setSelectedVodCats((prev) => (prev || []).filter(id => id !== c.id));
                                }
                              }}
                            />
                          ))}
                        </SimpleGrid>
                      </div>
                    </Stack>
                  </Accordion.Panel>
                </Accordion.Item>
              )}

              {portalCategories.series && portalCategories.series.length > 0 && (
                <Accordion.Item value="series" style={{ backgroundColor: '#18181B' }}>
                  <Accordion.Control>
                    <Group justify="space-between" pr="md">
                      <Text size="sm" fw={600}>Series (TV Show) Categories</Text>
                      <Badge color="blue" size="xs">
                        {selectedSeriesCats?.length ?? 0} / {portalCategories.series.length} Selected
                      </Badge>
                    </Group>
                  </Accordion.Control>
                  <Accordion.Panel>
                    <Stack gap="sm">
                      <Group gap="xs">
                        <Button size="xxs" variant="subtle" onClick={() => setSelectedSeriesCats(portalCategories.series.map(s => s.id))}>Select All</Button>
                        <Button size="xxs" variant="subtle" color="red" onClick={() => setSelectedSeriesCats([])}>Deselect All</Button>
                      </Group>
                      <Divider />
                      <div style={{ maxHeight: 220, overflowY: 'auto', padding: '4px' }}>
                        <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="xs">
                          {portalCategories.series.map((s) => (
                            <Checkbox
                              key={s.id}
                              label={s.title}
                              checked={(selectedSeriesCats || []).includes(s.id)}
                              onChange={(e) => {
                                if (e.currentTarget.checked) {
                                  setSelectedSeriesCats((prev) => [...(prev || []), s.id]);
                                } else {
                                  setSelectedSeriesCats((prev) => (prev || []).filter(id => id !== s.id));
                                }
                              }}
                            />
                          ))}
                        </SimpleGrid>
                      </div>
                    </Stack>
                  </Accordion.Panel>
                </Accordion.Item>
              )}
            </Accordion>

            <Group justify="flex-end" mt="md">
              <Button size="xs" variant="default" onClick={() => setCategoriesModalOpen(false)}>
                Cancel
              </Button>
              <Button size="xs" onClick={handleSaveCategories} loading={saving}>
                Save Category Selection
              </Button>
            </Group>
          </Stack>
        )}
      </Modal>
    </AppShellMain>
  );
}
