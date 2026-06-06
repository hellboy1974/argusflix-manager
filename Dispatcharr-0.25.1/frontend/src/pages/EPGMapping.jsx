import React, { useEffect, useState, useMemo, useCallback } from 'react';
import {
  Box,
  Text,
  TextInput,
  Group,
  Stack,
  Badge,
  ScrollArea,
  Button,
  ActionIcon,
  Select,
  Switch,
  Flex,
  Paper,
  Divider,
  Checkbox,
  Slider,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Search, Zap, Link, Tv, AlertCircle } from 'lucide-react';
import { Allotment } from 'allotment';
import 'allotment/dist/style.css';
import { FixedSizeList as List } from 'react-window';

import useChannelsStore from '../store/channels';
import useEPGsStore from '../store/epgs';
import api from '../api';
import ErrorBoundary from '../components/ErrorBoundary';

const EPGMappingContent = () => {
  // Zustand Stores
  const channels = useChannelsStore((s) => s.channels);
  const fetchChannels = useChannelsStore((s) => s.fetchChannels);
  const channelGroups = useChannelsStore((s) => s.channelGroups);
  const fetchChannelGroups = useChannelsStore((s) => s.fetchChannelGroups);

  const tvgs = useEPGsStore((s) => s.tvgs);
  const epgs = useEPGsStore((s) => s.epgs);
  const fetchEPGs = useEPGsStore((s) => s.fetchEPGs);
  const fetchEPGData = useEPGsStore((s) => s.fetchEPGData);

  // Local State
  const [selectedChannel, setSelectedChannel] = useState(null);
  const [channelSearch, setChannelSearch] = useState('');
  const [epgSearch, setEpgSearch] = useState('');
  const [filterGroup, setFilterGroup] = useState('all');
  const [filterUnmappedOnly, setFilterUnmappedOnly] = useState(true);
  const [epgSourceFilter, setEpgSourceFilter] = useState('all');
  
  const [isUpdating, setIsUpdating] = useState(false);
  const [selectedChannelIds, setSelectedChannelIds] = useState(new Set());
  const [matchThreshold, setMatchThreshold] = useState(85);

  // Initial Load
  useEffect(() => {
    fetchChannels();
    fetchChannelGroups();
    fetchEPGs();
    fetchEPGData();
  }, [fetchChannels, fetchChannelGroups, fetchEPGs, fetchEPGData]);

  // Derived Data
  const channelList = useMemo(() => {
    return Object.values(channels).filter((c) => {
      // 1. Filter by unmapped
      if (filterUnmappedOnly && c.epg_data_id) return false;
      // 2. Filter by Group
      if (filterGroup !== 'all' && String(c.channel_group_id) !== filterGroup) return false;
      // 3. Filter by Search
      if (channelSearch) {
        const searchLower = channelSearch.toLowerCase();
        return c.name?.toLowerCase().includes(searchLower) || c.tvg_id?.toLowerCase().includes(searchLower);
      }
      return true;
    }).sort((a, b) => a.name.localeCompare(b.name));
  }, [channels, filterUnmappedOnly, filterGroup, channelSearch]);

  const epgList = useMemo(() => {
    return tvgs.filter((tvg) => {
      // 1. Filter by EPG Source
      if (epgSourceFilter !== 'all') {
        if (epgSourceFilter.startsWith('group:')) {
          const grpName = epgSourceFilter.substring(6);
          const source = epgs[tvg.epg_source];
          if (!source || source.group_name !== grpName) return false;
        } else {
          if (String(tvg.epg_source) !== epgSourceFilter) return false;
        }
      }
      // 2. Filter by Search
      if (epgSearch) {
        const searchLower = epgSearch.toLowerCase();
        return tvg.name?.toLowerCase().includes(searchLower) || tvg.tvg_id?.toLowerCase().includes(searchLower);
      }
      return true;
    });
  }, [tvgs, epgs, epgSourceFilter, epgSearch]);

  // Options for dropdowns
  const groupOptions = useMemo(() => {
    const opts = [{ value: 'all', label: 'All Groups' }];
    Object.values(channelGroups).forEach(g => {
      opts.push({ value: String(g.id), label: g.name });
    });
    return opts;
  }, [channelGroups]);

  const sourceOptions = useMemo(() => {
    const opts = [{ value: 'all', label: 'All Sources' }];
    const addedGroups = new Set();
    Object.values(epgs).forEach(source => {
      if (source.group_name && source.group_name.trim() !== '') {
        const grp = source.group_name.trim();
        if (!addedGroups.has(grp)) {
          addedGroups.add(grp);
          opts.push({ value: `group:${grp}`, label: `Group: ${grp}` });
        }
      } else {
        opts.push({ value: String(source.id), label: source.name });
      }
    });
    return opts;
  }, [epgs]);

  // Actions
  const handleSelectChannel = (channel) => {
    setSelectedChannel(channel);
    // Auto-fill EPG search with channel name for quick matching
    setEpgSearch(channel.name);
  };

  const toggleChannelSelection = (id) => {
    const newSelected = new Set(selectedChannelIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedChannelIds(newSelected);
  };

  const handleSelectAllVisible = () => {
    if (selectedChannelIds.size === channelList.length) {
      setSelectedChannelIds(new Set());
    } else {
      const allIds = channelList.map((c) => c.id);
      setSelectedChannelIds(new Set(allIds));
    }
  };

  const handleAssignEPG = async (tvg) => {
    if (!selectedChannel) return;
    setIsUpdating(true);
    try {
      await api.updateChannel({
        id: selectedChannel.id,
        epg_data_id: tvg.id,
      });
      notifications.show({
        title: 'Mapped Successfully',
        message: `${selectedChannel.name} mapped to ${tvg.name}`,
        color: 'green'
      });
      fetchChannels(); // Refresh channel state
      // Move to next unmapped channel
      const currentIndex = channelList.findIndex(c => c.id === selectedChannel.id);
      if (currentIndex !== -1 && currentIndex + 1 < channelList.length) {
        handleSelectChannel(channelList[currentIndex + 1]);
      } else {
        setSelectedChannel(null);
        setEpgSearch('');
      }
    } catch (e) {
      notifications.show({
        title: 'Error',
        message: 'Failed to assign EPG data',
        color: 'red'
      });
    } finally {
      setIsUpdating(false);
    }
  };

  const handleClearEPG = async (channel) => {
    try {
      await api.updateChannel({
        id: channel.id,
        epg_data_id: null,
      });
      notifications.show({ title: 'Unmapped', message: `Cleared EPG for ${channel.name}` });
      fetchChannels();
    } catch (e) {
      console.error(e);
    }
  };

  const handleSmartMatch = async () => {
    setIsUpdating(true);
    try {
      let channelsToMatch = [];
      if (selectedChannelIds.size > 0) {
        channelsToMatch = Array.from(selectedChannelIds);
      } else {
        // If nothing is explicitly checked, match all visible UNMAPPED channels
        channelsToMatch = channelList
          .filter((c) => !c.epg_data_id)
          .map((c) => c.id);
      }

      if (channelsToMatch.length === 0) {
        notifications.show({
          title: 'Info',
          message: 'No unmapped channels to match.',
          color: 'blue',
        });
        setIsUpdating(false);
        return;
      }

      const response = await api.smartMatchEPG(channelsToMatch, matchThreshold);
      
      notifications.show({
        title: 'Smart Match Complete',
        message: response.message || `Matching finished.`,
        color: response.matched_count > 0 ? 'green' : 'orange',
      });
      
      fetchChannels();
      setSelectedChannelIds(new Set()); // clear selection
    } catch (e) {
      console.error(e);
    } finally {
      setIsUpdating(false);
    }
  };

  // Render Rows
  const ChannelRow = ({ index, style }) => {
    const channel = channelList[index];
    const isSelected = selectedChannel?.id === channel.id;
    return (
      <div style={style}>
        <Box
          p="xs"
          mb={4}
          onClick={() => handleSelectChannel(channel)}
          style={{
            cursor: 'pointer',
            backgroundColor: isSelected ? 'var(--mantine-color-blue-9)' : 'var(--mantine-color-dark-6)',
            borderRadius: '4px',
            border: isSelected ? '1px solid var(--mantine-color-blue-5)' : '1px solid transparent',
          }}
        >
          <Group justify="space-between" wrap="nowrap">
            <Group gap="xs" wrap="nowrap" style={{ overflow: 'hidden' }}>
              <Checkbox
                size="xs"
                checked={selectedChannelIds.has(channel.id)}
                onChange={() => toggleChannelSelection(channel.id)}
                onClick={(e) => e.stopPropagation()} // Prevent row click from firing
              />
              <Box style={{ overflow: 'hidden' }}>
                <Text size="sm" fw={500} truncate>{channel.name}</Text>
                <Text size="xs" c="dimmed" truncate>
                  Group: {channelGroups[channel.channel_group_id]?.name || 'None'}
                </Text>
              </Box>
            </Group>
            {channel.epg_data_id ? (
              <Badge color="green" variant="light" size="xs">Mapped</Badge>
            ) : (
              <Badge color="red" variant="light" size="xs">Unmapped</Badge>
            )}
          </Group>
        </Box>
      </div>
    );
  };

  const EPGRow = ({ index, style }) => {
    const tvg = epgList[index];
    return (
      <div style={style}>
        <Box
          p="xs"
          mb={4}
          style={{
            backgroundColor: 'var(--mantine-color-dark-6)',
            borderRadius: '4px',
            border: '1px solid transparent',
          }}
        >
          <Group justify="space-between" wrap="nowrap">
            <Box style={{ overflow: 'hidden', flex: 1 }}>
              <Text size="sm" fw={500} truncate>{tvg.name}</Text>
              <Text size="xs" c="dimmed" truncate>{tvg.tvg_id}</Text>
            </Box>
            <Button 
              size="xs" 
              variant="light" 
              color="blue"
              onClick={() => handleAssignEPG(tvg)}
              disabled={!selectedChannel || isUpdating}
              leftSection={<Link size={14} />}
            >
              Assign
            </Button>
          </Group>
        </Box>
      </div>
    );
  };

  return (
    <Box h="100vh" w="100%" p={10} display="flex" style={{ flexDirection: 'column', gap: '10px' }}>
      <Group justify="space-between" align="center" px={5}>
        <Group>
          <Tv size={24} />
          <Text size="xl" fw={600}>Advanced EPG Mapping</Text>
        </Group>
        <Group align="center" gap="lg">
          <Box w={200}>
            <Text size="xs" fw={500} mb={2}>Smart Match Threshold: {matchThreshold}%</Text>
            <Slider
              value={matchThreshold}
              onChange={setMatchThreshold}
              min={50}
              max={100}
              step={1}
              size="sm"
              color="blue"
              marks={[{ value: 50, label: 'Loose' }, { value: 85, label: 'Strict' }, { value: 100, label: 'Exact' }]}
            />
          </Box>
          <Button
            size="sm"
            variant="light"
            color="blue"
            leftSection={<Zap size={16} />}
            onClick={handleSmartMatch}
            loading={isUpdating}
          >
            {selectedChannelIds.size > 0 ? `Smart Match Selected (${selectedChannelIds.size})` : 'Smart Match Visible'}
          </Button>
          <Badge size="lg" color="blue" variant="dot">
            {channelList.length} Channels visible
          </Badge>
        </Group>
      </Group>

      <Box style={{ flex: 1, minHeight: 0 }}>
        <Allotment defaultSizes={[40, 60]}>
          {/* LEFT PANE - CHANNELS */}
          <Box h="100%" p="sm" style={{ display: 'flex', flexDirection: 'column' }}>
            <Paper p="sm" mb="md" withBorder>
              <Stack gap="xs">
                <Text size="sm" fw={500}>Channels Filter</Text>
                <TextInput
                  placeholder="Search Channels..."
                  value={channelSearch}
                  onChange={(e) => setChannelSearch(e.currentTarget.value)}
                  leftSection={<Search size={14} />}
                  size="xs"
                />
                <Group grow>
                  <Select
                    size="xs"
                    data={groupOptions}
                    value={filterGroup}
                    onChange={setFilterGroup}
                  />
                  <Switch
                    label="Unmapped Only"
                    size="xs"
                    checked={filterUnmappedOnly}
                    onChange={(e) => setFilterUnmappedOnly(e.currentTarget.checked)}
                  />
                </Group>
                <Group justify="space-between" align="center" mt="xs">
                  <Checkbox
                    size="xs"
                    label={`Select All Visible (${channelList.length})`}
                    checked={channelList.length > 0 && selectedChannelIds.size === channelList.length}
                    onChange={handleSelectAllVisible}
                  />
                  {selectedChannelIds.size > 0 && (
                    <Text size="xs" c="dimmed">{selectedChannelIds.size} selected</Text>
                  )}
                </Group>
              </Stack>
            </Paper>

            <Box style={{ flex: 1 }}>
              {channelList.length > 0 ? (
                <List
                  height={window.innerHeight - 250} // Rough height estimate, will handle via ResizeObserver in prod ideally
                  itemCount={channelList.length}
                  itemSize={65}
                  width="100%"
                >
                  {ChannelRow}
                </List>
              ) : (
                <Text c="dimmed" ta="center" mt="xl">No channels found</Text>
              )}
            </Box>
          </Box>

          {/* RIGHT PANE - EPG DATA */}
          <Box h="100%" p="sm" style={{ display: 'flex', flexDirection: 'column' }}>
            <Paper p="sm" mb="md" withBorder>
              <Stack gap="xs">
                <Group justify="space-between">
                  <Text size="sm" fw={500}>EPG Database</Text>
                  {selectedChannel && (
                    <Badge color="blue" variant="filled">
                      Mapping: {selectedChannel.name}
                    </Badge>
                  )}
                </Group>
                
                <TextInput
                  placeholder="Search EPG..."
                  value={epgSearch}
                  onChange={(e) => setEpgSearch(e.currentTarget.value)}
                  leftSection={<Search size={14} />}
                  size="xs"
                />
                <Select
                  size="xs"
                  data={sourceOptions}
                  value={epgSourceFilter}
                  onChange={setEpgSourceFilter}
                  placeholder="Filter by Source"
                />
              </Stack>
            </Paper>

            <Box style={{ flex: 1 }}>
              {!selectedChannel ? (
                <Stack align="center" justify="center" h="100%" c="dimmed">
                  <AlertCircle size={48} opacity={0.5} />
                  <Text>Select a channel on the left to start mapping</Text>
                </Stack>
              ) : epgList.length > 0 ? (
                <List
                  height={window.innerHeight - 250}
                  itemCount={epgList.length}
                  itemSize={65}
                  width="100%"
                >
                  {EPGRow}
                </List>
              ) : (
                <Text c="dimmed" ta="center" mt="xl">No EPG records match your search</Text>
              )}
            </Box>
          </Box>
        </Allotment>
      </Box>
    </Box>
  );
};

const EPGMapping = () => {
  return (
    <ErrorBoundary>
      <EPGMappingContent />
    </ErrorBoundary>
  );
};

export default EPGMapping;
