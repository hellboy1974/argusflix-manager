import useUserAgentsStore from '../store/userAgents';
import M3UsTable from '../components/tables/M3UsTable';
import EPGsTable from '../components/tables/EPGsTable';
import EPGStatusTab from '../components/EPGStatusTab';
import { Box, Stack, Tabs } from '@mantine/core';
import { Database, Activity } from 'lucide-react';
import ErrorBoundary from '../components/ErrorBoundary';

const PageContent = () => {
  const error = useUserAgentsStore((state) => state.error);
  if (error) throw new Error(error);

  return (
    <Box p="md" h="100%">
      <Tabs defaultValue="sources" h="100%" display="flex" style={{ flexDirection: 'column' }}>
        <Tabs.List>
          <Tabs.Tab value="sources" leftSection={<Database size={16} />}>
            Content Sources
          </Tabs.Tab>
          <Tabs.Tab value="epg_status" leftSection={<Activity size={16} />}>
            EPG Status
          </Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="sources" pt="md" style={{ flex: 1, minHeight: 0 }}>
          <Stack
            h="100%"
            miw="1100px"
            style={{
              overflowX: 'auto',
              overflowY: 'auto',
            }}
            spacing="xs"
          >
            <Box sx={{ flex: '1 1 50%', overflow: 'hidden' }}>
              <M3UsTable />
            </Box>

            <Box sx={{ flex: '1 1 50%', overflow: 'hidden' }}>
              <EPGsTable />
            </Box>
          </Stack>
        </Tabs.Panel>

        <Tabs.Panel value="epg_status" pt="md" style={{ flex: 1, minHeight: 0 }}>
          <EPGStatusTab />
        </Tabs.Panel>
      </Tabs>
    </Box>
  );
};

const M3UPage = () => {
  return (
    <ErrorBoundary>
      <PageContent />
    </ErrorBoundary>
  );
};

export default M3UPage;
