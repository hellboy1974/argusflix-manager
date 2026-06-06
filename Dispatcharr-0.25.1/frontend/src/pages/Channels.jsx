import React, { useCallback, useRef, useState, useEffect } from 'react';
import ChannelsTable from '../components/tables/ChannelsTable';
import StreamsTable from '../components/tables/StreamsTable';
import CategorySidebar from '../components/CategorySidebar';
import { Box } from '@mantine/core';
import { Allotment } from 'allotment';
import { USER_LEVELS } from '../constants';
import useAuthStore from '../store/auth';
import useLogosStore from '../store/logos';
import useChannelsStore from '../store/channels';
import useLocalStorage from '../hooks/useLocalStorage';
import ErrorBoundary from '../components/ErrorBoundary';
import API from '../api';

const PageContent = () => {
  const authUser = useAuthStore((s) => s.user);
  const fetchChannelAssignableLogos = useLogosStore(
    (s) => s.fetchChannelAssignableLogos
  );
  const enableLogoRendering = useLogosStore((s) => s.enableLogoRendering);

  const channelGroups = useChannelsStore((s) => s.channelGroups);
  const fetchChannelGroups = useChannelsStore((s) => s.fetchChannelGroups);

  const [selectedGroupId, setSelectedGroupId] = useState(null);
  const [playlists, setPlaylists] = useState([]);

  const fetchPlaylists = useCallback(async () => {
    try {
      const data = await API.getCustomPlaylists();
      setPlaylists(data || []);
    } catch (e) {
      console.error(e);
    }
  }, []);

  const handleBulkAction = useCallback(() => {
    fetchChannelGroups();
    fetchPlaylists();
  }, [fetchChannelGroups, fetchPlaylists]);

  const channelsReady = useRef(false);
  const streamsReady = useRef(false);
  const logosTriggered = useRef(false);

  const [allotmentSizes, setAllotmentSizes] = useLocalStorage(
    'channels-splitter-sizes',
    [60, 40]
  );

  useEffect(() => {
    fetchChannelGroups();
    fetchPlaylists();
  }, [fetchChannelGroups, fetchPlaylists]);

  // Only load logos when BOTH tables are ready
  const tryLoadLogos = useCallback(() => {
    if (
      channelsReady.current &&
      streamsReady.current &&
      !logosTriggered.current
    ) {
      logosTriggered.current = true;
      // Use requestAnimationFrame to defer logo loading until after browser paint
      // This ensures EPG column is fully rendered before logos start loading
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          enableLogoRendering();
          fetchChannelAssignableLogos();
        });
      });
    }
  }, [fetchChannelAssignableLogos, enableLogoRendering]);

  const handleChannelsReady = useCallback(() => {
    channelsReady.current = true;
    tryLoadLogos();
  }, [tryLoadLogos]);

  const handleStreamsReady = useCallback(() => {
    streamsReady.current = true;
    tryLoadLogos();
  }, [tryLoadLogos]);

  const handleSplitChange = (sizes) => {
    setAllotmentSizes(sizes);
  };

  const handleResize = (sizes) => {
    setAllotmentSizes(sizes);
  };

  if (!authUser.id) return <></>;

  // Resolve group name for filtering
  const selectedGroup = selectedGroupId ? channelGroups[selectedGroupId]?.name : '';

  // Format channel groups list for Sidebar
  const categoriesList = Object.values(channelGroups).map((g) => ({
    id: g.id,
    name: g.name,
    channel_count: g.channel_count,
  })).sort((a, b) => a.name.localeCompare(b.name));

  if (authUser.user_level <= USER_LEVELS.STANDARD) {
    handleStreamsReady();
    return (
      <Box h={'100vh'} w={'100%'} display={'flex'} p={10} style={{ overflow: 'hidden', gap: '10px' }}>
        <CategorySidebar
          categories={categoriesList}
          selectedId={selectedGroupId}
          onSelect={(id) => setSelectedGroupId(selectedGroupId === id ? null : id)}
          onBulkAction={handleBulkAction}
          type="live-tv"
          playlists={playlists}
        />
        <Box style={{ flex: 1, height: '100%', minWidth: 0, overflowY: 'auto' }}>
          <ChannelsTable onReady={handleChannelsReady} selectedGroup={selectedGroup} />
        </Box>
      </Box>
    );
  }

  return (
    <Box h={'100vh'} w={'100%'} display={'flex'} p={10} style={{ overflow: 'hidden', gap: '10px' }}>
      <CategorySidebar
        categories={categoriesList}
        selectedId={selectedGroupId}
        onSelect={(id) => setSelectedGroupId(selectedGroupId === id ? null : id)}
        onBulkAction={handleBulkAction}
        type="live-tv"
        playlists={playlists}
      />
      <Box style={{ flex: 1, height: '100%', minWidth: 0 }}>
        <Allotment
          defaultSizes={allotmentSizes}
          h={'100%'}
          w={'100%'}
          miw={'625px'}
          className="custom-allotment"
          minSize={100}
          onChange={handleSplitChange}
          onResize={handleResize}
        >
          <Box p={10} miw={'100px'} style={{ overflowX: 'auto' }}>
            <Box miw={'625px'}>
              <ChannelsTable onReady={handleChannelsReady} selectedGroup={selectedGroup} />
            </Box>
          </Box>
          <Box p={10} miw={'100px'} style={{ overflowX: 'auto' }}>
            <Box miw={'625px'}>
              <StreamsTable onReady={handleStreamsReady} />
            </Box>
          </Box>
        </Allotment>
      </Box>
    </Box>
  );
};

const ChannelsPage = () => {
  return (
    <ErrorBoundary>
      <PageContent />
    </ErrorBoundary>
  );
};

export default ChannelsPage;
