import React, { Suspense, useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Box,
  Center,
  Tabs,
  Title,
  Text,
  Loader,
  Paper
} from '@mantine/core';
import {
  MonitorCog,
  Smartphone,
  Network,
  Users
} from 'lucide-react';

const UserAgentsTable = React.lazy(() => import('../components/tables/UserAgentsTable.jsx'));
const StreamProfilesTable = React.lazy(() => import('../components/tables/StreamProfilesTable.jsx'));
const OutputProfilesTable = React.lazy(() => import('../components/tables/OutputProfilesTable.jsx'));
const BackupManager = React.lazy(() => import('../components/backups/BackupManager.jsx'));
const UiSettingsForm = React.lazy(() => import('../components/forms/settings/UiSettingsForm.jsx'));
const UserLimitsForm = React.lazy(() => import('../components/forms/settings/UserLimitsForm.jsx'));
const NetworkAccessForm = React.lazy(() => import('../components/forms/settings/NetworkAccessForm.jsx'));
const ProxySettingsForm = React.lazy(() => import('../components/forms/settings/ProxySettingsForm.jsx'));
const StreamSettingsForm = React.lazy(() => import('../components/forms/settings/StreamSettingsForm.jsx'));
const DvrSettingsForm = React.lazy(() => import('../components/forms/settings/DvrSettingsForm.jsx'));
const SystemSettingsForm = React.lazy(() => import('../components/forms/settings/SystemSettingsForm.jsx'));
const NavOrderForm = React.lazy(() => import('../components/forms/settings/NavOrderForm.jsx'));
const AppConfigForm = React.lazy(() => import('../components/forms/settings/AppConfigForm.jsx'));

import useAuthStore from '../store/auth';
import { USER_LEVELS } from '../constants';
import ErrorBoundary from '../components/ErrorBoundary.jsx';

const SettingsContent = () => {
  const [activeTab, setActiveTab] = useState('system');
  const location = useLocation();
  const userLevel = useAuthStore((state) => state.user?.level);

  useEffect(() => {
    const hash = location.hash.replace('#', '');
    if (hash) {
      setActiveTab(hash);
    }
  }, [location.hash]);

  if (userLevel !== USER_LEVELS.ADMIN) {
    return (
      <Center h="100%">
        <Text>You do not have permission to view this page.</Text>
      </Center>
    );
  }

  return (
    <Center p={10}>
      <Box w={'100%'} maw={1000}>
        <Title order={2} mb="md">Manager Einstellungen</Title>
        <Paper p="md" withBorder>
          <Tabs value={activeTab} onChange={setActiveTab} orientation="vertical" variant="pills">
            
            <Tabs.List miw={200} mr="xl">
              <Tabs.Tab value="system" leftSection={<MonitorCog size={16} />}>
                System & Verwaltung
              </Tabs.Tab>
              <Tabs.Tab value="app_config" leftSection={<Smartphone size={16} />}>
                Android App Config
              </Tabs.Tab>
              <Tabs.Tab value="network" leftSection={<Network size={16} />}>
                Netzwerk & Streaming
              </Tabs.Tab>
              <Tabs.Tab value="profiles" leftSection={<Users size={16} />}>
                Profile & Agents
              </Tabs.Tab>
            </Tabs.List>

            <Suspense fallback={<Center p="xl"><Loader /></Center>}>
              
              <Tabs.Panel value="system">
                <Box mb="xl">
                  <SystemSettingsForm />
                </Box>
                <Box mb="xl">
                  <UiSettingsForm />
                </Box>
                <Box mb="xl">
                  <NavOrderForm />
                </Box>
                <Box mb="xl">
                  <BackupManager />
                </Box>
              </Tabs.Panel>

              <Tabs.Panel value="app_config">
                <AppConfigForm />
              </Tabs.Panel>

              <Tabs.Panel value="network">
                <Box mb="xl">
                  <NetworkAccessForm />
                </Box>
                <Box mb="xl">
                  <ProxySettingsForm />
                </Box>
                <Box mb="xl">
                  <StreamSettingsForm />
                </Box>
                <Box mb="xl">
                  <DvrSettingsForm />
                </Box>
              </Tabs.Panel>

              <Tabs.Panel value="profiles">
                <Box mb="xl">
                  <UserLimitsForm />
                </Box>
                <Box mb="xl">
                  <UserAgentsTable />
                </Box>
                <Box mb="xl">
                  <StreamProfilesTable />
                </Box>
                <Box mb="xl">
                  <OutputProfilesTable />
                </Box>
              </Tabs.Panel>

            </Suspense>
          </Tabs>
        </Paper>
      </Box>
    </Center>
  );
};

const Settings = () => {
  return (
    <ErrorBoundary>
      <SettingsContent />
    </ErrorBoundary>
  );
};

export default Settings;
