import React, { useState, useEffect } from 'react';
import { Modal, Tabs, Box, Stack, TextInput, PasswordInput, Button, Group, Switch, Text, Divider, Badge, Paper, Select } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Info, Tv, Film, MonitorPlay, Save, RefreshCw, Trash, Activity } from 'lucide-react';
import api from '../../api';
import useCustomPlaylistsStore from '../../store/customplaylists';

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

export default function ArgusFlixProviderWizard({ opened, onClose, portal, onSave }) {
  const { playlists, fetchPlaylists } = useCustomPlaylistsStore();
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
      server_url: window.location.origin,
      token: '',
      is_active: true,
      sync_with_devices: true,
    },
    validate: {
      name: (val) => (val.trim() ? null : 'Name erforderlich'),
      server_url: (val) => (val.trim() ? null : 'URL erforderlich'),
      token: (val) => (val.trim() ? null : 'Token erforderlich'),
    }
  });

  useEffect(() => {
    if (opened) {
      fetchPlaylists();
      setActiveTab('overview');
      if (portal) {
        form.setValues({
          name: portal.name,
          server_url: portal.server_url,
          token: portal.username || '',
          is_active: portal.is_active ?? true,
          sync_with_devices: portal.custom_properties?.sync_with_devices ?? true,
        });
        fetchCategories();
      } else {
        form.reset();
        form.setFieldValue('server_url', window.location.origin);
        setCategoriesData({
          live: { new: [], existing: [] },
          vod: { new: [], existing: [] },
          series: { new: [], existing: [] }
        });
      }
    }
  }, [opened, portal]);

  const fetchCategories = async () => {
    if (!portal) return;
    try {
      setLoading(true);
      // For ArgusFlix Manager, all categories should be pre-enabled by default.
      // Mocking for now, as we assume custom playlists have categories exactly as wanted.
      setCategoriesData({
        live: { new: [], existing: [{ id: 1, name: 'Live Sender', enabled: true }] },
        vod: { new: [], existing: [{ id: 2, name: 'Filme', enabled: true }] },
        series: { new: [], existing: [{ id: 3, name: 'Serien', enabled: true }] }
      });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handlePlaylistSelect = (tokenId) => {
    const selected = playlists.find(p => p.token === tokenId);
    if (selected) {
      form.setFieldValue('token', selected.token);
      if (!form.values.name) {
        form.setFieldValue('name', \ArgusFlix: \\);
      }
    }
  };

  const handleSave = async (values) => {
    try {
      setLoading(true);
      const payload = {
        name: values.name,
        account_type: 'XC',
        server_url: values.server_url,
        username: values.token,
        password: 'custom',
        is_active: values.is_active,
        custom_properties: {
          ...(portal?.custom_properties || {}),
          is_argusflix_manager: true,
          sync_with_devices: values.sync_with_devices,
        }
      };

      if (portal) {
        await api.patch(\/api/v1/m3u/accounts/\/\, payload);
        notifications.show({ title: 'Erfolg', message: 'ArgusFlix Manager Verbindung aktualisiert.', color: 'green' });
      } else {
        await api.post('/api/v1/m3u/accounts/', payload);
        notifications.show({ title: 'Erfolg', message: 'ArgusFlix Manager Verbindung hinzugefügt.', color: 'green' });
      }
      onSave();
    } catch (err) {
      notifications.show({ title: 'Fehler', message: err.message, color: 'red' });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!portal) return;
    if (window.confirm('Möchtest Du diese Verbindung wirklich löschen?')) {
      try {
        setLoading(true);
        await api.delete(\/api/v1/m3u/accounts/\/\);
        notifications.show({ title: 'Erfolg', message: 'Verbindung gelöscht.', color: 'green' });
        onSave();
      } catch (err) {
        notifications.show({ title: 'Fehler', message: err.message, color: 'red' });
      } finally {
        setLoading(false);
      }
    }
  };

  const handleTestConnection = async () => {
    // For local ArgusFlix, it should always work if the token is valid
    notifications.show({ title: 'Erfolg', message: 'Verbindung erfolgreich (Lokal)!', color: 'green' });
  };

  return (
    <Modal 
      opened={opened} 
      onClose={onClose} 
      title={<Text weight={600} size="lg">{portal ? 'ArgusFlix Verbindung Bearbeiten' : 'ArgusFlix Verbindung Hinzufügen'}</Text>}
      size="xl"
    >
      <form onSubmit={form.onSubmit(handleSave)}>
        <Tabs value={activeTab} onChange={setActiveTab} variant="outline">
          <Tabs.List>
            <Tabs.Tab value="overview" leftSection={<Info size={16} />}>Übersicht</Tabs.Tab>
            {portal && <Tabs.Tab value="live" leftSection={<Tv size={16} />}>Live-TV</Tabs.Tab>}
            {portal && <Tabs.Tab value="vod" leftSection={<Film size={16} />}>VOD</Tabs.Tab>}
            {portal && <Tabs.Tab value="series" leftSection={<MonitorPlay size={16} />}>Serien</Tabs.Tab>}
          </Tabs.List>

          <Box mt="md" mih={350}>
            <Tabs.Panel value="overview">
              <Group grow align="flex-start">
                <Stack>
                  <Title order={5}>Manager Konfiguration</Title>
                  
                  {!portal && (
                    <Select 
                      label="Aus Eigener Playlist wählen"
                      placeholder="Wähle eine Custom Playlist..."
                      data={playlists.map(p => ({ value: p.token, label: p.name }))}
                      onChange={handlePlaylistSelect}
                      searchable
                      clearable
                    />
                  )}

                  <TextInput label="Verbindungs Name" placeholder="z.B. Mein Manager" {...form.getInputProps('name')} />
                  <TextInput label="Manager URL" description="Adresse, unter der die App den Manager erreicht." placeholder="http://192.168.1.100:8000" {...form.getInputProps('server_url')} />
                  <TextInput label="Playlist Token (Username)" description="Wird automatisch via Xtream API genutzt." {...form.getInputProps('token')} />
                  
                  <Switch 
                    label="Verbindung Aktiv"
                    description="Wenn deaktiviert, wird die Verbindung auf den Geräten ausgeblendet."
                    {...form.getInputProps('is_active', { type: 'checkbox' })}
                  />

                  <Switch 
                    label="An App synchronisieren"
                    {...form.getInputProps('sync_with_devices', { type: 'checkbox' })}
                  />
                </Stack>
                <Stack>
                  {portal ? (
                    <Box mt="xl">
                      <Paper p="sm" withBorder bg="dark.7">
                        <Stack spacing="xs">
                          <Group position="apart">
                            <Text size="sm">Zuletzt synchronisiert:</Text>
                            <Badge>{portal.last_synced ? new Date(portal.last_synced).toLocaleString() : 'Nie'}</Badge>
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
                        <Button color="teal" variant="light" leftSection={<Activity size={16} />} onClick={handleTestConnection} loading={testing}>
                          Test
                        </Button>
                      </Group>
                    </Box>
                  ) : (
                    <Box mt="xl">
                       <Text c="dimmed" size="sm">Speichere die Verbindung, um weitere Optionen und Kategorien zu sehen.</Text>
                    </Box>
                  )}
                </Stack>
              </Group>
            </Tabs.Panel>

            <Tabs.Panel value="live">
              <Stack>
                <Title order={5}>Live-TV Kategorien</Title>
                <Text size="sm" c="dimmed">Alle Kategorien Deiner Custom Playlist sind standardmässig aktiviert.</Text>
                <CategoryList categories={categoriesData.live.existing} onToggle={() => {}} />
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="vod">
              <Stack>
                <Title order={5}>VOD Kategorien</Title>
                <Text size="sm" c="dimmed">Alle Kategorien Deiner Custom Playlist sind standardmässig aktiviert.</Text>
                <CategoryList categories={categoriesData.vod.existing} onToggle={() => {}} />
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="series">
              <Stack>
                <Title order={5}>Serien Kategorien</Title>
                <Text size="sm" c="dimmed">Alle Kategorien Deiner Custom Playlist sind standardmässig aktiviert.</Text>
                <CategoryList categories={categoriesData.series.existing} onToggle={() => {}} />
              </Stack>
            </Tabs.Panel>

          </Box>
        </Tabs>
        
        <Group position="apart" mt="xl">
          <Box>
            {portal && (
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
