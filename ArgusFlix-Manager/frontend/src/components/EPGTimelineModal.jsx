import React, { useEffect, useState } from 'react';
import { Modal, Box, Text, Group, Stack, Badge, Loader, ScrollArea } from '@mantine/core';
import { Calendar } from 'lucide-react';
import { format } from '../utils/dateTimeUtils.js';
import api from '../api';
import useEPGsStore from '../store/epgs';

const EPGTimelineModal = ({ opened, onClose, tvg, channel }) => {
  const epgs = useEPGsStore((s) => s.epgs);
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (opened && tvg) {
      fetchPrograms();
    }
  }, [opened, tvg]);

  const fetchPrograms = async () => {
    setLoading(true);
    try {
      // Use the API to fetch programs for the given epg_data_id
      const response = await api.getCurrentProgramForEpg(tvg.id);
      
      // The backend batch endpoint returns a list of matched programs
      if (response && response.length > 0 && !response[0].parsing) {
        setPrograms(response);
      } else {
        setPrograms([]);
      }
    } catch (e) {
      console.error('Failed to fetch programs for EPG inspector', e);
      setPrograms([]);
    } finally {
      setLoading(false);
    }
  };

  const getOffsetTime = (timeStr) => {
    if (!timeStr) return null;
    const date = new Date(timeStr);
    
    // Calculate total offset
    const sourceOffset = epgs[tvg?.epg_source]?.time_offset_minutes || 0;
    const channelOffset = channel?.epg_time_offset_minutes || 0;
    const totalOffsetMs = (sourceOffset + channelOffset) * 60000;
    
    return new Date(date.getTime() + totalOffsetMs);
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={<Group><Calendar size={20} /><Text fw={500}>EPG Inspector: {tvg?.name}</Text></Group>}
      size="lg"
    >
      {loading ? (
        <Group justify="center" p="xl">
          <Loader size="sm" />
          <Text size="sm" c="dimmed">Loading EPG Data...</Text>
        </Group>
      ) : programs.length > 0 ? (
        <ScrollArea h={400} offsetScrollbars>
          <Stack gap="md">
            {programs.map((prog, idx) => (
              <Box key={idx} p="sm" style={{ borderLeft: '3px solid var(--mantine-color-blue-6)', backgroundColor: 'var(--mantine-color-dark-6)' }}>
                <Group justify="space-between" mb="xs">
                  <Text fw={500}>{prog.title}</Text>
                  <Group gap="xs">
                    <Badge variant="light" color="blue">
                      {format(getOffsetTime(prog.start_time), 'HH:mm')}
                    </Badge>
                    <Text size="xs" c="dimmed">-</Text>
                    <Badge variant="light" color="blue">
                      {format(getOffsetTime(prog.end_time), 'HH:mm')}
                    </Badge>
                  </Group>
                </Group>
                {prog.desc && <Text size="sm" c="dimmed" lineClamp={3}>{prog.desc}</Text>}
              </Box>
            ))}
          </Stack>
        </ScrollArea>
      ) : (
        <Box p="xl" ta="center">
          <Text c="dimmed">No programs found for this EPG data right now.</Text>
        </Box>
      )}
    </Modal>
  );
};

export default EPGTimelineModal;
