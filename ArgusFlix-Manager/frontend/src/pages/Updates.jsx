import React, { useState, useEffect } from 'react';
import { Box, Title, Text, Stack, Paper, Group, Badge, Button, Divider, Loader } from '@mantine/core';
import { RefreshCw, Check, X } from 'lucide-react';
import api from '../api';
import ErrorBoundary from '../components/ErrorBoundary';

const UpdatesContent = () => {
  const [loading, setLoading] = useState(true);
  const [providers, setProviders] = useState([]);

  useEffect(() => {
    fetchUpdates();
  }, []);

  const fetchUpdates = async () => {
    try {
      setLoading(true);
      // Fetch all accounts
      const res = await api.get('/api/v1/m3u-accounts/');
      const accounts = res.data?.results || res.data || [];
      
      const fiveDaysAgo = new Date();
      fiveDaysAgo.setDate(fiveDaysAgo.getDate() - 5);

      const providersWithUpdates = accounts.map(account => {
        const newLive = []; // Parse from account.channel_groups if they existed
        const newVod = [];
        const newSeries = [];

        // Here we'd iterate over the relationships included in the serializer
        if (account.channel_groups) {
          account.channel_groups.forEach(cg => {
            if (!cg.is_acknowledged && new Date(cg.first_seen_at) > fiveDaysAgo) {
              newLive.push({ id: cg.channel_group, name: 'Kategorie ' + cg.channel_group, type: 'live' });
            }
          });
        }
        // Assuming VOD & Series are somehow fetched or included

        return {
          id: account.id,
          name: account.name,
          newLive,
          newVod,
          newSeries
        };
      }).filter(p => p.newLive.length > 0 || p.newVod.length > 0 || p.newSeries.length > 0);

      setProviders(providersWithUpdates);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (providerId, category, action) => {
    // action: 'activate' | 'dismiss'
    // category: { id, type }
    try {
      // We added 'acknowledge-categories' endpoint
      await api.post(\/api/v1/m3u-accounts/\/acknowledge-categories/\, {
        categories: [{ id: category.id, type: category.type }],
        acknowledge_all: false
      });
      // Refresh
      fetchUpdates();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAcknowledgeAll = async (providerId) => {
    try {
      await api.post(\/api/v1/m3u-accounts/\/acknowledge-categories/\, {
        acknowledge_all: true
      });
      fetchUpdates();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <Box p="md"><Loader /></Box>;
  }

  return (
    <Box p="md" h="100%">
      <Group position="apart" mb="xl">
        <Title order={2}>Updates & Neue Kategorien</Title>
        <Button leftSection={<RefreshCw size={16} />} variant="light" onClick={fetchUpdates}>
          Aktualisieren
        </Button>
      </Group>

      {providers.length === 0 ? (
        <Paper p="xl" withBorder style={{ textAlign: 'center' }}>
          <Text c="dimmed" size="lg">Keine neuen Updates vorhanden.</Text>
          <Text c="dimmed" size="sm">Alle neuen Kategorien wurden bearbeitet oder es gibt keine neuen Änderungen.</Text>
        </Paper>
      ) : (
        <Stack spacing="xl">
          {providers.map(provider => (
            <Paper key={provider.id} p="md" withBorder>
              <Group position="apart" mb="md">
                <Box>
                  <Title order={4}>{provider.name}</Title>
                  <Text size="sm" c="dimmed">Neue Kategorien wurden von diesem Provider gefunden.</Text>
                </Box>
                <Button 
                  variant="light" 
                  color="blue"
                  onClick={() => handleAcknowledgeAll(provider.id)}
                >
                  Alle Aktivieren
                </Button>
              </Group>
              <Divider mb="md" />

              {/* Live TV Updates */}
              {provider.newLive.length > 0 && (
                <Box mb="md">
                  <Text weight={500} mb="xs">Live-TV</Text>
                  <Stack spacing="xs">
                    {provider.newLive.map(cat => (
                      <Group key={cat.id} position="apart" bg="dark.6" p="xs" style={{ borderRadius: 4 }}>
                        <Text size="sm">{cat.name}</Text>
                        <Group>
                          <Button size="xs" variant="light" color="green" onClick={() => handleAcknowledge(provider.id, cat, 'activate')}>
                            Aktivieren
                          </Button>
                          <Button size="xs" variant="subtle" color="gray" onClick={() => handleAcknowledge(provider.id, cat, 'dismiss')}>
                            Verwerfen
                          </Button>
                        </Group>
                      </Group>
                    ))}
                  </Stack>
                </Box>
              )}

              {/* VOD & Series would be similarly rendered here */}
            </Paper>
          ))}
        </Stack>
      )}
    </Box>
  );
};

const UpdatesPage = () => {
  return (
    <ErrorBoundary>
      <UpdatesContent />
    </ErrorBoundary>
  );
};

export default UpdatesPage;
