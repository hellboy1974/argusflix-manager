import React, { useState, useEffect } from 'react';
import {
  TextInput,
  Button,
  Group,
  Stack,
  Text,
  Paper,
  Divider,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import api from '../../../api';

const MetadataSettingsForm = ({ active }) => {
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const [formData, setFormData] = useState({
    tmdb_api_key: '',
    omdb_api_key: '',
    language: 'de-DE',
    provider_priority: ['tmdb', 'omdb']
  });

  useEffect(() => {
    if (active) {
      loadSettings();
    }
  }, [active]);

  const loadSettings = async () => {
    setLoading(true);
    try {
      const { data } = await api.getCoreSettings();
      const metadataSettings = data.find(s => s.key === 'metadata_settings');
      if (metadataSettings && metadataSettings.value) {
        setFormData({
          ...formData,
          ...metadataSettings.value
        });
      }
    } catch (error) {
      console.error('Failed to load metadata settings:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to load metadata settings',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const { data } = await api.getCoreSettings();
      const metadataSettings = data.find(s => s.key === 'metadata_settings');
      
      if (metadataSettings) {
        await api.updateCoreSetting(metadataSettings.id, {
          key: 'metadata_settings',
          name: 'Metadata Settings',
          value: formData,
        });
      } else {
        await api.createCoreSetting({
          key: 'metadata_settings',
          name: 'Metadata Settings',
          value: formData,
        });
      }

      notifications.show({
        title: 'Success',
        message: 'Metadata settings saved successfully',
        color: 'green',
      });
    } catch (error) {
      console.error('Failed to save metadata settings:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to save metadata settings',
        color: 'red',
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack spacing="md">
        <Text size="sm" color="dimmed">
          Configure external metadata providers to automatically fetch rich metadata (posters, genres, ratings, descriptions) for Movies and Series.
        </Text>

        <Paper withBorder p="md" radius="md">
          <Stack spacing="sm">
            <Text weight={500} size="lg">TMDB (The Movie Database)</Text>
            <Text size="xs" color="dimmed">Priority 1 Provider. Highly recommended for rich metadata and posters.</Text>
            <TextInput
              label="API Key"
              placeholder="Enter your TMDB v3 API Key"
              value={formData.tmdb_api_key}
              onChange={(e) => setFormData({ ...formData, tmdb_api_key: e.target.value })}
              description="You can get a free API key at themoviedb.org"
            />
            <TextInput
              label="Language Code"
              placeholder="e.g. de-DE, en-US"
              value={formData.language}
              onChange={(e) => setFormData({ ...formData, language: e.target.value })}
            />
          </Stack>
        </Paper>

        <Paper withBorder p="md" radius="md">
          <Stack spacing="sm">
            <Text weight={500} size="lg">OMDb (Open Movie Database)</Text>
            <Text size="xs" color="dimmed">Priority 2 Provider. Excellent for real IMDb ratings.</Text>
            <TextInput
              label="API Key"
              placeholder="Enter your OMDb API Key"
              value={formData.omdb_api_key}
              onChange={(e) => setFormData({ ...formData, omdb_api_key: e.target.value })}
              description="You can get a free API key at omdbapi.com"
            />
          </Stack>
        </Paper>

        <Divider />

        <Group position="right">
          <Button 
            type="submit" 
            loading={saving} 
            disabled={loading}
          >
            Save Settings
          </Button>
        </Group>
      </Stack>
    </form>
  );
};

export default MetadataSettingsForm;
