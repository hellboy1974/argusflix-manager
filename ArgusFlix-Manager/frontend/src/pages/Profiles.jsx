import React, { useEffect, useState } from 'react';
import {
  Box,
  Title,
  Text,
  Group,
  Stack,
  Card,
  Button,
  Avatar,
  ActionIcon,
  Modal,
  TextInput,
  Checkbox,
  Loader,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import { Edit, Trash, Plus, User as UserIcon, Lock } from 'lucide-react';
import api from '../api';

const Profiles = () => {
  const [profiles, setProfiles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [opened, { open, close }] = useDisclosure(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const [formData, setFormData] = useState({ id: null, name: '', avatar_url: '', pin: '', is_kids_profile: false });

  const fetchProfiles = async () => {
    try {
      setIsLoading(true);
      const data = await api.get('/api/accounts/profiles/');
      setProfiles(Array.isArray(data) ? data : data.results || []);
    } catch (e) {
      console.error(e);
      notifications.show({ title: 'Error', message: 'Failed to load profiles', color: 'red' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProfiles();
  }, []);

  const handleSave = async () => {
    try {
      if (formData.id) {
        await api.put(`/api/accounts/profiles/${formData.id}/`, formData);
        notifications.show({ title: 'Success', message: 'Profile updated', color: 'green' });
      } else {
        await api.post('/api/accounts/profiles/', formData);
        notifications.show({ title: 'Success', message: 'Profile created', color: 'green' });
      }
      close();
      fetchProfiles();
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to save profile', color: 'red' });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this profile? This will delete all watch history and favorites associated with it.')) return;
    try {
      setIsDeleting(true);
      await api.delete(`/api/accounts/profiles/${id}/`);
      notifications.show({ title: 'Deleted', message: 'Profile removed', color: 'green' });
      fetchProfiles();
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to delete profile', color: 'red' });
    } finally {
      setIsDeleting(false);
    }
  };

  const openEdit = (profile) => {
    setFormData({ id: profile.id, name: profile.name, avatar_url: profile.avatar_url || '', pin: profile.pin || '', is_kids_profile: profile.is_kids_profile });
    open();
  };

  const openCreate = () => {
    setFormData({ id: null, name: '', avatar_url: '', pin: '', is_kids_profile: false });
    open();
  };

  if (isLoading) {
    return <Loader mt="xl" />;
  }

  return (
    <Box>
      <Group justify="space-between" mb="lg">
        <Title order={2}>Cloud Profiles</Title>
        <Button leftSection={<Plus size={16} />} onClick={openCreate}>Add Profile</Button>
      </Group>

      <Text c="dimmed" mb="xl">
        Profiles sync watch history and favorites across your Argus TV Apps. Create multiple profiles to keep recommendations and watch history separate.
      </Text>

      <Group align="flex-start" gap="lg">
        {profiles.map(p => (
          <Card key={p.id} shadow="sm" padding="lg" radius="md" withBorder style={{ width: 250 }}>
            <Stack align="center" gap="sm">
              <Avatar src={p.avatar_url} size={80} radius="xl" color="blue">
                {!p.avatar_url && <UserIcon size={40} />}
              </Avatar>
              <Group gap="xs">
                <Title order={4}>{p.name}</Title>
                {p.pin && <Lock size={16} color="gray" />}
              </Group>
              {p.is_kids_profile && <Text size="xs" c="green" fw={700}>Kids Profile</Text>}
            </Stack>

            <Group grow mt="md">
              <Button variant="light" size="xs" leftSection={<Edit size={14} />} onClick={() => openEdit(p)}>
                Edit
              </Button>
              <ActionIcon variant="light" color="red" size="md" onClick={() => handleDelete(p.id)} loading={isDeleting}>
                <Trash size={14} />
              </ActionIcon>
            </Group>
          </Card>
        ))}
        {profiles.length === 0 && (
          <Text c="dimmed">No profiles created yet. Create one to enable Watch History sync.</Text>
        )}
      </Group>

      <Modal opened={opened} onClose={close} title={formData.id ? "Edit Profile" : "Create Profile"}>
        <Stack gap="md">
          <TextInput
            label="Profile Name"
            placeholder="e.g. Papa, Kids"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <TextInput
            label="Avatar URL (Optional)"
            placeholder="https://..."
            value={formData.avatar_url}
            onChange={(e) => setFormData({ ...formData, avatar_url: e.target.value })}
          />
          <TextInput
            label="PIN (Optional)"
            placeholder="4 Digits (e.g. 1234)"
            maxLength={4}
            value={formData.pin}
            onChange={(e) => setFormData({ ...formData, pin: e.target.value.replace(/\D/g, '') })}
          />
          <Checkbox
            label="Kids Profile"
            checked={formData.is_kids_profile}
            onChange={(e) => setFormData({ ...formData, is_kids_profile: e.currentTarget.checked })}
          />
          <Button onClick={handleSave} disabled={!formData.name} fullWidth mt="md">
            Save Profile
          </Button>
        </Stack>
      </Modal>
    </Box>
  );
};

export default Profiles;
