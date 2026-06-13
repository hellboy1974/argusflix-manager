import React, { useState, useEffect } from 'react';
import { Modal, Tabs, Box, Stack, TextInput, Button, Group, Switch, Text, Divider, Badge, Paper, Select } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Info, Tv, Film, MonitorPlay, Save, RefreshCw, Trash } from 'lucide-react';
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

export default function StalkerProviderWizard({ opened, onClose, portal, onSave }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [categoriesData, setCategoriesData] = useState({
    live: { new: [], existing: [] },
    vod: { new: [], existing: [] },
    series: { new: [], existing: [] }
  });

  const form = useForm({
    initialValues: {
      name: '',
      server_url: '',
      mac: '',
      sync_policy: 'manual',
      sync_with_devices: true,
      is_active: true,
      serial_number1: '',
      serial_number2: '',
      signature: '',
    },
    validate: {
      name: (val) => (val.trim() ? null : 'Name erforderlich'),
      server_url: (val) => (val.trim() ? null : 'URL erforderlich'),
      mac: (val) => (val.trim() ? null : 'MAC-Adresse erforderlich'),
    }
  });

  useEffect(() => {
    if (opened) {
      setActiveTab('overview');
      if (portal) {
        form.setValues({
          name: portal.name,
          server_url: portal.server_url,
          mac: portal.custom_properties?.mac || '',
          sync_policy: portal.sync_policy || 'manual',
          sync_with_devices: portal.sync_with_devices ?? true,
          is_active: portal.is_active ?? true,
          serial_number1: portal.custom_properties?.serial_number1 || '',
          serial_number2: portal.custom_properties?.serial_number2 || '',
          signature: portal.custom_properties?.signature || '',
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
  }, [opened, portal]);

  const fetchCategories = async () => {
    if (!portal) return;
    try {
      setLoading(true);
      const [channelsRes, vodRes] = await Promise.all([
        api.get('/api/v1/channel-groups/'),
        api.get('/api/v1/vod-categories/')
      ]);
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
        name: values.name.startsWith('Stalker:') ? values.name : Stalker: \,
        server_url: values.server_url,
        sync_policy: values.sync_policy,
        sync_with_devices: values.sync_with_devices,
        is_active: values.is_active,
        account_type: 'STD',
        custom_properties: {
          ...(portal?.custom_properties || {}),
          mac: values.mac,
          serial_number1: values.serial_number1,
          serial_number2: values.serial_number2,
          signature: values.signature,
        }
      };

      if (portal) {
        await api.patch(\/api/v1/m3u-accounts/\/\, payload);
        notifications.show({ title: 'Erfolg', message: 'Portal gespeichert.', color: 'green' });
      } else {
        await api.post('/api/v1/m3u-accounts/', payload);
        notifications.show({ title: 'Erfolg', message: 'Portal hinzugefügt.', color: 'green' });
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
    if (window.confirm('Möchtest Du dieses Portal wirklich löschen?')) {
      try {
        setLoading(true);
        await api.delete(\/api/v1/m3u-accounts/\/\);
        notifications.show({ title: 'Erfolg', message: 'Portal gelöscht.', color: 'green' });
        onSave();
      } catch (err) {
        notifications.show({ title: 'Fehler', message: err.message, color: 'red' });
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Modal 
      opened={opened} 
      onClose={onClose} 
      title={<Text weight={600} size="lg">{portal ? 'Stalker Portal Bearbeiten' : 'Stalker Portal Hinzufügen'}</Text>}
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
                  <Title order={5}>Portal Informationen</Title>
                  <TextInput label="Profilname" placeholder="z.B. Mein Provider" {...form.getInputProps('name')} />
                  <TextInput label="Portal URL" placeholder="http://mag.provider.com/c/" {...form.getInputProps('server_url')} />
                  <TextInput label="MAC-Adresse" placeholder="00:1A:79:..." {...form.getInputProps('mac')} />
                  
                  <Switch 
                    label="Verbindung Aktiv"
                    description="Wenn deaktiviert, wird das Portal nicht mehr synchronisiert oder angezeigt."
                    {...form.getInputProps('is_active', { type: 'checkbox' })}
                  />

                  <Select 
                    label="Synchronisations-Richtlinie"
                    data={[
                      { value: 'auto_on_startup', label: 'Beim Starten synchronisieren' },
                      { value: 'manual', label: 'Nur Manuell' }
                    ]}
                    {...form.getInputProps('sync_policy')}
                  />
                  <Switch 
                    label="Mit Manager/Geräten synchronisieren"
                    {...form.getInputProps('sync_with_devices', { type: 'checkbox' })}
                  />
                </Stack>
                <Stack>
                  <Title order={5}>Optionale Geräte-Infos (Emulation)</Title>
                  <TextInput label="Seriennummer 1" placeholder="Optional" {...form.getInputProps('serial_number1')} />
                  <TextInput label="Seriennummer 2" placeholder="Optional" {...form.getInputProps('serial_number2')} />
                  <TextInput label="Signatur" placeholder="Optional" {...form.getInputProps('signature')} />

                  {portal && (
                    <Box mt="xl">
                      <Paper p="sm" withBorder bg="dark.7">
                        <Stack spacing="xs">
                          <Group position="apart">
                            <Text size="sm">Zuletzt synchronisiert:</Text>
                            <Badge>{portal.updated_at ? new Date(portal.updated_at).toLocaleString() : 'Nie'}</Badge>
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
                      <Button fullWidth mt="sm" variant="light" leftSection={<RefreshCw size={16} />}>
                        Jetzt Synchronisieren
                      </Button>
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
