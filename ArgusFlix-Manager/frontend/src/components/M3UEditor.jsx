import React, { useEffect, useState } from 'react';
import { Box, Button, Group, Text, Accordion, Switch, Badge, Stack } from '@mantine/core';
import { Link2Off, RefreshCw } from 'lucide-react';
import useChannelsStore from '../store/channels';
import { showNotification } from '@mantine/notifications';
import api from '../api';

const M3UEditor = () => {
  const channelGroups = useChannelsStore((s) => s.channelGroups);
  const channels = useChannelsStore((s) => s.channels);
  const fetchChannelGroups = useChannelsStore((s) => s.fetchChannelGroups);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (channelGroups.length === 0) {
      fetchChannelGroups();
    }
  }, [channelGroups, fetchChannelGroups]);

  const handleDeadLinkCheck = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/v1/channels/m3u-editor/actions/dead-link-check/');
      showNotification({
        title: 'Erfolg',
        message: response.data.message || 'Dead-Link Check gestartet',
        color: 'green',
      });
    } catch (error) {
      showNotification({
        title: 'Fehler',
        message: 'Konnte Dead-Link Check nicht starten',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAutoEpgMatch = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/v1/channels/m3u-editor/actions/auto-epg-match/');
      showNotification({
        title: 'Erfolg',
        message: response.data.message || 'Auto-EPG Match gestartet',
        color: 'green',
      });
    } catch (error) {
      showNotification({
        title: 'Fehler',
        message: 'Konnte Auto-EPG Match nicht starten',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p="md" h="100%" display="flex" style={{ flexDirection: 'column' }}>
      <Group justify="space-between" mb="md">
        <Text size="xl" fw={700}>M3U Editor</Text>
        <Group>
          <Button 
            leftSection={<Link2Off size={16} />} 
            variant="light" 
            color="red"
            onClick={handleDeadLinkCheck}
            loading={loading}
          >
            Dead-Link Check
          </Button>
          <Button 
            leftSection={<RefreshCw size={16} />} 
            variant="light" 
            onClick={handleAutoEpgMatch}
            loading={loading}
          >
            Auto-EPG Match
          </Button>
        </Group>
      </Group>

      <Text size="sm" c="dimmed" mb="lg">
        Ziehe Kanäle per Drag & Drop in andere Gruppen. Bearbeite EPG-IDs und setze Kanäle auf versteckt.
      </Text>

      <Box style={{ flex: 1, overflowY: 'auto' }}>
        <Accordion variant="separated">
          {channelGroups.map(group => {
            const groupChannels = channels.filter(c => c.channel_group === group.id);
            return (
              <Accordion.Item key={group.id} value={group.id.toString()}>
                <Accordion.Control>
                  <Group justify="space-between">
                    <Text fw={500}>{group.name}</Text>
                    <Badge color="gray" variant="light">{groupChannels.length} Kanäle</Badge>
                  </Group>
                </Accordion.Control>
                <Accordion.Panel>
                  <Stack gap="xs">
                    {groupChannels.map(channel => (
                      <Group key={channel.id} justify="space-between" p="xs" style={{ border: '1px solid #eee', borderRadius: '4px' }}>
                        <Text size="sm">{channel.name}</Text>
                        <Group>
                          <Badge variant="dot" color={channel.tvg_id ? 'green' : 'red'}>
                            {channel.tvg_id || 'Kein EPG'}
                          </Badge>
                          <Switch 
                            checked={!channel.hidden_from_output} 
                            label="Sichtbar" 
                            size="sm"
                            readOnly
                          />
                        </Group>
                      </Group>
                    ))}
                  </Stack>
                </Accordion.Panel>
              </Accordion.Item>
            );
          })}
        </Accordion>
      </Box>
    </Box>
  );
};

export default M3UEditor;
