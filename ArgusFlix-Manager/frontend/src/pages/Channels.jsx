import React, { useCallback, useRef } from 'react';
import ChannelsTable from '../components/tables/ChannelsTable';
import StreamsTable from '../components/tables/StreamsTable';
import { Box, Tabs } from '@mantine/core';
import { Allotment } from 'allotment';
import { USER_LEVELS } from '../constants';
import useAuthStore from '../store/auth';
import useLogosStore from '../store/logos';
import useLocalStorage from '../hooks/useLocalStorage';
import ErrorBoundary from '../components/ErrorBoundary';
import { List, Edit3 } from 'lucide-react';
import M3UEditor from '../components/M3UEditor';

const PageContent = () => {
  const authUser = useAuthStore((s) => s.user);
  const fetchChannelAssignableLogos = useLogosStore(
    (s) => s.fetchChannelAssignableLogos
  );
  const enableLogoRendering = useLogosStore((s) => s.enableLogoRendering);

  const channelsReady = useRef(false);
  const streamsReady = useRef(false);
  const logosTriggered = useRef(false);

  const [allotmentSizes, setAllotmentSizes] = useLocalStorage(
    'channels-splitter-sizes',
    [60, 40]
  );
  
  const [activeTab, setActiveTab] = useLocalStorage('channels-active-tab', 'live-view');

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

  if (authUser.user_level <= USER_LEVELS.STANDARD) {
    handleStreamsReady();
    return (
      <Box style={{ padding: 10 }}>
        <ChannelsTable onReady={handleChannelsReady} />
      </Box>
    );
  }

  return (
    <Box h={'100vh'} w={'100%'} display={'flex'} style={{ flexDirection: 'column' }}>
      <Tabs value={activeTab} onChange={setActiveTab} style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Box p="xs">
          <Tabs.List>
            <Tabs.Tab value="live-view" leftSection={<List size={16} />}>
              Listen-Ansicht
            </Tabs.Tab>
            <Tabs.Tab value="editor" leftSection={<Edit3 size={16} />}>
              M3U Editor
            </Tabs.Tab>
          </Tabs.List>
        </Box>

        <Tabs.Panel value="live-view" style={{ flex: 1, overflow: 'hidden' }}>
          <Box h={'100%'} w={'100%'} display={'flex'} style={{ overflowX: 'auto' }}>
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
              <Box p={10} miw={'100px'} style={{ overflowX: 'auto', height: '100%' }}>
                <Box miw={'625px'} h={'100%'}>
                  <ChannelsTable onReady={handleChannelsReady} />
                </Box>
              </Box>
              <Box p={10} miw={'100px'} style={{ overflowX: 'auto', height: '100%' }}>
                <Box miw={'625px'} h={'100%'}>
                  <StreamsTable onReady={handleStreamsReady} />
                </Box>
              </Box>
            </Allotment>
          </Box>
        </Tabs.Panel>

        <Tabs.Panel value="editor" style={{ flex: 1, overflow: 'hidden' }}>
          <M3UEditor />
        </Tabs.Panel>
      </Tabs>
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
