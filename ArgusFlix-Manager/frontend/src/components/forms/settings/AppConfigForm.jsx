import React, { useState, useEffect } from 'react';
import {
  Box,
  Title,
  Text,
  Select,
  Switch,
  Group,
  Stack,
  Button,
  NumberInput,
  Divider,
  Paper,
  Tabs,
  Loader
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Save, Smartphone, Settings as SettingsIcon, PlaySquare, Shield, Tv } from 'lucide-react';
import api from '../../../api';

export default function AppConfigForm() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const form = useForm({
    initialValues: {
      appLanguage: 'en',
      parentalControlLevel: 0,
      hasParentalPin: false,
      playerDecoderMode: 'HARDWARE',
      playerSurfaceMode: 'SURFACE_VIEW',
      vodViewMode: 'GRID',
      liveTvChannelMode: 'LIST',
      liveChannelGroupingMode: 'FLAT',
    },
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const res = await api.get('/api/v1/core/app-settings/');
      // API returns an object or a list. Based on our ViewSet, list returns a single object payload
      if (res.data) {
        form.setValues(res.data);
      }
    } catch (err) {
      console.error(err);
      notifications.show({
        title: 'Fehler',
        message: 'Konnte App-Einstellungen nicht laden.',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (values) => {
    try {
      setSaving(true);
      // Our API supports create/patch for the singleton
      await api.post('/api/v1/core/app-settings/', values);
      notifications.show({
        title: 'Gespeichert',
        message: 'Globale App-Einstellungen wurden erfolgreich gespeichert.',
        color: 'green',
      });
    } catch (err) {
      console.error(err);
      notifications.show({
        title: 'Fehler',
        message: 'Beim Speichern ist ein Fehler aufgetreten.',
        color: 'red',
      });
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Box p="md"><Loader /></Box>;

  return (
    <Box>
      <Group position="apart" mb="md">
        <Box>
          <Title order={3}>ArgusFlix App Konfiguration</Title>
          <Text c="dimmed" size="sm">
            Diese Einstellungen werden global für alle verbundenen Android-TV Apps synchronisiert.
          </Text>
        </Box>
        <Button
          leftSection={<Save size={16} />}
          onClick={() => handleSave(form.values)}
          loading={saving}
        >
          Speichern
        </Button>
      </Group>

      <Paper p="md" withBorder>
        <Tabs defaultValue="general" orientation="vertical">
          <Tabs.List>
            <Tabs.Tab value="general" leftSection={<SettingsIcon size={16} />}>Allgemein</Tabs.Tab>
            <Tabs.Tab value="player" leftSection={<PlaySquare size={16} />}>Player</Tabs.Tab>
            <Tabs.Tab value="ui" leftSection={<Tv size={16} />}>Oberfläche</Tabs.Tab>
            <Tabs.Tab value="parental" leftSection={<Shield size={16} />}>Jugendschutz</Tabs.Tab>
          </Tabs.List>

          <Tabs.Panel value="general" pl="md">
            <Stack>
              <Title order={5}>Allgemeine Einstellungen</Title>
              <Select
                label="App Sprache"
                description="Erzwingt eine bestimmte Sprache auf den Endgeräten"
                data={[
                  { value: 'en', label: 'English' },
                  { value: 'de', label: 'Deutsch' },
                  { value: 'es', label: 'Español' },
                ]}
                {...form.getInputProps('appLanguage')}
              />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="player" pl="md">
            <Stack>
              <Title order={5}>Player Einstellungen</Title>
              <Select
                label="Decoder Modus"
                data={[
                  { value: 'HARDWARE', label: 'Hardware-Beschleunigung (Empfohlen)' },
                  { value: 'SOFTWARE', label: 'Software-Decoding' },
                  { value: 'AUTO', label: 'Automatisch' }
                ]}
                {...form.getInputProps('playerDecoderMode')}
              />
              <Select
                label="Surface Modus"
                data={[
                  { value: 'SURFACE_VIEW', label: 'SurfaceView (Bessere Leistung)' },
                  { value: 'TEXTURE_VIEW', label: 'TextureView (Bessere UI-Integration)' }
                ]}
                {...form.getInputProps('playerSurfaceMode')}
              />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="ui" pl="md">
            <Stack>
              <Title order={5}>Live-TV & VOD Darstellung</Title>
              <Select
                label="VOD Ansicht"
                data={[
                  { value: 'GRID', label: 'Kachel-Ansicht (Grid)' },
                  { value: 'LIST', label: 'Listen-Ansicht' }
                ]}
                {...form.getInputProps('vodViewMode')}
              />
              <Select
                label="Live-TV Listen-Ansicht"
                data={[
                  { value: 'LIST', label: 'Klassische Liste' },
                  { value: 'GUIDE', label: 'EPG Guide Ansicht' }
                ]}
                {...form.getInputProps('liveTvChannelMode')}
              />
              <Select
                label="Kanalgruppierung"
                data={[
                  { value: 'FLAT', label: 'Flache Liste' },
                  { value: 'CATEGORIES', label: 'Nach Kategorien sortiert' }
                ]}
                {...form.getInputProps('liveChannelGroupingMode')}
              />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="parental" pl="md">
            <Stack>
              <Title order={5}>Jugendschutz-Einstellungen</Title>
              <Switch
                label="Jugendschutz-PIN erforderlich"
                description="Wenn aktiviert, muss beim Profilwechsel ein PIN eingegeben werden."
                {...form.getInputProps('hasParentalPin', { type: 'checkbox' })}
              />
              <NumberInput
                label="Standard Jugendschutz-Level"
                description="Maximal erlaubte FSK / USK Stufe (0 = uneingeschränkt)"
                min={0}
                max={18}
                {...form.getInputProps('parentalControlLevel')}
              />
            </Stack>
          </Tabs.Panel>
        </Tabs>
      </Paper>
    </Box>
  );
}
