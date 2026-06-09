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
  TextInput,
  Select,
  Switch,
  Paper,
  Loader,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Server, Edit, Trash, Zap, Plus, Check, X } from 'lucide-react';
import api from '../api';
import ErrorBoundary from '../components/ErrorBoundary';

const MediaServersContent = () => {
  const [servers, setServers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingServer, setEditingServer] = useState(null);
  const [isTesting, setIsTesting] = useState(false);

  const form = useForm({
    initialValues: {
      name: '',
      server_type: 'plex',
      base_url: '',
      api_token: '',
      is_active: true,
    },
    validate: {
      name: (value) => (value.trim().length > 0 ? null : 'Name is required'),
      base_url: (value) =>
        /^https?:\/\/.+/.test(value) ? null : 'Valid URL required (http/https)',
      api_token: (value) =>
        value.trim().length > 0 ? null : 'API Token is required',
    },
  });

  const fetchServers = async () => {
    setIsLoading(true);
    try {
      const data = await api.getMediaServers();
      setServers(Array.isArray(data) ? data : data.results || []);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchServers();
  }, []);

  const handleOpenModal = (server = null) => {
    if (server) {
      setEditingServer(server);
      form.setValues({
        name: server.name,
        server_type: server.server_type,
        base_url: server.base_url,
        api_token: server.api_token || '',
        is_active: server.is_active,
      });
    } else {
      setEditingServer(null);
      form.reset();
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    form.reset();
    setEditingServer(null);
  };

  const handleSubmit = async (values) => {
    try {
      if (editingServer) {
        await api.updateMediaServer(editingServer.id, values);
        notifications.show({
          title: 'Success',
          message: 'Media server updated successfully',
          color: 'green',
        });
      } else {
        await api.addMediaServer(values);
        notifications.show({
          title: 'Success',
          message: 'Media server added successfully',
          color: 'green',
        });
      }
      handleCloseModal();
      fetchServers();
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this server?')) {
      try {
        await api.deleteMediaServer(id);
        notifications.show({
          title: 'Success',
          message: 'Media server deleted',
          color: 'green',
        });
        fetchServers();
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleTestConnection = async (id) => {
    setIsTesting(true);
    try {
      const resp = await api.testMediaServerConnection(id);
      if (resp.status === 'success') {
        notifications.show({
          title: 'Connection Successful',
          message: resp.message,
          color: 'green',
          icon: <Check size={16} />,
        });
      } else {
        notifications.show({
          title: 'Connection Failed',
          message: resp.message || 'Unknown error',
          color: 'red',
          icon: <X size={16} />,
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <Stack p="md" h="100%" gap="md">
      <Group justify="space-between" align="center" mb="xs">
        <Stack gap={2}>
          <Group gap="xs">
            <Server size={24} color="var(--mantine-color-blue-filled)" />
            <Title order={2} style={{ fontFamily: 'Outfit, Inter, sans-serif', fontWeight: 600 }}>
              Media Servers
            </Title>
          </Group>
          <Text size="xs" c="dimmed">
            Manage your Plex, Emby, and Jellyfin servers for integration with Argus IPTV Player.
          </Text>
        </Stack>
        <Button leftSection={<Plus size={16} />} onClick={() => handleOpenModal()}>
          Add Server
        </Button>
      </Group>

      <Paper withBorder p="md" style={{ flex: 1, overflow: 'auto' }}>
        {isLoading ? (
          <Group justify="center" p="xl">
            <Loader />
          </Group>
        ) : servers.length === 0 ? (
          <Text c="dimmed" ta="center" p="xl">
            No media servers configured.
          </Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Name</Table.Th>
                <Table.Th>Type</Table.Th>
                <Table.Th>Base URL</Table.Th>
                <Table.Th>Status</Table.Th>
                <Table.Th>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {servers.map((server) => (
                <Table.Tr key={server.id}>
                  <Table.Td fw={500}>{server.name}</Table.Td>
                  <Table.Td>
                    <Badge color={server.server_type === 'plex' ? 'yellow' : server.server_type === 'emby' ? 'green' : 'violet'}>
                      {server.server_type.toUpperCase()}
                    </Badge>
                  </Table.Td>
                  <Table.Td>{server.base_url}</Table.Td>
                  <Table.Td>
                    {server.is_active ? (
                      <Badge color="green" variant="light">Active</Badge>
                    ) : (
                      <Badge color="gray" variant="light">Inactive</Badge>
                    )}
                  </Table.Td>
                  <Table.Td>
                    <Group gap="xs">
                      <Button
                        size="xs"
                        variant="light"
                        color="blue"
                        leftSection={<Zap size={14} />}
                        onClick={() => handleTestConnection(server.id)}
                        loading={isTesting}
                      >
                        Test
                      </Button>
                      <ActionIcon color="blue" variant="subtle" onClick={() => handleOpenModal(server)}>
                        <Edit size={16} />
                      </ActionIcon>
                      <ActionIcon color="red" variant="subtle" onClick={() => handleDelete(server.id)}>
                        <Trash size={16} />
                      </ActionIcon>
                    </Group>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Paper>

      <Modal
        opened={isModalOpen}
        onClose={handleCloseModal}
        title={editingServer ? 'Edit Media Server' : 'Add Media Server'}
      >
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Stack gap="md">
            <TextInput
              label="Name"
              placeholder="My Plex Server"
              withAsterisk
              {...form.getInputProps('name')}
            />
            <Select
              label="Server Type"
              data={[
                { value: 'plex', label: 'Plex' },
                { value: 'emby', label: 'Emby' },
                { value: 'jellyfin', label: 'Jellyfin' },
              ]}
              withAsterisk
              {...form.getInputProps('server_type')}
            />
            <TextInput
              label="Base URL"
              placeholder="http://192.168.1.100:32400"
              withAsterisk
              {...form.getInputProps('base_url')}
            />
            <TextInput
              label="API Token"
              placeholder="Your authentication token"
              withAsterisk
              {...form.getInputProps('api_token')}
            />
            <Switch
              label="Active"
              {...form.getInputProps('is_active', { type: 'checkbox' })}
            />
            <Group justify="flex-end" mt="md">
              <Button variant="default" onClick={handleCloseModal}>
                Cancel
              </Button>
              <Button type="submit">Save</Button>
            </Group>
          </Stack>
        </form>
      </Modal>
    </Stack>
  );
};

const MediaServersPage = () => {
  return (
    <ErrorBoundary>
      <MediaServersContent />
    </ErrorBoundary>
  );
};

export default MediaServersPage;
