import React, { useEffect, useCallback, useState } from 'react';
import { Box, Tabs, Flex, Text, TabsList, TabsTab, Button, Group } from '@mantine/core';
import { Github } from 'lucide-react';
import api from '../api';
import useLogosStore from '../store/logos';
import useVODLogosStore from '../store/vodLogos';
import LogosTable from '../components/tables/LogosTable';
import VODLogosTable from '../components/tables/VODLogosTable';
import { showNotification } from '../utils/notificationUtils.js';

const LogosPage = () => {
  const logos = useLogosStore((s) => s.logos);
  const totalCount = useVODLogosStore((s) => s.totalCount);
  const [activeTab, setActiveTab] = useState('channel');
  const [isSyncing, setIsSyncing] = useState(false);
  const logoCount =
    activeTab === 'channel' ? Object.keys(logos).length : totalCount;

  const loadChannelLogos = useCallback(async () => {
    try {
      // Only fetch all logos if we haven't loaded them yet
      if (useLogosStore.getState().needsAllLogos()) {
        await useLogosStore.getState().fetchAllLogos();
      }
    } catch (err) {
      showNotification({
        title: 'Error',
        message: 'Failed to load channel logos',
        color: 'red',
      });
      console.error('Failed to load channel logos:', err);
    }
  }, []);

  useEffect(() => {
    // Always load channel logos on mount
    loadChannelLogos();
  }, [loadChannelLogos]);

  const handleSyncGitHub = async () => {
    setIsSyncing(true);
    try {
      const response = await api.post('/api/logos/sync_github/');
      const data = response.data;
      showNotification({
        title: 'Sync Complete',
        message: data.message,
        color: 'green',
      });
      // Force reload of logos
      await useLogosStore.getState().fetchAllLogos();
    } catch (err) {
      showNotification({
        title: 'Sync Failed',
        message: err.response?.data?.error || 'Failed to sync GitHub logos',
        color: 'red',
      });
      console.error('GitHub sync error:', err);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <Box>
      {/* Header with title and tabs */}
      <Box style={{ justifyContent: 'center' }} display={'flex'} p={'10px 0'}>
        <Flex
          style={{
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
          w={'100%'}
          maw={'1200px'}
          pb={10}
        >
          <Flex gap={8} align="center">
            <Text
              ff={'Inter, sans-serif'}
              fz={'20px'}
              fw={500}
              lh={1}
              c="white"
              mb={0}
              lts={'-0.3px'}
            >
              Logos
            </Text>
            <Text size="sm" c="dimmed">
              ({logoCount} {logoCount !== 1 ? 'logos' : 'logo'})
            </Text>
          </Flex>

          <Group>
            {activeTab === 'channel' && (
              <Button
                size="xs"
                variant="light"
                color="blue"
                leftSection={<Github size={16} />}
                onClick={handleSyncGitHub}
                loading={isSyncing}
              >
                Sync GitHub TV-Logos
              </Button>
            )}

            <Tabs value={activeTab} onChange={setActiveTab} variant="pills">
              <TabsList>
                <TabsTab value="channel">Channel Logos</TabsTab>
                <TabsTab value="vod">VOD Logos</TabsTab>
              </TabsList>
            </Tabs>
          </Group>
        </Flex>
      </Box>

      {/* Content based on active tab */}
      {activeTab === 'channel' && <LogosTable />}
      {activeTab === 'vod' && <VODLogosTable />}
    </Box>
  );
};

export default LogosPage;
