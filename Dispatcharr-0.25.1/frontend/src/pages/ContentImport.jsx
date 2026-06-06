import React from 'react';
import { Box, Stack, Tabs, Text, Title, Group } from '@mantine/core';
import { ListVideo, Radio, FileText, Download, Play } from 'lucide-react';
import M3UsTable from '../components/tables/M3UsTable';
import EPGsTable from '../components/tables/EPGsTable';
import StalkerPortalsTable from '../components/tables/StalkerPortalsTable';
import ErrorBoundary from '../components/ErrorBoundary';

const PageContent = () => {
  return (
    <Stack
      p="md"
      h="100%"
      miw="1100px"
      style={{
        overflowX: 'auto',
        overflowY: 'auto',
      }}
      gap="md"
    >
      <Group justify="space-between" align="center" mb="xs">
        <Stack gap={2}>
          <Group gap="xs">
            <Download size={24} color="var(--mantine-color-blue-filled)" />
            <Title order={2} style={{ fontFamily: 'Outfit, Inter, sans-serif', fontWeight: 600 }}>
              Content Import
            </Title>
          </Group>
          <Text size="xs" c="dimmed">
            Manage your external playlists (M3U), Xtream Codes panels, Stalker/MAG portals, and XMLTV EPG guides.
          </Text>
        </Stack>
      </Group>

      <Tabs defaultValue="xtream" variant="outline" styles={{
        root: {
          display: 'flex',
          flexDirection: 'column',
          flex: 1,
        },
        panel: {
          paddingTop: 'var(--mantine-spacing-md)',
          flex: 1,
        }
      }}>
        <Tabs.List>
          <Tabs.Tab value="xtream" leftSection={<Play size={16} />}>
            Xtream Codes
          </Tabs.Tab>
          <Tabs.Tab value="m3u" leftSection={<ListVideo size={16} />}>
            M3U Playlists
          </Tabs.Tab>
          <Tabs.Tab value="stalker" leftSection={<Radio size={16} />}>
            Stalker Portals
          </Tabs.Tab>
          <Tabs.Tab value="epg" leftSection={<FileText size={16} />}>
            EPG-Guides
          </Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="xtream">
          <Box style={{ overflow: 'hidden' }}>
            <M3UsTable filterType="XC" />
          </Box>
        </Tabs.Panel>

        <Tabs.Panel value="m3u">
          <Box style={{ overflow: 'hidden' }}>
            <M3UsTable filterType="STD" />
          </Box>
        </Tabs.Panel>

        <Tabs.Panel value="stalker">
          <Box style={{ overflow: 'hidden' }}>
            <StalkerPortalsTable />
          </Box>
        </Tabs.Panel>

        <Tabs.Panel value="epg">
          <Box style={{ overflow: 'hidden' }}>
            <EPGsTable />
          </Box>
        </Tabs.Panel>
      </Tabs>
    </Stack>
  );
};

const ContentImportPage = () => {
  return (
    <ErrorBoundary>
      <PageContent />
    </ErrorBoundary>
  );
};

export default ContentImportPage;
