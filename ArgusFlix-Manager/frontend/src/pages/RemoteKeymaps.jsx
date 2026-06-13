import React, { useEffect, useState } from 'react';
import {
  Box,
  Stack,
  Text,
  Title,
  Group,
  Button,
  Table,
  ActionIcon,
  Modal,
  Paper,
  Loader,
  TextInput,
  Select,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Trash, Plus, Save, Edit } from 'lucide-react';
import api from '../api';

const ANDROID_KEY_CODES = [
  { value: 'KEYCODE_PROG_RED', label: 'Red Button' },
  { value: 'KEYCODE_PROG_GREEN', label: 'Green Button' },
  { value: 'KEYCODE_PROG_YELLOW', label: 'Yellow Button' },
  { value: 'KEYCODE_PROG_BLUE', label: 'Blue Button' },
  { value: 'KEYCODE_GUIDE', label: 'Guide / EPG' },
  { value: 'KEYCODE_INFO', label: 'Info' },
  { value: 'KEYCODE_TV_TELETEXT', label: 'Teletext' },
  { value: 'KEYCODE_MEDIA_RECORD', label: 'Record / DVR' },
  { value: 'KEYCODE_BUTTON_1', label: 'VOD / Custom 1' },
  { value: 'KEYCODE_BUTTON_2', label: 'Live / Custom 2' },
  { value: 'KEYCODE_BUTTON_3', label: 'Series / Custom 3' },
];

const APP_ACTIONS = [
  { value: 'OPEN_LIVE', label: 'Open Live TV' },
  { value: 'OPEN_VOD', label: 'Open Movies (VOD)' },
  { value: 'OPEN_SERIES', label: 'Open Series' },
  { value: 'OPEN_EPG', label: 'Open TV Guide' },
  { value: 'OPEN_FAVORITES', label: 'Open Favorites' },
  { value: 'TOGGLE_PIP', label: 'Toggle Picture-in-Picture' },
  { value: 'TOGGLE_SUBTITLES', label: 'Toggle Subtitles' },
  { value: 'OPEN_SEARCH', label: 'Search' },
  { value: 'EXIT_APP', label: 'Exit App' },
];

const RemoteKeymaps = () => {
  const [keymaps, setKeymaps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  const [opened, setOpened] = useState(false);
  const [formData, setFormData] = useState({ id: null, name: '', mapping: {} });
  
  const [currentKey, setCurrentKey] = useState('');
  const [currentAction, setCurrentAction] = useState('');

  const fetchKeymaps = async () => {
    setIsLoading(true);
    try {
      const data = await api.get('/api/devices/keymaps/');
      setKeymaps(Array.isArray(data) ? data : data.results || []);
    } catch (e) {
      console.error(e);
      notifications.show({ title: 'Error', message: 'Failed to load keymaps', color: 'red' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchKeymaps();
  }, []);

  const handleSave = async () => {
    try {
      if (formData.id) {
        await api.put(`/api/devices/keymaps/${formData.id}/`, formData);
        notifications.show({ title: 'Success', message: 'Keymap updated', color: 'green' });
      } else {
        await api.post('/api/devices/keymaps/', formData);
        notifications.show({ title: 'Success', message: 'Keymap created', color: 'green' });
      }
      setOpened(false);
      fetchKeymaps();
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to save keymap', color: 'red' });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this keymap profile?')) return;
    try {
      await api.delete(`/api/devices/keymaps/${id}/`);
      notifications.show({ title: 'Deleted', message: 'Keymap removed', color: 'green' });
      fetchKeymaps();
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to delete keymap', color: 'red' });
    }
  };

  const addMapping = () => {
    if (currentKey && currentAction) {
      setFormData(prev => ({
        ...prev,
        mapping: { ...prev.mapping, [currentKey]: currentAction }
      }));
      setCurrentKey('');
      setCurrentAction('');
    }
  };

  const removeMapping = (keyToRemove) => {
    setFormData(prev => {
      const newMapping = { ...prev.mapping };
      delete newMapping[keyToRemove];
      return { ...prev, mapping: newMapping };
    });
  };

  const openEdit = (keymap) => {
    setFormData({ id: keymap.id, name: keymap.name, mapping: keymap.mapping || {} });
    setOpened(true);
  };

  const openCreate = () => {
    setFormData({ id: null, name: '', mapping: {} });
    setOpened(true);
  };

  return (
    <Box>
      <Group justify="space-between" mb="md">
        <Text size="sm" c="dimmed">
          Create custom remote control mappings to push to your Argus TV devices.
        </Text>
        <Button leftSection={<Plus size={16} />} onClick={openCreate} color="blue">
          Create Keymap Profile
        </Button>
      </Group>

      <Paper withBorder p="md">
        {isLoading ? (
          <Group justify="center" p="xl"><Loader /></Group>
        ) : keymaps.length === 0 ? (
          <Text c="dimmed" ta="center" p="xl">No keymap profiles created yet.</Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Profile Name</Table.Th>
                <Table.Th>Mapped Keys</Table.Th>
                <Table.Th>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {keymaps.map(k => (
                <Table.Tr key={k.id}>
                  <Table.Td fw={500}>{k.name}</Table.Td>
                  <Table.Td>{Object.keys(k.mapping || {}).length} rules</Table.Td>
                  <Table.Td>
                    <Group gap="xs">
                      <ActionIcon variant="light" color="blue" onClick={() => openEdit(k)}>
                        <Edit size={14} />
                      </ActionIcon>
                      <ActionIcon variant="light" color="red" onClick={() => handleDelete(k.id)}>
                        <Trash size={14} />
                      </ActionIcon>
                    </Group>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Paper>

      <Modal opened={opened} onClose={() => setOpened(false)} title={formData.id ? "Edit Keymap Profile" : "Create Keymap Profile"} size="lg">
        <Stack gap="md">
          <TextInput
            label="Profile Name"
            placeholder="e.g. Formuler Z11 Default"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          
          <Paper withBorder p="md">
            <Title order={5} mb="sm">Key Mappings</Title>
            
            <Group align="flex-end" mb="md">
              <Select
                label="Android Key Code"
                placeholder="Select key"
                data={ANDROID_KEY_CODES}
                value={currentKey}
                onChange={setCurrentKey}
                searchable
                style={{ flex: 1 }}
              />
              <Select
                label="App Action"
                placeholder="Select action"
                data={APP_ACTIONS}
                value={currentAction}
                onChange={setCurrentAction}
                style={{ flex: 1 }}
              />
              <Button onClick={addMapping} disabled={!currentKey || !currentAction}>Add</Button>
            </Group>

            <Table striped>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Key Code</Table.Th>
                  <Table.Th>Action</Table.Th>
                  <Table.Th></Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {Object.entries(formData.mapping).map(([key, action]) => (
                  <Table.Tr key={key}>
                    <Table.Td>{ANDROID_KEY_CODES.find(k => k.value === key)?.label || key}</Table.Td>
                    <Table.Td>{APP_ACTIONS.find(a => a.value === action)?.label || action}</Table.Td>
                    <Table.Td>
                      <ActionIcon color="red" variant="subtle" onClick={() => removeMapping(key)}>
                        <Trash size={14} />
                      </ActionIcon>
                    </Table.Td>
                  </Table.Tr>
                ))}
                {Object.keys(formData.mapping).length === 0 && (
                  <Table.Tr>
                    <Table.Td colSpan={3} align="center"><Text c="dimmed" size="sm">No mappings added</Text></Table.Td>
                  </Table.Tr>
                )}
              </Table.Tbody>
            </Table>
          </Paper>

          <Button onClick={handleSave} disabled={!formData.name} fullWidth mt="md">
            Save Keymap Profile
          </Button>
        </Stack>
      </Modal>
    </Box>
  );
};

export default RemoteKeymaps;
