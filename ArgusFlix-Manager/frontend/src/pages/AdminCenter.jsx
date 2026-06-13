import React, { useState, useEffect } from 'react';
import { Stack, Title, Group, Tabs, Text, Button, Table, Badge, ActionIcon, ScrollArea, Card, Switch, TextInput, Box, NumberInput } from '@mantine/core';
import { Activity, ShieldAlert, LineChart, Clock, Scissors, Database, Trash, RefreshCw, Save, AlertTriangle } from 'lucide-react';
import { notifications } from '@mantine/notifications';
import API from '../api';

const AdminCenter = () => {
  const [activeTab, setActiveTab] = useState('monitor');
  const [connections, setConnections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [vpnGuardEnabled, setVpnGuardEnabled] = useState(false);
  const [gluetunUrl, setGluetunUrl] = useState('http://gluetun:8000');
  const [vpnStatus, setVpnStatus] = useState('unknown');
  const [auditResults, setAuditResults] = useState([]);
  const [auditing, setAuditing] = useState(false);
  const [epgSources, setEpgSources] = useState([]);
  const [savingOffset, setSavingOffset] = useState({});
  const [clearingCache, setClearingCache] = useState(false);
  const [zombies, setZombies] = useState([]);
  const [scanningZombies, setScanningZombies] = useState(false);
  const [cleaningZombies, setCleaningZombies] = useState(false);

  const fetchVpnSettings = async () => {
    try {
      const settingsResponse = await API.getSettings();
      const settings = settingsResponse?.results || [];
      const vpnSetting = settings.find((s) => s.key === 'vpn_guard');
      if (vpnSetting && vpnSetting.value) {
        setVpnGuardEnabled(vpnSetting.value.enabled || false);
        setGluetunUrl(vpnSetting.value.gluetun_url || 'http://gluetun:8000');
      }
      
      const statusResponse = await API.getVpnStatus();
      setVpnStatus(statusResponse?.status || 'unknown');
    } catch (e) {
      console.error(e);
    }
  };

  const fetchAuditResults = async () => {
    try {
      const data = await API.getProviderAudit();
      setAuditResults(data || []);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchEpgSources = async () => {
    try {
      const response = await API.getEPGs();
      setEpgSources(response?.results || []);
    } catch (e) {
      console.error(e);
    }
  };

  const handleUpdateOffset = async (sourceId, newOffset) => {
    setSavingOffset(prev => ({ ...prev, [sourceId]: true }));
    try {
      await API.updateEPG({ id: sourceId, time_offset_minutes: newOffset });
      notifications.show({ title: 'Success', message: 'Timeshift offset updated', color: 'green' });
      fetchEpgSources();
    } catch (e) {
      console.error(e);
    } finally {
      setSavingOffset(prev => ({ ...prev, [sourceId]: false }));
    }
  };

  const saveVpnSettings = async () => {
    try {
      const settingsResponse = await API.getSettings();
      const settings = settingsResponse?.results || [];
      const vpnSetting = settings.find((s) => s.key === 'vpn_guard');
      
      const newValue = { enabled: vpnGuardEnabled, gluetun_url: gluetunUrl };
      if (vpnSetting) {
        await API.updateSetting(vpnSetting.id, { value: newValue });
      } else {
        await API.createSetting({ key: 'vpn_guard', name: 'VPN Guard Config', value: newValue });
      }
      notifications.show({ title: 'Success', message: 'VPN Guard settings saved', color: 'green' });
    } catch (e) {
      console.error(e);
      notifications.show({ title: 'Error', message: 'Failed to save VPN Guard settings', color: 'red' });
    }
  };

  const fetchConnections = async () => {
    setLoading(true);
    try {
      const data = await API.getActiveConnections();
      setConnections(data || []);
    } catch (e) {
      console.error('Failed to fetch connections:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'monitor') {
      fetchConnections();
    } else if (activeTab === 'vpn') {
      fetchVpnSettings();
    } else if (activeTab === 'auditor') {
      fetchAuditResults();
    } else if (activeTab === 'timeshift') {
      fetchEpgSources();
    } else if (activeTab === 'doctor') {
      handleScanZombies();
    }
  }, [activeTab]);

  const handleScanZombies = async () => {
    setScanningZombies(true);
    try {
      const data = await API.scanProxyZombies();
      setZombies(data?.zombies || []);
    } catch (e) {
      console.error(e);
    } finally {
      setScanningZombies(false);
    }
  };

  const handleCleanZombies = async () => {
    setCleaningZombies(true);
    try {
      const resp = await API.cleanProxyZombies();
      if (resp?.success) {
        notifications.show({ title: 'Success', message: `${resp.cleaned_count} Zombie-Prozesse wurden beendet.`, color: 'green' });
        handleScanZombies();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setCleaningZombies(false);
    }
  };

  const handleClearCache = async () => {
    setClearingCache(true);
    try {
      const resp = await API.clearSystemCache();
      if (resp?.success) {
        notifications.show({ title: 'Cache Cleared', message: 'Der System-Cache wurde erfolgreich geleert.', color: 'green' });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setClearingCache(false);
    }
  };

  const handleTriggerAudit = async () => {
    setAuditing(true);
    try {
      await API.triggerProviderAudit();
      notifications.show({ title: 'Audit Started', message: 'The benchmark is running in the background. Refresh in a moment.', color: 'blue' });
    } catch (e) {
      console.error(e);
    } finally {
      setAuditing(false);
    }
  };

  const handleKillStream = async (clientId) => {
    try {
      await API.killActiveConnection(clientId);
      notifications.show({ title: 'Success', message: 'Stream terminated successfully', color: 'green' });
      fetchConnections();
    } catch (e) {
      console.error('Failed to kill stream:', e);
    }
  };

  return (
    <Stack p="md" h="100%" gap="md">
      <Group justify="space-between" align="center">
        <Group gap="xs">
          <Activity size={24} color="var(--mantine-color-red-filled)" />
          <Title order={2} style={{ fontFamily: 'Outfit, Inter, sans-serif', fontWeight: 600 }}>
            Wartungs-Zentrale
          </Title>
        </Group>
      </Group>

      <Tabs value={activeTab} onChange={setActiveTab} variant="outline" radius="md">
        <Tabs.List>
          <Tabs.Tab value="monitor" leftSection={<Activity size={16} />}>Live-Monitor</Tabs.Tab>
          <Tabs.Tab value="vpn" leftSection={<ShieldAlert size={16} />}>VPN-Guard</Tabs.Tab>
          <Tabs.Tab value="auditor" leftSection={<LineChart size={16} />}>Auditor</Tabs.Tab>
          <Tabs.Tab value="epg" leftSection={<Clock size={16} />}>EPG-Shifter</Tabs.Tab>
          <Tabs.Tab value="slicer" leftSection={<Scissors size={16} />}>Slicer</Tabs.Tab>
          <Tabs.Tab value="sqlite" leftSection={<Database size={16} />}>DB-Optimizer</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="monitor" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Group justify="space-between" mb="md">
              <Text fw={500}>Active Client Connections</Text>
              <Button leftSection={<RefreshCw size={14} />} variant="light" size="xs" onClick={fetchConnections} loading={loading}>
                Refresh
              </Button>
            </Group>
            <ScrollArea>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Client ID</Table.Th>
                    <Table.Th>User ID</Table.Th>
                    <Table.Th>Media ID</Table.Th>
                    <Table.Th>Connected Since</Table.Th>
                    <Table.Th>Actions</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {connections.length === 0 ? (
                    <Table.Tr>
                      <Table.Td colSpan={5} ta="center">No active connections</Table.Td>
                    </Table.Tr>
                  ) : (
                    connections.map((conn) => (
                      <Table.Tr key={conn.client_id}>
                        <Table.Td><Text size="sm" family="monospace">{conn.client_id}</Text></Table.Td>
                        <Table.Td><Badge variant="outline">{conn.user_id}</Badge></Table.Td>
                        <Table.Td>{conn.media_id}</Table.Td>
                        <Table.Td>{new Date(conn.connected_at * 1000).toLocaleString()}</Table.Td>
                        <Table.Td>
                          <ActionIcon color="red" variant="subtle" onClick={() => handleKillStream(conn.client_id)}>
                            <Trash size={16} />
                          </ActionIcon>
                        </Table.Td>
                      </Table.Tr>
                    ))
                  )}
                </Table.Tbody>
              </Table>
            </ScrollArea>
          </Card>
        </Tabs.Panel>

        <Tabs.Panel value="vpn" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Stack gap="md">
              <Group justify="space-between" align="center">
                <Box>
                  <Text fw={500} size="lg">VPN-Guard (Gluetun Kill-Switch)</Text>
                  <Text c="dimmed" size="sm">Stoppt Stream-Proxys sofort, falls der VPN-Tunnel abbricht.</Text>
                </Box>
                <Badge color={vpnStatus === 'up' ? 'green' : vpnStatus === 'down' ? 'red' : 'gray'} variant="light" size="lg">
                  VPN STATUS: {vpnStatus.toUpperCase()}
                </Badge>
              </Group>
              
              <Switch 
                label="VPN-Guard aktivieren" 
                checked={vpnGuardEnabled}
                onChange={(event) => setVpnGuardEnabled(event.currentTarget.checked)}
                size="md"
              />
              
              <TextInput 
                label="Gluetun Control API URL"
                description="The internal Docker URL to reach Gluetun's control API (port 8000)"
                value={gluetunUrl}
                onChange={(event) => setGluetunUrl(event.currentTarget.value)}
                placeholder="http://gluetun:8000"
              />
              
              <Group justify="flex-end" mt="md">
                <Button onClick={saveVpnSettings} leftSection={<ShieldAlert size={16} />}>
                  Save Settings
                </Button>
              </Group>
            </Stack>
          </Card>
        </Tabs.Panel>
        <Tabs.Panel value="auditor" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Group justify="space-between" mb="md">
              <Box>
                <Text fw={500} size="lg">Provider-Auditor</Text>
                <Text c="dimmed" size="sm">Führt Latenz- und Verfügbarkeits-Benchmarks für alle konfigurierten M3U/XC-Provider durch.</Text>
              </Box>
              <Button leftSection={<LineChart size={14} />} onClick={handleTriggerAudit} loading={auditing}>
                Run Benchmark Now
              </Button>
            </Group>
            
            <Group justify="flex-end" mb="xs">
              <Button variant="subtle" size="xs" onClick={fetchAuditResults} leftSection={<RefreshCw size={12} />}>
                Refresh Results
              </Button>
            </Group>
            
            <ScrollArea>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Provider Name</Table.Th>
                    <Table.Th>Type</Table.Th>
                    <Table.Th>Status</Table.Th>
                    <Table.Th>Latency (ms)</Table.Th>
                    <Table.Th>Last Checked</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {auditResults.length === 0 ? (
                    <Table.Tr>
                      <Table.Td colSpan={5} ta="center">No benchmark results yet</Table.Td>
                    </Table.Tr>
                  ) : (
                    auditResults.map((res) => (
                      <Table.Tr key={res.id}>
                        <Table.Td fw={500}>{res.name}</Table.Td>
                        <Table.Td>{res.type}</Table.Td>
                        <Table.Td>
                          <Badge color={res.status === 'OK' ? 'green' : 'red'}>{res.status}</Badge>
                        </Table.Td>
                        <Table.Td>
                          <Text c={res.latency_ms > 1500 ? 'red' : res.latency_ms > 800 ? 'yellow' : 'green'} fw={500}>
                            {res.latency_ms > 0 ? `${res.latency_ms} ms` : 'N/A'}
                          </Text>
                        </Table.Td>
                        <Table.Td>{res.last_checked ? new Date(res.last_checked * 1000).toLocaleString() : 'N/A'}</Table.Td>
                      </Table.Tr>
                    ))
                  )}
                </Table.Tbody>
              </Table>
            </ScrollArea>
          </Card>
        </Tabs.Panel>
        <Tabs.Panel value="epg" pt="md">
          <Text c="dimmed">EPG Timezone-Shifter Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>
        <Tabs.Panel value="slicer" pt="md">
          <Text c="dimmed">Playlist-Slicer Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>
        <Tabs.Panel value="sqlite" pt="md">
          <Text c="dimmed">SQLite DB-Optimizer Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>
      </Tabs>
    </Stack>
  );
};

export default AdminCenter;
