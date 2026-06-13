import React, { useEffect } from 'react';
import {
  Box,
  Paper,
  Table,
  Badge,
  Text,
  Group,
  Stack,
  ActionIcon,
  ScrollArea,
} from '@mantine/core';
import { RefreshCw, AlertCircle, CheckCircle2, Clock } from 'lucide-react';
import useEPGsStore from '../store/epgs';
import api from '../api';
import { notifications } from '@mantine/notifications';

const getStatusColor = (status) => {
  switch (status) {
    case 'success':
      return 'green';
    case 'error':
      return 'red';
    case 'fetching':
    case 'parsing':
      return 'blue';
    case 'disabled':
      return 'gray';
    case 'idle':
    default:
      return 'orange';
  }
};

const getStatusIcon = (status) => {
  switch (status) {
    case 'success':
      return <CheckCircle2 size={16} />;
    case 'error':
      return <AlertCircle size={16} />;
    case 'fetching':
    case 'parsing':
      return <RefreshCw size={16} className="spin" />;
    default:
      return <Clock size={16} />;
  }
};

const EPGStatusTab = () => {
  const epgs = useEPGsStore((s) => s.epgs);
  const fetchEPGs = useEPGsStore((s) => s.fetchEPGs);

  useEffect(() => {
    fetchEPGs();
  }, [fetchEPGs]);

  const sources = Object.values(epgs).sort((a, b) => a.name.localeCompare(b.name));

  const handleRefresh = async (id) => {
    try {
      await api.refreshEPG(id);
      notifications.show({ title: 'Success', message: 'EPG refresh started', color: 'green' });
      fetchEPGs();
    } catch (e) {
      notifications.show({ title: 'Error', message: 'Failed to start EPG refresh', color: 'red' });
    }
  };

  return (
    <Box p="md" h="100%">
      <Paper withBorder p="0" radius="md" style={{ overflow: 'hidden' }}>
        <ScrollArea h="calc(100vh - 120px)">
          <Table stickyHeader highlightOnHover verticalSpacing="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Source Name</Table.Th>
                <Table.Th>Type</Table.Th>
                <Table.Th>Status</Table.Th>
                <Table.Th>Last Updated</Table.Th>
                <Table.Th>Message / Error</Table.Th>
                <Table.Th w={80}>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {sources.length === 0 ? (
                <Table.Tr>
                  <Table.Td colSpan={6}>
                    <Text c="dimmed" ta="center" py="xl">
                      No EPG sources found
                    </Text>
                  </Table.Td>
                </Table.Tr>
              ) : (
                sources.map((source) => (
                  <Table.Tr key={source.id}>
                    <Table.Td>
                      <Text fw={500} size="sm">{source.name}</Text>
                    </Table.Td>
                    <Table.Td>
                      <Badge variant="light" color="gray">
                        {source.source_type}
                      </Badge>
                    </Table.Td>
                    <Table.Td>
                      <Badge
                        color={getStatusColor(source.status)}
                        variant="light"
                        leftSection={getStatusIcon(source.status)}
                      >
                        {source.status}
                      </Badge>
                    </Table.Td>
                    <Table.Td>
                      <Text size="sm">
                        {source.updated_at
                          ? new Date(source.updated_at).toLocaleString()
                          : 'Never'}
                      </Text>
                    </Table.Td>
                    <Table.Td>
                      <Text size="sm" c={source.status === 'error' ? 'red' : 'dimmed'} lineClamp={2} title={source.last_message || ''}>
                        {source.last_message || '—'}
                      </Text>
                    </Table.Td>
                    <Table.Td>
                      <ActionIcon
                        variant="subtle"
                        color="blue"
                        onClick={() => handleRefresh(source.id)}
                        disabled={source.status === 'fetching' || source.status === 'parsing'}
                        title="Force Refresh"
                      >
                        <RefreshCw size={16} />
                      </ActionIcon>
                    </Table.Td>
                  </Table.Tr>
                ))
              )}
            </Table.Tbody>
          </Table>
        </ScrollArea>
      </Paper>
    </Box>
  );
};

export default EPGStatusTab;
