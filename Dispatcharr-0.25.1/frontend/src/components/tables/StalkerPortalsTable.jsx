import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  Text,
  Badge,
  Group,
  Button,
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
  Loader,
  Divider,
  Checkbox,
  Alert,
} from '@mantine/core';
import {
  Globe,
  Plus,
  Trash2,
  Edit2,
  Sliders,
  RefreshCw,
  Play,
  Check,
  AlertTriangle,
} from 'lucide-react';
import { usePluginStore } from '../../store/plugins.jsx';
import { showNotification } from '../../utils/notificationUtils.js';
import API from '../../api';

export default function StalkerPortalsTable() {
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
  const [portalUaInput, setPortalUaInput] = 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3';
  const [portalActiveInput, setPortalActiveInput] = useState(true);

  // Parse portals list whenever settings load
  useEffect(() => {
    if (settings.portals_json) {
      try {
        const parsed = JSON.parse(settings.portals_json);
        setPortalsList(Array.isArray(parsed) ? parsed : []);
      } catch (e) {
        setPortalsList([]);
      }
    } else {
      setPortalsList([]);
    }
    setBulkImportText(settings.bulk_import_text || '');
    setSyncLive(settings.sync_live !== false);
    setSyncVod(!!settings.sync_vod);
    setSyncSeries(!!settings.sync_series);
    setSyncVodLimit(settings.sync_vod_limit ?? 100);
    setSyncSeriesLimit(settings.sync_series_limit ?? 50);
  }, [settings]);

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

  const handleOpenAddPortal = () => {
    setEditingPortalIdx(null);
    setPortalNameInput('');
    setPortalUrlInput('');
    setPortalMacInput('');
    setPortalActiveInput(true);
    setPortalModalOpen(true);
  };

  const handleOpenEditPortal = (idx) => {
    const p = portalsList[idx];
    setEditingPortalIdx(idx);
    setPortalNameInput(p.name || '');
    setPortalUrlInput(p.url || '');
    setPortalMacInput(p.mac || '');
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
      user_agent: 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
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

  if (loadingPlugins && !plugin) {
    return (
      <Stack align="center" justify="center" h="40vh">
        <Loader size="md" />
        <Text size="sm" c="dimmed">Loading Stalker Portals...</Text>
      </Stack>
    );
  }

  if (!plugin) {
    return (
      <Alert color="red" title="Plugin Not Found" icon={<AlertTriangle size={18} />}>
        The backend plugin <code>stalker_toolbox</code> is not installed or enabled in Dispatcharr. Please enable it in My Plugins.
      </Alert>
    );
  }

  return (
    <Stack gap="md">
      {!enabled ? (
        <Alert color="orange" title="Plugin is currently Disabled" icon={<AlertTriangle size={18} />}>
          To manage Stalker portals, please enable the plugin in My Plugins or click the button below.
          <Group mt="md">
            <Button size="xs" color="green" leftSection={<Check size={14} />} onClick={handleEnablePlugin}>
              Enable Plugin
            </Button>
          </Group>
        </Alert>
      ) : (
        <Grid>
          <Grid.Col span={{ base: 12, xl: 9 }}>
            <Stack gap="md">
              <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                <Group justify="space-between" mb="sm">
                  <Text fw={600} size="sm">Configured Portals</Text>
                  <Group gap="xs">
                    {portalsList.some(p => typeof p.status === 'string' && p.status.includes('Failed')) && (
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
                                <Text size="xs" fw={500} c={(typeof p.expiry === 'string' && (p.expiry.toLowerCase().includes('expire') || p.expiry.toLowerCase().includes('limit'))) ? 'dimmed' : 'teal'}>
                                  {p.expiry}
                                </Text>
                                {p.status && (
                                  <Badge size="xxs" color={p.status === 'Active' ? 'green' : (typeof p.status === 'string' && p.status.includes('Failed')) ? 'red' : 'orange'} variant="light">
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
                  Paste a list of URL and MAC combinations.
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
            </Stack>
          </Grid.Col>

          <Grid.Col span={{ base: 12, xl: 3 }}>
            <Stack gap="md">
              <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                <Text fw={600} size="sm" mb="xs">Handshake Actions</Text>
                <Text size="xs" c="dimmed" mb="sm">
                  Trigger handshakes or synchronization tasks.
                </Text>
                <Stack gap="xs">
                  <Button
                    size="xs"
                    variant="outline"
                    color="green"
                    leftSection={<RefreshCw size={14} />}
                    loading={actionRunning === 'test_connections'}
                    disabled={actionRunning !== null || portalsList.length === 0}
                    onClick={() => executeAction('test_connections')}
                    fullWidth
                  >
                    Test Portal Handshakes
                  </Button>
                  <Button
                    size="xs"
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
                    fullWidth
                  >
                    Sync Active Playlists
                  </Button>
                </Stack>
              </Card>

              <Card withBorder style={{ backgroundColor: '#1E1E24' }}>
                <Text fw={600} size="sm" mb="xs">Active Jobs Log</Text>
                <div style={{ height: '180px', position: 'relative' }}>
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
    </Stack>
  );
}
