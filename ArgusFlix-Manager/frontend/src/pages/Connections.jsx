import React, { useState, useEffect } from 'react';
import { Box, Stack, Accordion, Button, Group, Title, Text, Paper, Loader, Badge } from '@mantine/core';
import { Database, Plus, Server, Link as LinkIcon } from 'lucide-react';
import ErrorBoundary from '../components/ErrorBoundary';
import EPGsTable from '../components/tables/EPGsTable';
import usePlaylistsStore from '../store/playlists';
import useMediaServersStore from '../store/mediaservers';
import StalkerProviderWizard from '../components/forms/StalkerProviderWizard';
import XtreamProviderWizard from '../components/forms/XtreamProviderWizard';
import M3uProviderWizard from '../components/forms/M3uProviderWizard';
import PlexProviderWizard from '../components/forms/PlexProviderWizard';
import EmbyProviderWizard from '../components/forms/EmbyProviderWizard';
import JellyfinProviderWizard from '../components/forms/JellyfinProviderWizard';
import ArgusFlixProviderWizard from '../components/forms/ArgusFlixProviderWizard';

const ConnectionsContent = () => {
  const { playlists, fetchPlaylists, isLoading: isPlaylistsLoading } = usePlaylistsStore();
  const { servers, fetchServers, isLoading: isServersLoading } = useMediaServersStore();
  
  const [stalkerWizardOpen, setStalkerWizardOpen] = useState(false);
  const [selectedStalkerPortal, setSelectedStalkerPortal] = useState(null);

  const [xtreamWizardOpen, setXtreamWizardOpen] = useState(false);
  const [selectedXtreamPanel, setSelectedXtreamPanel] = useState(null);

  const [m3uWizardOpen, setM3uWizardOpen] = useState(false);
  const [selectedM3uLink, setSelectedM3uLink] = useState(null);

  const [plexWizardOpen, setPlexWizardOpen] = useState(false);
  const [selectedPlexServer, setSelectedPlexServer] = useState(null);

  const [embyWizardOpen, setEmbyWizardOpen] = useState(false);
  const [selectedEmbyServer, setSelectedEmbyServer] = useState(null);

  const [jellyfinWizardOpen, setJellyfinWizardOpen] = useState(false);
  const [selectedJellyfinServer, setSelectedJellyfinServer] = useState(null);

  const [argusFlixWizardOpen, setArgusFlixWizardOpen] = useState(false);
  const [selectedArgusFlixPortal, setSelectedArgusFlixPortal] = useState(null);

  useEffect(() => {
    fetchPlaylists();
    fetchServers();
  }, [fetchPlaylists, fetchServers]);

  const argusFlixConnections = playlists.filter(
    (p) => p.custom_properties?.is_argusflix_manager
  );

  const stalkerPortals = playlists.filter(
    (p) => (p.name.startsWith('Stalker:') || p.custom_properties?.portal_key) && !p.custom_properties?.is_argusflix_manager
  );

  const xtreamPanels = playlists.filter(
    (p) => (p.account_type === 'XC' || (p.username && p.password && !p.name.startsWith('Stalker:'))) && !p.custom_properties?.is_argusflix_manager
  );

  const m3uLinks = playlists.filter(
    (p) => (p.account_type === 'STD' || !p.account_type) && 
           !p.username && 
           !p.name.startsWith('Stalker:') && 
           !p.custom_properties?.portal_key &&
           !p.custom_properties?.is_argusflix_manager
  );

  const plexServers = servers.filter((s) => s.server_type === 'plex');
  const embyServers = servers.filter((s) => s.server_type === 'emby');
  const jellyfinServers = servers.filter((s) => s.server_type === 'jellyfin');

  const isLoading = isPlaylistsLoading || isServersLoading;

  return (
    <Box p="md" h="100%">
      <Title order={2} mb="md">Verbindungen (Connections)</Title>
      
      {isLoading ? (
        <Loader />
      ) : (
        <Accordion variant="separated" defaultValue="argusflix">
          
          <Accordion.Item value="argusflix">
            <Accordion.Control icon={<LinkIcon size={20} color="var(--mantine-color-blue-6)" />}>
              <Text weight={600} color="blue">ArgusFlix Manager (Eigene Playlisten)</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  color="blue"
                  onClick={() => {
                    setSelectedArgusFlixPortal(null);
                    setArgusFlixWizardOpen(true);
                  }}
                >
                  ArgusFlix Verbindung Hinzufügen
                </Button>
                
                {argusFlixConnections.map((portal) => (
                  <Paper key={portal.id} p="md" withBorder opacity={portal.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{portal.name}</Text>
                          {portal.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{portal.server_url}</Text>
                      </Box>
                      <Button variant="subtle" color="blue" onClick={() => {
                        setSelectedArgusFlixPortal(portal);
                        setArgusFlixWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="stalker">
            <Accordion.Control icon={<Database size={20} />}>
              <Text weight={500}>Stalker Portale</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  onClick={() => {
                    setSelectedStalkerPortal(null);
                    setStalkerWizardOpen(true);
                  }}
                >
                  Stalker Portal Hinzufügen
                </Button>
                
                {stalkerPortals.map((portal) => (
                  <Paper key={portal.id} p="md" withBorder opacity={portal.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{portal.name}</Text>
                          {portal.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{portal.server_url}</Text>
                      </Box>
                      <Button variant="subtle" onClick={() => {
                        setSelectedStalkerPortal(portal);
                        setStalkerWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="xtream">
            <Accordion.Control icon={<Database size={20} />}>
              <Text weight={500}>Xtream Panels</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  onClick={() => {
                    setSelectedXtreamPanel(null);
                    setXtreamWizardOpen(true);
                  }}
                >
                  Xtream Panel Hinzufügen
                </Button>

                {xtreamPanels.map((panel) => (
                  <Paper key={panel.id} p="md" withBorder opacity={panel.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{panel.name}</Text>
                          {panel.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{panel.server_url}</Text>
                      </Box>
                      <Button variant="subtle" onClick={() => {
                        setSelectedXtreamPanel(panel);
                        setXtreamWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="m3u">
            <Accordion.Control icon={<Database size={20} />}>
              <Text weight={500}>M3U-Links (Standard)</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  onClick={() => {
                    setSelectedM3uLink(null);
                    setM3uWizardOpen(true);
                  }}
                >
                  M3U-Link Hinzufügen
                </Button>

                {m3uLinks.map((link) => (
                  <Paper key={link.id} p="md" withBorder opacity={link.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{link.name}</Text>
                          {link.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{link.server_url}</Text>
                      </Box>
                      <Button variant="subtle" onClick={() => {
                        setSelectedM3uLink(link);
                        setM3uWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="plex">
            <Accordion.Control icon={<Server size={20} />}>
              <Text weight={500}>Plex Media Server</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  color="orange"
                  onClick={() => {
                    setSelectedPlexServer(null);
                    setPlexWizardOpen(true);
                  }}
                >
                  Plex Server Hinzufügen
                </Button>

                {plexServers.map((server) => (
                  <Paper key={server.id} p="md" withBorder opacity={server.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{server.name}</Text>
                          {server.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{server.base_url}</Text>
                      </Box>
                      <Button variant="subtle" color="orange" onClick={() => {
                        setSelectedPlexServer(server);
                        setPlexWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="emby">
            <Accordion.Control icon={<Server size={20} />}>
              <Text weight={500}>Emby Media Server</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  color="green"
                  onClick={() => {
                    setSelectedEmbyServer(null);
                    setEmbyWizardOpen(true);
                  }}
                >
                  Emby Server Hinzufügen
                </Button>

                {embyServers.map((server) => (
                  <Paper key={server.id} p="md" withBorder opacity={server.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{server.name}</Text>
                          {server.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{server.base_url}</Text>
                      </Box>
                      <Button variant="subtle" color="green" onClick={() => {
                        setSelectedEmbyServer(server);
                        setEmbyWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="jellyfin">
            <Accordion.Control icon={<Server size={20} />}>
              <Text weight={500}>Jellyfin Media Server</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack>
                <Button 
                  leftSection={<Plus size={16} />} 
                  variant="light"
                  color="violet"
                  onClick={() => {
                    setSelectedJellyfinServer(null);
                    setJellyfinWizardOpen(true);
                  }}
                >
                  Jellyfin Server Hinzufügen
                </Button>

                {jellyfinServers.map((server) => (
                  <Paper key={server.id} p="md" withBorder opacity={server.is_active === false ? 0.6 : 1}>
                    <Group position="apart">
                      <Box>
                        <Group spacing="xs">
                          <Text weight={500}>{server.name}</Text>
                          {server.is_active === false && <Badge color="red" variant="filled">Inaktiv</Badge>}
                        </Group>
                        <Text size="sm" c="dimmed">{server.base_url}</Text>
                      </Box>
                      <Button variant="subtle" color="violet" onClick={() => {
                        setSelectedJellyfinServer(server);
                        setJellyfinWizardOpen(true);
                      }}>
                        Bearbeiten / Einstellungen
                      </Button>
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>

          <Accordion.Item value="epg">
            <Accordion.Control icon={<Database size={20} />}>
              <Text weight={500}>EPG Quellen</Text>
            </Accordion.Control>
            <Accordion.Panel>
              <EPGsTable />
            </Accordion.Panel>
          </Accordion.Item>
        </Accordion>
      )}

      <ArgusFlixProviderWizard
        opened={argusFlixWizardOpen}
        onClose={() => setArgusFlixWizardOpen(false)}
        portal={selectedArgusFlixPortal}
        onSave={() => {
          setArgusFlixWizardOpen(false);
          fetchPlaylists();
        }}
      />

      <StalkerProviderWizard 
        opened={stalkerWizardOpen} 
        onClose={() => setStalkerWizardOpen(false)} 
        portal={selectedStalkerPortal}
        onSave={() => {
          setStalkerWizardOpen(false);
          fetchPlaylists();
        }}
      />

      <XtreamProviderWizard
        opened={xtreamWizardOpen}
        onClose={() => setXtreamWizardOpen(false)}
        portal={selectedXtreamPanel}
        onSave={() => {
          setXtreamWizardOpen(false);
          fetchPlaylists();
        }}
      />

      <M3uProviderWizard
        opened={m3uWizardOpen}
        onClose={() => setM3uWizardOpen(false)}
        portal={selectedM3uLink}
        onSave={() => {
          setM3uWizardOpen(false);
          fetchPlaylists();
        }}
      />

      <PlexProviderWizard
        opened={plexWizardOpen}
        onClose={() => setPlexWizardOpen(false)}
        server={selectedPlexServer}
        onSave={() => {
          setPlexWizardOpen(false);
          fetchServers();
        }}
      />

      <EmbyProviderWizard
        opened={embyWizardOpen}
        onClose={() => setEmbyWizardOpen(false)}
        server={selectedEmbyServer}
        onSave={() => {
          setEmbyWizardOpen(false);
          fetchServers();
        }}
      />

      <JellyfinProviderWizard
        opened={jellyfinWizardOpen}
        onClose={() => setJellyfinWizardOpen(false)}
        server={selectedJellyfinServer}
        onSave={() => {
          setJellyfinWizardOpen(false);
          fetchServers();
        }}
      />
    </Box>
  );
};

const ConnectionsPage = () => {
  return (
    <ErrorBoundary>
      <ConnectionsContent />
    </ErrorBoundary>
  );
};

export default ConnectionsPage;
