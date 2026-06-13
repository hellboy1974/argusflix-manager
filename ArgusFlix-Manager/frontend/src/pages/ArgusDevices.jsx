import React, { useEffect, useState } from 'react';
import {
  Box,
  Stack,
  Text,
  Title,
  Group,
  Button,
  Table,
  Badge,
  ActionIcon,
  Modal,
  Paper,
  Loader,
  Menu,
  Checkbox,
  TextInput,
  Select,
  Tabs,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Smartphone, Trash, Plus, Wifi, WifiOff, UploadCloud, DownloadCloud, MoreVertical, MonitorPlay, Gamepad2 } from 'lucide-react';
import api from '../api';
import ErrorBoundary from '../components/ErrorBoundary';
import RemoteKeymaps from './RemoteKeymaps';

const ArgusDevicesContent = () => {
  const [activeTab, setActiveTab] = useState('devices');
  const [devices, setDevices] = useState([]);
  const [keymaps, setKeymaps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isPairingModalOpen, setIsPairingModalOpen] = useState(false);
  const [pairingCode, setPairingCode] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  // Remote Install Modal state
  const [isRemoteInstallModalOpen, setIsRemoteInstallModalOpen] = useState(false);
  const [remoteIp, setRemoteIp] = useState('');
  const [isInstalling, setIsInstalling] = useState(false);

  // Backup/Restore Modal state
  const [isBackupModalOpen, setIsBackupModalOpen] = useState(false);
  const [backupMode, setBackupMode] = useState(''); // 'pull' or 'push'
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [backupOptions, setBackupOptions] = useState({
    playlists: true,
    servers: true,
    settings: true,
    history: false,
  });
  const [deviceBackups, setDeviceBackups] = useState([]);
  const [selectedBackupUrl, setSelectedBackupUrl] = useState('');
  const [isFetchingBackups, setIsFetchingBackups] = useState(false);

  // Push Provider Modal state
  const [isPushProviderModalOpen, setIsPushProviderModalOpen] = useState(false);
  const [pushProviderData, setPushProviderData] = useState({ type: 'stalker', name: '', url: '', mac: '', username: '', password: '', token: '' });

  const fetchDevices = async () => {
    setIsLoading(true);
    try {
      const data = await api.getArgusDevices();
      setDevices(Array.isArray(data) ? data : data.results || []);
      
      const keymapData = await api.get('/api/devices/keymaps/');
      setKeymaps(Array.isArray(keymapData) ? keymapData : keymapData.results || []);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices();
    
    let interval;
    if (isPairingModalOpen) {
      interval = setInterval(fetchDevices, 3000);
    }
    return () => clearInterval(interval);
  }, [isPairingModalOpen]);

  const handleOpenPairingModal = async () => {
    setIsGenerating(true);
    setIsPairingModalOpen(true);
    try {
      const resp = await api.generateDevicePairingCode();
      if (resp.pairing_code) {
        setPairingCode(resp.pairing_code);
      }
    } catch (e) {
      setIsPairingModalOpen(false);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRemoteInstall = async () => {
    if (!remoteIp) return;
    setIsInstalling(true);
    try {
      const resp = await api.remoteInstallDevice(remoteIp);
      notifications.show({
        title: 'Installation Complete',
        message: resp.message || 'App successfully installed and launched.',
        color: 'green',
      });
      setIsRemoteInstallModalOpen(false);
      setRemoteIp('');
    } catch (e) {
      // API error handler already shows notification
    } finally {
      setIsInstalling(false);
    }
  };


  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to remove this device?')) {
      try {
        await api.deleteArgusDevice(id);
        notifications.show({
          title: 'Success',
          message: 'Device removed',
          color: 'green',
        });
        fetchDevices();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleSendCommand = async (id, command, payload = {}) => {
    try {
      await api.sendDeviceCommand(id, command, payload);
      notifications.show({
        title: 'Command Sent',
        message: `Command '${command}' sent successfully`,
        color: 'blue',
      });
    } catch (e) {
      console.error(e);
    }
  };

  const handleAssignKeymap = async (deviceId, keymapId) => {
    try {
      await api.patch(`/api/devices/devices/${deviceId}/`, {
        keymap: keymapId || null
      });
      notifications.show({
        title: 'Success',
        message: 'Keymap profile assigned successfully',
        color: 'green'
      });
      fetchDevices();
    } catch (e) {
      notifications.show({
        title: 'Error',
        message: 'Failed to assign keymap profile',
        color: 'red'
      });
    }
  };

  const openBackupModal = async (device, mode) => {
    setSelectedDevice(device);
    setBackupMode(mode);
    setIsBackupModalOpen(true);
    if (mode === 'push') {
      setIsFetchingBackups(true);
      try {
        const resp = await api.getDeviceBackups(device.id);
        const results = Array.isArray(resp) ? resp : (resp?.results || []);
        setDeviceBackups(results);
        if (results.length > 0) {
          setSelectedBackupUrl(results[0].file);
        } else {
          setSelectedBackupUrl('');
        }
      } catch (e) {
        console.error("Failed to fetch backups", e);
      } finally {
        setIsFetchingBackups(false);
      }
    }
  };

  const executeBackupAction = () => {
    if (backupMode === 'pull') {
      handleSendCommand(selectedDevice.id, 'PULL_BACKUP', backupOptions);
    } else {
      if (!selectedBackupUrl) return;
      handleSendCommand(selectedDevice.id, 'PUSH_BACKUP', { backup_url: selectedBackupUrl });
    }
    setIsBackupModalOpen(false);
  };

  const handlePushProvider = () => {
    if (!selectedDevice || !pushProviderData.url) return;
    handleSendCommand(selectedDevice.id, 'add_provider', {
      type: pushProviderData.type,
      name: pushProviderData.name || `Pushed ${pushProviderData.type}`,
      url: pushProviderData.url,
      mac: pushProviderData.mac,
      username: pushProviderData.username,
      password: pushProviderData.password,
      token: pushProviderData.token,
      serverUrl: pushProviderData.url, // map url to serverUrl for media servers/xtream
    });
    setIsPushProviderModalOpen(false);
    setPushProviderData({ type: 'stalker', name: '', url: '', mac: '', username: '', password: '', token: '' });
  };

  return (
    <Stack p="md" h="100%" gap="md">
      <Group justify="space-between" align="center" mb="xs">
        <Stack gap={2}>
          <Group gap="xs">
            <Smartphone size={24} color="var(--mantine-color-blue-filled)" />
            <Title order={2} style={{ fontFamily: 'Outfit, Inter, sans-serif', fontWeight: 600 }}>
              Argus TV Devices
            </Title>
          </Group>
          <Text size="xs" c="dimmed">
            Manage your connected Argus IPTV Player devices. Push playlists, sync media servers, and backup settings.
          </Text>
        </Stack>
        <Group>
          <Button variant="light" leftSection={<MonitorPlay size={16} />} onClick={() => setIsRemoteInstallModalOpen(true)} color="orange">
            Remote Install to TV
          </Button>
          <Button leftSection={<Plus size={16} />} onClick={handleOpenPairingModal} color="blue">
            Pair New Device
          </Button>
        </Group>
      </Group>

      <Tabs value={activeTab} onChange={setActiveTab} style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Tabs.List mb="md">
          <Tabs.Tab value="devices" leftSection={<Smartphone size={16} />}>
            Paired Devices
          </Tabs.Tab>
          <Tabs.Tab value="keymaps" leftSection={<Gamepad2 size={16} />}>
            Remote Keymaps
          </Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="devices" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <Paper withBorder p="md" style={{ flex: 1, overflow: 'auto' }}>
            {isLoading && devices.length === 0 ? (
              <Group justify="center" p="xl">
                <Loader />
              </Group>
            ) : devices.length === 0 ? (
              <Text c="dimmed" ta="center" p="xl">
                No devices paired yet.
              </Text>
            ) : (
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Name</Table.Th>
                    <Table.Th>Device ID</Table.Th>
                    <Table.Th>Status</Table.Th>
                    <Table.Th>Keymap Profile</Table.Th>
                    <Table.Th>Last IP</Table.Th>
                    <Table.Th>Actions</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {devices.map((device) => (
                    <Table.Tr key={device.id}>
                      <Table.Td fw={500}>{device.name}</Table.Td>
                      <Table.Td><Text size="xs" c="dimmed">{device.device_id}</Text></Table.Td>
                      <Table.Td>
                        {device.is_paired ? (
                          <Badge color="green" variant="light" leftSection={<Wifi size={10} />}>Paired</Badge>
                        ) : (
                          <Badge color="yellow" variant="light" leftSection={<WifiOff size={10} />}>Pending</Badge>
                        )}
                      </Table.Td>
                      <Table.Td>
                        {device.is_paired ? (
                          <Select
                            size="xs"
                            placeholder="Default (No Keymap)"
                            data={[
                              { value: '', label: 'Default (No Keymap)' },
                              ...keymaps.map(k => ({ value: String(k.id), label: k.name }))
                            ]}
                            value={device.keymap ? String(device.keymap) : ''}
                            onChange={(val) => handleAssignKeymap(device.id, val)}
                            clearable
                          />
                        ) : (
                          <Text size="xs" c="dimmed">-</Text>
                        )}
                      </Table.Td>
                      <Table.Td>{device.last_ip || 'N/A'}</Table.Td>
                      <Table.Td>
                        {device.is_paired && (
                          <Group gap="xs">
                            <Button
                              size="xs"
                              variant="light"
                              color="blue"
                              leftSection={<UploadCloud size={14} />}
                              onClick={() => handleSendCommand(device.id, 'SYNC_PLAYLISTS')}
                            >
                              Push Playlists
                            </Button>
                            <Menu shadow="md" width={200} position="bottom-end">
                              <Menu.Target>
                                <ActionIcon variant="subtle" color="gray">
                                  <MoreVertical size={16} />
                                </ActionIcon>
                              </Menu.Target>
                              <Menu.Dropdown>
                                <Menu.Item leftSection={<UploadCloud size={14} />} onClick={() => handleSendCommand(device.id, 'SYNC_SERVERS')}>
                                  Push Media Servers
                                </Menu.Item>
                                <Menu.Item leftSection={<UploadCloud size={14} />} onClick={() => {
                                  setSelectedDevice(device);
                                  setIsPushProviderModalOpen(true);
                                }}>
                                  Push Provider to TV
                                </Menu.Item>
                                <Menu.Item leftSection={<DownloadCloud size={14} />} onClick={() => openBackupModal(device, 'pull')}>
                                  Request Backup from TV
                                </Menu.Item>
                                <Menu.Item leftSection={<UploadCloud size={14} />} onClick={() => openBackupModal(device, 'push')}>
                                  Restore Backup to TV
                                </Menu.Item>
                                <Menu.Divider />
                                <Menu.Item color="red" leftSection={<Trash size={14} />} onClick={() => handleDelete(device.id)}>
                                  Remove Device
                                </Menu.Item>
                              </Menu.Dropdown>
                            </Menu>
                          </Group>
                        )}
                        {!device.is_paired && (
                          <ActionIcon color="red" variant="subtle" onClick={() => handleDelete(device.id)}>
                            <Trash size={16} />
                          </ActionIcon>
                        )}
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            )}
          </Paper>
        </Tabs.Panel>
        
        <Tabs.Panel value="keymaps" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <RemoteKeymaps />
        </Tabs.Panel>
      </Tabs>

      {/* Backup / Restore Selection Modal */}
      <Modal
        opened={isBackupModalOpen}
        onClose={() => setIsBackupModalOpen(false)}
        title={backupMode === 'pull' ? `Request Backup from ${selectedDevice?.name}` : `Restore Backup to ${selectedDevice?.name}`}
      >
        <Stack gap="md">
          {backupMode === 'pull' ? (
            <>
              <Text size="sm">
                Please select the specific data components you want to include in this backup:
              </Text>
              <Paper withBorder p="sm">
                <Stack gap="xs">
                  <Checkbox
                    label="Playlists (M3U, Xtream, Stalker)"
                    checked={backupOptions.playlists}
                    onChange={(event) => setBackupOptions({ ...backupOptions, playlists: event.currentTarget.checked })}
                  />
                  <Checkbox
                    label="Media Server Profiles (Plex, Emby, Jellyfin)"
                    checked={backupOptions.servers}
                    onChange={(event) => setBackupOptions({ ...backupOptions, servers: event.currentTarget.checked })}
                  />
                  <Checkbox
                    label="App Settings (UI, Theme, Preferences)"
                    checked={backupOptions.settings}
                    onChange={(event) => setBackupOptions({ ...backupOptions, settings: event.currentTarget.checked })}
                  />
                  <Checkbox
                    label="Watch History & Favorites"
                    checked={backupOptions.history}
                    onChange={(event) => setBackupOptions({ ...backupOptions, history: event.currentTarget.checked })}
                  />
                </Stack>
              </Paper>
            </>
          ) : (
            <>
              <Text size="sm">Select an existing backup to restore to the TV:</Text>
              {isFetchingBackups ? (
                <Loader size="sm" />
              ) : deviceBackups.length > 0 ? (
                <Select
                  label="Select Backup"
                  value={selectedBackupUrl}
                  onChange={setSelectedBackupUrl}
                  data={deviceBackups.map(b => ({
                    value: b.file,
                    label: `Backup from ${new Date(b.created_at).toLocaleString()}`
                  }))}
                />
              ) : (
                <Text size="sm" c="red">No backups found for this device.</Text>
              )}
            </>
          )}
          <Group justify="flex-end" mt="md">
            <Button variant="default" onClick={() => setIsBackupModalOpen(false)}>Cancel</Button>
            <Button 
               onClick={executeBackupAction} 
               color={backupMode === 'pull' ? 'blue' : 'orange'}
               disabled={backupMode === 'push' && !selectedBackupUrl}
            >
              {backupMode === 'pull' ? 'Request Backup' : 'Push Restore'}
            </Button>
          </Group>
        </Stack>
      </Modal>

      <Modal
        opened={isPushProviderModalOpen}
        onClose={() => setIsPushProviderModalOpen(false)}
        title="Push Provider to TV"
        centered
        overlayProps={{ blur: 3 }}
      >
        <Stack gap="md">
          <Text size="sm" c="dimmed">
            This will push the connection directly to the TV App via WebSocket and automatically save it as a provider.
          </Text>
          <Select
            label="Provider Type"
            value={pushProviderData.type}
            onChange={(val) => setPushProviderData({ ...pushProviderData, type: val })}
            data={[
              { value: 'stalker', label: 'Stalker Portal' },
              { value: 'xtream', label: 'Xtream Codes' },
              { value: 'm3u', label: 'M3U Playlist' },
              { value: 'plex', label: 'Plex Server' },
              { value: 'emby', label: 'Emby Server' },
              { value: 'jellyfin', label: 'Jellyfin Server' },
            ]}
          />
          <TextInput
            label="Name (Optional)"
            placeholder="e.g. My Server"
            value={pushProviderData.name}
            onChange={(e) => setPushProviderData({ ...pushProviderData, name: e.target.value })}
          />
          <TextInput
            label={pushProviderData.type === 'm3u' ? 'M3U URL' : 'Server/Portal URL'}
            placeholder="http://example.com"
            value={pushProviderData.url}
            onChange={(e) => setPushProviderData({ ...pushProviderData, url: e.target.value })}
            required
          />
          {pushProviderData.type === 'stalker' && (
            <TextInput
              label="MAC Address"
              placeholder="00:1A:79:XX:XX:XX"
              value={pushProviderData.mac}
              onChange={(e) => setPushProviderData({ ...pushProviderData, mac: e.target.value })}
              required
            />
          )}
          {['xtream', 'emby', 'jellyfin'].includes(pushProviderData.type) && (
            <>
              <TextInput
                label="Username"
                value={pushProviderData.username}
                onChange={(e) => setPushProviderData({ ...pushProviderData, username: e.target.value })}
                required
              />
              <TextInput
                label="Password"
                type="password"
                value={pushProviderData.password}
                onChange={(e) => setPushProviderData({ ...pushProviderData, password: e.target.value })}
              />
            </>
          )}
          {pushProviderData.type === 'plex' && (
            <TextInput
              label="Plex Token"
              value={pushProviderData.token}
              onChange={(e) => setPushProviderData({ ...pushProviderData, token: e.target.value })}
              required
            />
          )}
          <Group justify="right" mt="md">
            <Button variant="light" color="gray" onClick={() => setIsPushProviderModalOpen(false)}>Cancel</Button>
            <Button color="blue" onClick={handlePushProvider} disabled={!pushProviderData.url}>
              Push Provider
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* Pairing Modal */}
      <Modal
        opened={isPairingModalOpen}
        onClose={() => setIsPairingModalOpen(false)}
        title="Pair New Argus TV Device"
        centered
      >
        <Stack align="center" py="xl">
          <Text size="sm" ta="center">
            Open the Argus IPTV Player on your TV and enter the following 6-digit code:
          </Text>
          {isGenerating ? (
            <Loader />
          ) : (
            <Text style={{ fontSize: '48px', fontWeight: 700, letterSpacing: '8px' }} c="blue">
              {pairingCode}
            </Text>
          )}
          <Text size="xs" c="dimmed" ta="center" mt="md">
            This window will automatically close once the device is paired.
          </Text>
        </Stack>
      </Modal>

      {/* Remote Install Modal */}
      <Modal
        opened={isRemoteInstallModalOpen}
        onClose={() => setIsRemoteInstallModalOpen(false)}
        title="Remote Install to TV"
        centered
      >
        <Stack gap="md">
          <Text size="sm">
            Enter the IP address of your Android TV. Make sure "Network Debugging" is enabled in Developer Options.
          </Text>
          <TextInput
            label="TV IP Address"
            placeholder="e.g. 192.168.1.55"
            value={remoteIp}
            onChange={(e) => setRemoteIp(e.currentTarget.value)}
          />
          <Group justify="flex-end" mt="md">
            <Button variant="default" onClick={() => setIsRemoteInstallModalOpen(false)}>Cancel</Button>
            <Button 
              color="orange" 
              onClick={handleRemoteInstall}
              loading={isInstalling}
              disabled={!remoteIp}
            >
              Install ArgusFlix
            </Button>
          </Group>
        </Stack>
      </Modal>
    </Stack>
  );
};

const ArgusDevicesPage = () => {
  return (
    <ErrorBoundary>
      <ArgusDevicesContent />
    </ErrorBoundary>
  );
};

export default ArgusDevicesPage;
