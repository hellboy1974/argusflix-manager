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
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Smartphone, Trash, Plus, Wifi, WifiOff, UploadCloud, DownloadCloud, MoreVertical } from 'lucide-react';
import api from '../api';
import ErrorBoundary from '../components/ErrorBoundary';

const ArgusDevicesContent = () => {
  const [devices, setDevices] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isPairingModalOpen, setIsPairingModalOpen] = useState(false);
  const [pairingCode, setPairingCode] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

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

  const fetchDevices = async () => {
    setIsLoading(true);
    try {
      const data = await api.getArgusDevices();
      setDevices(Array.isArray(data) ? data : data.results || []);
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

  const openBackupModal = (device, mode) => {
    setSelectedDevice(device);
    setBackupMode(mode);
    setIsBackupModalOpen(true);
  };

  const executeBackupAction = () => {
    const command = backupMode === 'pull' ? 'PULL_BACKUP' : 'PUSH_BACKUP';
    handleSendCommand(selectedDevice.id, command, backupOptions);
    setIsBackupModalOpen(false);
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
        <Button leftSection={<Plus size={16} />} onClick={handleOpenPairingModal} color="blue">
          Pair New Device
        </Button>
      </Group>

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

      {/* Backup / Restore Selection Modal */}
      <Modal
        opened={isBackupModalOpen}
        onClose={() => setIsBackupModalOpen(false)}
        title={backupMode === 'pull' ? `Request Backup from ${selectedDevice?.name}` : `Restore Backup to ${selectedDevice?.name}`}
      >
        <Stack gap="md">
          <Text size="sm">
            Please select the specific data components you want to {backupMode === 'pull' ? 'include in this backup' : 'restore to the TV'}:
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
          <Group justify="flex-end" mt="md">
            <Button variant="default" onClick={() => setIsBackupModalOpen(false)}>Cancel</Button>
            <Button onClick={executeBackupAction} color={backupMode === 'pull' ? 'blue' : 'orange'}>
              {backupMode === 'pull' ? 'Request Backup' : 'Push Restore'}
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
