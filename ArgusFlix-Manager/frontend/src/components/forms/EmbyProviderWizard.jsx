import React, { useState, useEffect } from 'react';
import { Modal, Tabs, Box, Stack, TextInput, PasswordInput, Button, Group, Switch, Text, Divider, Badge, Paper } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Info, Tv, Film, MonitorPlay, Save, RefreshCw, Trash, Activity } from 'lucide-react';
import api from '../../api';

const CategoryList = ({ categories, onToggle }) => {
  if (!categories || categories.length === 0) return <Text c="dimmed">Keine Kategorien vorhanden.</Text>;
  return (
    <Stack spacing="xs">
      {categories.map((cat) => (
        <Group key={cat.id} position="apart" align="center" noWrap>
          <Box style={{ flex: 1 }}>
            <Text size="sm">{cat.name}</Text>
          </Box>
          <Switch 
            checked={cat.enabled}
            onChange={(e) => onToggle(cat.id, e.currentTarget.checked)}
          />
        </Group>
      ))}
    </Stack>
  );
};

export default function EmbyProviderWizard({ opened, onClose, server, onSave }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [categoriesData, setCategoriesData] = useState({
    live: { new: [], existing: [] },
    vod: { new: [], existing: [] },
    series: { new: [], existing: [] }
  });

  const form = useForm({
    initialValues: {
      name: '',
      base_url: '',
      api_token: '',
      is_active: true,
      sync_with_devices: true,
    },
    validate: {
      name: (val) => (val.trim() ? null : 'Name erforderlich'),
      base_url: (val) => (val.trim() ? null : 'URL erforderlich'),
      api_token: (val) => (val.trim() ? null : 'Emby Token erforderlich'),
    }
  });

  useEffect(() => {
    if (opened) {
      setActiveTab('overview');
      if (server) {
        form.setValues({
          name: server.name,
          base_url: server.base_url,
          api_token: server.api_token || '',
          is_active: server.is_active ?? true,
          sync_with_devices: server.custom_properties?.sync_with_devices ?? true,
        });
        fetchCategories();
      } else {
        form.reset();
        setCategoriesData({
          live: { new: [], existing: [] },
          vod: { new: [], existing: [] },
          series: { new: [], existing: [] }
        });
      }
    }
  }, [opened, server]);

  const fetchCategories = async () => {
    if (!server) return;
    try {
      setLoading(true);
      // For now, mock or fetch categories
      setCategoriesData({
        live: { new: [], existing: [] },
        vod: { new: [], existing: [] },
        series: { new: [], existing: [] }
      });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (values) => {
    try {
      setLoading(true);
      const payload = {
        name: values.name,
        server_type: 'emby',
        base_url: values.base_url,
        api_token: values.api_token,
        is_active: values.is_active,
        custom_properties: {
          ...(server?.custom_properties || {}),
          sync_with_devices: values.sync_with_devices,
        }
      };

      if (server) {
        await api.patch(`/api/v1/mediaservers/${server.id}/`, payload);
        notifications.show({ title: 'Erfolg', message: 'Emby Server gespeichert.', color: 'green' });
      } else {
        await api.post('/api/v1/mediaservers/', payload);
        notifications.show({ title: 'Erfolg', message: 'Emby Server hinzugefügt.', color: 'green' });
      }
      onSave();
    } catch (err) {
      notifications.show({ title: 'Fehler', message: err.message, color: 'red' });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!server) return;
    if (window.confirm('Möchtest Du diesen Emby Server wirklich löschen?')) {
      try {
        setLoading(true);
        await api.delete(`/api/v1/mediaservers/${server.id}/`);
        notifications.show({ title: 'Erfolg', message: 'Server gelöscht.', color: 'green' });
        onSave();
      } catch (err) {
        notifications.show({ title: 'Fehler', message: err.message, color: 'red' });
      } finally {
        setLoading(false);
      }
    }
  };

  const handleTestConnection = async () => {
    if (!server) return;
    try {
      setTesting(true);
      const res = await api.post(`/api/v1/mediaservers/${server.id}/test_connection/`);
      notifications.show({ title: 'Erfolg', message: 'Verbindung erfolgreich!', color: 'green' });
    } catch (err) {
      notifications.show({ title: 'Verbindungsfehler', message: err.response?.data?.message || err.message, color: 'red' });
    } finally {
      setTesting(false);
    }
  };

  return (
    <Modal 
      opened={opened} 
      onClose={onClose} 
      title={<Text weight={600} size="lg">{server ? 'Emby Server Bearbeiten' : 'Emby Server Hinzufügen'}</Text>}
      size="xl"
    >
      <form onSubmit={form.onSubmit(handleSave)}>
        <Tabs value={activeTab} onChange={setActiveTab} variant="outline">
          <Tabs.List>
            <Tabs.Tab value="overview" leftSection={<Info size={16} />}>Übersicht</Tabs.Tab>
            {server && <Tabs.Tab value="live" leftSection={<Tv size={16} />}>Live-TV</Tabs.Tab>}
            {server && <Tabs.Tab value="vod" leftSection={<Film size={16} />}>VOD</Tabs.Tab>}
            {server && <Tabs.Tab value="series" leftSection={<MonitorPlay size={16} />}>Serien</Tabs.Tab>}
          </Tabs.List>

          <Box mt="md" mih={350}>
            <Tabs.Panel value="overview">
              <Group grow align="flex-start">
                <Stack>
                  <Title order={5}>Server Informationen</Title>
                  <TextInput label="Server Name" placeholder="z.B. Mein Emby" {...form.getInputProps('name')} />
                  <TextInput label="Server URL" placeholder="http://192.168.1.100:8096" {...form.getInputProps('base_url')} />
                  <PasswordInput label="Emby Token" placeholder="X-Emby-Token" {...form.getInputProps('api_token')} />
                  
                  <Switch 
                    label="Verbindung Aktiv"
                    description="Wenn deaktiviert, wird der Server nicht synchronisiert."
                    {...form.getInputProps('is_active', { type: 'checkbox' })}
                  />

                  <Switch 
                    label="Mit Manager/Geräten synchronisieren"
                    {...form.getInputProps('sync_with_devices', { type: 'checkbox' })}
                  />
                </Stack>
                <Stack>
                  {server ? (
                    <Box mt="xl">
                      <Paper p="sm" withBorder bg="dark.7">
                        <Stack spacing="xs">
                          <Group position="apart">
                            <Text size="sm">Zuletzt synchronisiert:</Text>
                            <Badge>{server.updated_at ? new Date(server.updated_at).toLocaleString() : 'Nie'}</Badge>
                          </Group>
                          <Group position="apart">
                            <Text size="sm">Live-TV Sender:</Text>
                            <Badge color="blue">N/A</Badge>
                          </Group>
                          <Group position="apart">
                            <Text size="sm">VOD Filme:</Text>
                            <Badge color="grape">N/A</Badge>
                          </Group>
                        </Stack>
                      </Paper>
                      <Group grow mt="sm">
                        <Button variant="light" leftSection={<RefreshCw size={16} />}>
                          Sync
                        </Button>
                        <Button color="teal" variant="light" leftSection={<Activity size={16} />} onClick={handleTestConnection} loading={testing}>
                          Test
                        </Button>
                      </Group>
                    </Box>
                  ) : (
                    <Box mt="xl">
                       <Text c="dimmed" size="sm">Speichere den Emby Server, um weitere Optionen (Test, Sync, Kategorien) zu erhalten.</Text>
                    </Box>
                  )}
                </Stack>
              </Group>
            </Tabs.Panel>

            <Tabs.Panel value="live">
              <Stack>
                <Title order={5}>Neue Live-TV Kategorien</Title>
                <CategoryList categories={categoriesData.live.new} onToggle={() => {}} />
                <Divider my="sm" />
                <Title order={5}>Bestehende Live-TV Kategorien</Title>
                <CategoryList categories={categoriesData.live.existing} onToggle={() => {}} />
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="vod">
              <Stack>
                <Title order={5}>Neue VOD Kategorien</Title>
                <CategoryList categories={categoriesData.vod.new} onToggle={() => {}} />
                <Divider my="sm" />
                <Title order={5}>Bestehende VOD Kategorien</Title>
                <CategoryList categories={categoriesData.vod.existing} onToggle={() => {}} />
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="series">
              <Stack>
                <Title order={5}>Neue Serien Kategorien</Title>
                <CategoryList categories={categoriesData.series.new} onToggle={() => {}} />
                <Divider my="sm" />
                <Title order={5}>Bestehende Serien Kategorien</Title>
                <CategoryList categories={categoriesData.series.existing} onToggle={() => {}} />
              </Stack>
            </Tabs.Panel>

          </Box>
        </Tabs>
        
        <Group position="apart" mt="xl">
          <Box>
            {server && (
              <Button color="red" variant="subtle" leftSection={<Trash size={16} />} onClick={handleDelete}>
                Löschen
              </Button>
            )}
          </Box>
          <Group>
            <Button variant="default" onClick={onClose}>Abbrechen</Button>
            <Button type="submit" loading={loading} leftSection={<Save size={16} />}>Speichern</Button>
          </Group>
        </Group>
      </form>
    </Modal>
  );
}
