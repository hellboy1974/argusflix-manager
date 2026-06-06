import React, { useEffect, useState, Suspense } from 'react';
import {
  Box,
  Text,
  Group,
  Stack,
  Card,
  Badge,
  Button,
  Loader,
  Divider,
  Grid,
} from '@mantine/core';
import { Settings, Clock, RefreshCw } from 'lucide-react';
import { notifications } from '@mantine/notifications';
import api from '../api';
import ErrorBoundary from '../components/ErrorBoundary';
import ScheduleBuilderModal from '../components/modals/ScheduleBuilderModal';

const CronFormatBadge = ({ cron, interval }) => {
  if (cron) {
    return <Badge color="grape" variant="light">Cron: {cron}</Badge>;
  }
  if (interval > 0) {
    return <Badge color="blue" variant="light">Every {interval} hours</Badge>;
  }
  return <Badge color="red" variant="light">Disabled</Badge>;
};

const AutomationsContent = () => {
  const [epgs, setEpgs] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [pluginSettings, setPluginSettings] = useState({ refresh_interval_hours: 6, cron_expression: '' });
  const [scheduledPlugins, setScheduledPlugins] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal State
  const [modalOpened, setModalOpened] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [epgData, m3uData, repoData, pluginsData] = await Promise.all([
        api.getEPGs(),
        api.getPlaylists(),
        api.request('/api/plugins/repo-settings/'), // We fetch direct since it might not be in api.js wrappers yet
        api.getPlugins()
      ]);
      
      setEpgs(epgData || []);
      setPlaylists(m3uData || []);
      setPluginSettings(repoData || { refresh_interval_hours: 6, cron_expression: '' });
      
      // Filter plugins that have a cron schedule field
      const withSchedules = (pluginsData || []).filter(p => 
        p.fields && p.fields.some(f => f.id === 'cron_schedule' || f.id.includes('cron'))
      );
      setScheduledPlugins(withSchedules);
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to load automation data.', color: 'red' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const openScheduleModal = (item) => {
    setCurrentItem(item);
    setModalOpened(true);
  };

  const handleSaveSchedule = async (cron, interval) => {
    if (!currentItem) return;

    try {
      if (currentItem.type === 'epg') {
        await api.updateEPG({ id: currentItem.id, cron_expression: cron, refresh_interval: interval });
      } else if (currentItem.type === 'playlist') {
        // We pass id in the URL directly based on api.js logic
        await api.request(`/api/m3u/accounts/${currentItem.id}/`, {
          method: 'PATCH',
          body: { cron_expression: cron, refresh_interval: interval }
        });
      } else if (currentItem.type === 'repo') {
        await api.request('/api/plugins/repo-settings/', {
          method: 'PUT',
          body: { refresh_interval_hours: interval, cron_expression: cron }
        });
      } else if (currentItem.type === 'plugin_task') {
        // Find the cron field name
        const plugin = currentItem.plugin;
        const cronField = plugin.fields.find(f => f.id === 'cron_schedule' || f.id.includes('cron'));
        if (cronField) {
          const newSettings = { ...(plugin.settings || {}), [cronField.id]: cron };
          await api.updatePluginSettings(plugin.key, newSettings);
        }
      }

      notifications.show({ title: 'Success', message: 'Schedule updated successfully.', color: 'green' });
      fetchData();
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to update schedule.', color: 'red' });
    }
  };

  if (loading) {
    return (
      <Box h="100%" w="100%" display="flex" style={{ alignItems: 'center', justifyContent: 'center' }}>
        <Loader />
      </Box>
    );
  }

  return (
    <Box p={20}>
      <Group justify="space-between" mb="xl">
        <Group>
          <RefreshCw size={28} color="var(--mantine-color-blue-5)" />
          <Text size="xl" fw={600}>Automations Dashboard</Text>
        </Group>
      </Group>

      <Text c="dimmed" mb="xl">Manage the refresh schedules for your M3U Playlists, EPG Sources, and Plugins from a single dashboard.</Text>

      <Grid>
        {/* Playlists */}
        {playlists.map(pl => (
          <Grid.Col span={{ base: 12, md: 6, lg: 4 }} key={`pl-${pl.id}`}>
            <Card shadow="sm" p="lg" radius="md" withBorder>
              <Group justify="space-between" mb="xs">
                <Text fw={500}>{pl.name}</Text>
                <Badge color="blue" variant="filled">Playlist</Badge>
              </Group>
              <Group mb="md">
                <CronFormatBadge cron={pl.cron_expression} interval={pl.refresh_interval} />
              </Group>
              <Button variant="light" color="blue" fullWidth mt="md" radius="md" onClick={() => openScheduleModal({ ...pl, type: 'playlist' })}>
                <Clock size={16} style={{ marginRight: 8 }} /> Edit Schedule
              </Button>
            </Card>
          </Grid.Col>
        ))}

        {/* EPG Sources */}
        {epgs.map(epg => (
          <Grid.Col span={{ base: 12, md: 6, lg: 4 }} key={`epg-${epg.id}`}>
            <Card shadow="sm" p="lg" radius="md" withBorder>
              <Group justify="space-between" mb="xs">
                <Text fw={500}>{epg.name}</Text>
                <Badge color="green" variant="filled">EPG Source</Badge>
              </Group>
              <Group mb="md">
                <CronFormatBadge cron={epg.cron_expression} interval={epg.refresh_interval} />
              </Group>
              <Button variant="light" color="green" fullWidth mt="md" radius="md" onClick={() => openScheduleModal({ ...epg, type: 'epg' })}>
                <Clock size={16} style={{ marginRight: 8 }} /> Edit Schedule
              </Button>
            </Card>
          </Grid.Col>
        ))}

        {/* Plugin Repositories */}
        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <Card shadow="sm" p="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text fw={500}>Plugin Repositories</Text>
              <Badge color="grape" variant="filled">System</Badge>
            </Group>
            <Group mb="md">
              <CronFormatBadge cron={pluginSettings.cron_expression} interval={pluginSettings.refresh_interval_hours} />
            </Group>
            <Button variant="light" color="grape" fullWidth mt="md" radius="md" onClick={() => openScheduleModal({ id: 'plugins', name: 'Plugin Repositories', type: 'repo', cron_expression: pluginSettings.cron_expression, refresh_interval: pluginSettings.refresh_interval_hours })}>
              <Clock size={16} style={{ marginRight: 8 }} /> Edit Schedule
            </Button>
          </Card>
        </Grid.Col>

        {/* Individual Plugins */}
        {scheduledPlugins.map(plugin => {
          const cronField = plugin.fields.find(f => f.id === 'cron_schedule' || f.id.includes('cron'));
          const currentCron = plugin.settings?.[cronField.id] || cronField.default;
          
          return (
            <Grid.Col span={{ base: 12, md: 6, lg: 4 }} key={`plugin-${plugin.key}`}>
              <Card shadow="sm" p="lg" radius="md" withBorder>
                <Group justify="space-between" mb="xs">
                  <Text fw={500}>{plugin.name}</Text>
                  <Badge color="orange" variant="filled">Plugin</Badge>
                </Group>
                <Group mb="md">
                  <CronFormatBadge cron={currentCron} interval={0} />
                </Group>
                <Button variant="light" color="orange" fullWidth mt="md" radius="md" onClick={() => openScheduleModal({ id: plugin.key, name: plugin.name, type: 'plugin_task', cron_expression: currentCron, refresh_interval: 0, plugin: plugin })}>
                  <Clock size={16} style={{ marginRight: 8 }} /> Edit Schedule
                </Button>
              </Card>
            </Grid.Col>
          );
        })}
      </Grid>

      <ScheduleBuilderModal
        opened={modalOpened}
        onClose={() => setModalOpened(false)}
        onSave={handleSaveSchedule}
        title={`Edit Schedule for ${currentItem?.name || ''}`}
        initialCron={currentItem?.cron_expression}
        initialInterval={currentItem?.refresh_interval}
      />
    </Box>
  );
};

const Automations = () => {
  return (
    <ErrorBoundary>
      <AutomationsContent />
    </ErrorBoundary>
  );
};

export default Automations;
