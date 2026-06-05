import React, { useEffect, useState } from 'react';
import {
  Box,
  Flex,
  Group,
  Text,
  Title,
  Button,
  TextInput,
  Table,
  TableTbody,
  TableTd,
  TableTh,
  TableThead,
  TableTr,
  ScrollArea,
  Card,
  Checkbox,
  Stack,
  Loader,
  Badge,
  ActionIcon,
  Modal,
  Switch,
  CopyButton,
  Tooltip,
  Divider,
} from '@mantine/core';
import { Plus, Trash, Edit, Copy, Check, ExternalLink, ListPlus } from 'lucide-react';
import { notifications } from '@mantine/notifications';
import API from '../api';
import ErrorBoundary from '../components/ErrorBoundary';

const CustomPlaylistsPage = () => {
  const [playlists, setPlaylists] = useState([]);
  const [channelGroups, setChannelGroups] = useState([]);
  const [vodCategories, setVodCategories] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingGroupsAndCats, setLoadingGroupsAndCats] = useState(false);
  const [savingMappings, setSavingMappings] = useState(false);

  // Modal states
  const [modalOpened, setModalOpened] = useState(false);
  const [editPlaylist, setEditPlaylist] = useState(null);
  const [playlistName, setPlaylistName] = useState('');
  const [playlistActive, setPlaylistActive] = useState(true);
  const [savingPlaylist, setSavingPlaylist] = useState(false);

  // Mapping state
  const [selectedGroups, setSelectedGroups] = useState([]);
  const [selectedCats, setSelectedCats] = useState([]);
  
  // Search within mapper cards
  const [groupSearch, setGroupSearch] = useState('');
  const [catSearch, setCatSearch] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await API.getCustomPlaylists();
      setPlaylists(data || []);
      if (data && data.length > 0 && !selectedPlaylist) {
        setSelectedPlaylist(data[0]);
      }
    } catch (e) {
      console.error('Failed to load custom playlists', e);
    } finally {
      setLoading(false);
    }
  };

  const loadGroupsAndCategories = async () => {
    setLoadingGroupsAndCats(true);
    try {
      const groups = await API.getChannelGroups();
      const categories = await API.getVODCategories();
      setChannelGroups(groups || []);
      
      // Handle both array and paginated VOD categories response
      const catsList = categories?.results || categories || [];
      setVodCategories(catsList);
    } catch (e) {
      console.error('Failed to load channel groups or VOD categories', e);
    } finally {
      setLoadingGroupsAndCats(false);
    }
  };

  useEffect(() => {
    loadData();
    loadGroupsAndCategories();
  }, []);

  useEffect(() => {
    if (selectedPlaylist) {
      setSelectedGroups(selectedPlaylist.mapped_live_groups || []);
      setSelectedCats(selectedPlaylist.mapped_vod_categories || []);
    } else {
      setSelectedGroups([]);
      setSelectedCats([]);
    }
  }, [selectedPlaylist]);

  const handleOpenCreateModal = () => {
    setEditPlaylist(null);
    setPlaylistName('');
    setPlaylistActive(true);
    setModalOpened(true);
  };

  const handleOpenEditModal = (playlist, e) => {
    e.stopPropagation();
    setEditPlaylist(playlist);
    setPlaylistName(playlist.name);
    setPlaylistActive(playlist.is_active);
    setModalOpened(true);
  };

  const handleSavePlaylist = async () => {
    if (!playlistName.trim()) return;
    setSavingPlaylist(true);
    try {
      if (editPlaylist) {
        // Edit
        const updated = await API.updateCustomPlaylist(editPlaylist.id, {
          name: playlistName,
          is_active: playlistActive,
        });
        notifications.show({
          title: 'Success',
          message: 'Playlist updated successfully',
          color: 'green',
        });
        setPlaylists(playlists.map((p) => (p.id === updated.id ? updated : p)));
        if (selectedPlaylist?.id === updated.id) {
          setSelectedPlaylist(updated);
        }
      } else {
        // Create
        const created = await API.createCustomPlaylist({
          name: playlistName,
          is_active: playlistActive,
        });
        notifications.show({
          title: 'Success',
          message: 'Playlist created successfully',
          color: 'green',
        });
        setPlaylists([...playlists, created]);
        setSelectedPlaylist(created);
      }
      setModalOpened(false);
    } catch (e) {
      console.error(e);
    } finally {
      setSavingPlaylist(false);
    }
  };

  const handleDeletePlaylist = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this custom playlist?')) return;
    try {
      await API.deleteCustomPlaylist(id);
      notifications.show({
        title: 'Success',
        message: 'Playlist deleted',
        color: 'green',
      });
      const remaining = playlists.filter((p) => p.id !== id);
      setPlaylists(remaining);
      if (selectedPlaylist?.id === id) {
        setSelectedPlaylist(remaining.length > 0 ? remaining[0] : null);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSaveMappings = async () => {
    if (!selectedPlaylist) return;
    setSavingMappings(true);
    try {
      const updated = await API.updateCustomPlaylist(selectedPlaylist.id, {
        live_groups: selectedGroups,
        vod_categories: selectedCats,
      });
      notifications.show({
        title: 'Mappings Saved',
        message: 'Channel groups and VOD categories mapped successfully',
        color: 'green',
      });
      setPlaylists(playlists.map((p) => (p.id === updated.id ? updated : p)));
      setSelectedPlaylist(updated);
    } catch (e) {
      console.error(e);
    } finally {
      setSavingMappings(false);
    }
  };

  const toggleGroup = (groupId) => {
    if (selectedGroups.includes(groupId)) {
      setSelectedGroups(selectedGroups.filter((id) => id !== groupId));
    } else {
      setSelectedGroups([...selectedGroups, groupId]);
    }
  };

  const toggleCat = (catId) => {
    if (selectedCats.includes(catId)) {
      setSelectedCats(selectedCats.filter((id) => id !== catId));
    } else {
      setSelectedCats([...selectedCats, catId]);
    }
  };

  const selectAllGroups = () => {
    const visibleIds = filteredGroups.map((g) => g.id);
    const newSelected = Array.from(new Set([...selectedGroups, ...visibleIds]));
    setSelectedGroups(newSelected);
  };

  const deselectAllGroups = () => {
    const visibleIds = filteredGroups.map((g) => g.id);
    setSelectedGroups(selectedGroups.filter((id) => !visibleIds.includes(id)));
  };

  const selectAllCats = () => {
    const visibleIds = filteredCats.map((c) => c.id);
    const newSelected = Array.from(new Set([...selectedCats, ...visibleIds]));
    setSelectedCats(newSelected);
  };

  const deselectAllCats = () => {
    const visibleIds = filteredCats.map((c) => c.id);
    setSelectedCats(selectedCats.filter((id) => !visibleIds.includes(id)));
  };

  // Filter lists based on search
  const filteredGroups = channelGroups.filter((g) =>
    g.name.toLowerCase().includes(groupSearch.toLowerCase())
  );

  const filteredCats = vodCategories.filter((c) =>
    c.name.toLowerCase().includes(catSearch.toLowerCase())
  );

  const originHost = window.location.origin;
  const m3uUrl = selectedPlaylist ? `${originHost}/output/custom/${selectedPlaylist.token}/m3u` : '';
  const epgUrl = selectedPlaylist ? `${originHost}/output/custom/${selectedPlaylist.token}/xmltv` : '';
  const xcHostUrl = selectedPlaylist ? `${originHost}/output/custom/${selectedPlaylist.token}` : '';

  return (
    <ErrorBoundary>
      <Flex direction="column" h="100vh" p="md" style={{ overflow: 'hidden', backgroundColor: '#09090b' }}>
        <Group position="apart" mb="md">
          <Group spacing="xs">
            <ListPlus size={24} color="#3b82f6" />
            <Title order={3}>Custom Playlist Builder</Title>
          </Group>
          <Button leftSection={<Plus size={16} />} color="blue" onClick={handleOpenCreateModal}>
            New Playlist
          </Button>
        </Group>

        <Flex gap="md" style={{ flex: 1, minHeight: 0 }}>
          {/* Playlists Left Side List */}
          <Card
            w={320}
            p="md"
            style={{
              backgroundColor: '#18181b',
              border: '1px solid #27272a',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Text weight={600} mb="sm" size="sm" c="dimmed">
              PLAYLISTS ({playlists.length})
            </Text>
            <ScrollArea flex={1}>
              {loading ? (
                <Flex justify="center" p="xl">
                  <Loader size="sm" />
                </Flex>
              ) : playlists.length > 0 ? (
                <Stack spacing="xs">
                  {playlists.map((playlist) => (
                    <Box
                      key={playlist.id}
                      p="sm"
                      style={{
                        borderRadius: '6px',
                        cursor: 'pointer',
                        backgroundColor: selectedPlaylist?.id === playlist.id ? '#27272a' : '#09090b',
                        border: '1px solid #27272a',
                        transition: 'background-color 0.2s',
                      }}
                      onClick={() => setSelectedPlaylist(playlist)}
                    >
                      <Flex justify="space-between" align="center">
                        <Box>
                          <Text size="sm" weight={600}>
                            {playlist.name}
                          </Text>
                          <Group spacing={4} mt={4}>
                            <Badge color={playlist.is_active ? 'green' : 'red'} size="xs" variant="light">
                              {playlist.is_active ? 'Active' : 'Inactive'}
                            </Badge>
                            <Text size="10px" c="dimmed">
                              {playlist.mapped_live_groups.length} groups / {playlist.mapped_vod_categories.length} VOD cats
                            </Text>
                          </Group>
                        </Box>
                        <Group spacing={4}>
                          <ActionIcon
                            size="sm"
                            variant="subtle"
                            color="blue"
                            onClick={(e) => handleOpenEditModal(playlist, e)}
                          >
                            <Edit size={12} />
                          </ActionIcon>
                          <ActionIcon
                            size="sm"
                            variant="subtle"
                            color="red"
                            onClick={(e) => handleDeletePlaylist(playlist.id, e)}
                          >
                            <Trash size={12} />
                          </ActionIcon>
                        </Group>
                      </Flex>
                    </Box>
                  ))}
                </Stack>
              ) : (
                <Text size="xs" c="dimmed" align="center" mt="xl">
                  No custom playlists configured. Create one to map channel groups and categories.
                </Text>
              )}
            </ScrollArea>
          </Card>

          {/* Right Pane: Mappings and Link generation */}
          {selectedPlaylist ? (
            <Flex direction="column" flex={1} style={{ minHeight: 0 }} gap="md">
              {/* Credentials / Links Card */}
              <Card p="md" style={{ backgroundColor: '#18181b', border: '1px solid #27272a' }}>
                <Title order={5} mb="sm" style={{ letterSpacing: '-0.2px' }}>
                  Streaming Integration & Credentials
                </Title>
                <Stack spacing="xs">
                  {/* M3U */}
                  <Flex align="center" gap="sm">
                    <Text size="xs" w={100} weight={600} c="dimmed">M3U Link</Text>
                    <TextInput value={m3uUrl} readOnly style={{ flex: 1 }} size="xs" />
                    <CopyButton value={m3uUrl}>
                      {({ copied, copy }) => (
                        <Tooltip label={copied ? 'Copied' : 'Copy'}>
                          <ActionIcon color={copied ? 'teal' : 'gray'} onClick={copy} size="sm">
                            {copied ? <Check size={12} /> : <Copy size={12} />}
                          </ActionIcon>
                        </Tooltip>
                      )}
                    </CopyButton>
                  </Flex>

                  {/* XMLTV */}
                  <Flex align="center" gap="sm">
                    <Text size="xs" w={100} weight={600} c="dimmed">XMLTV EPG</Text>
                    <TextInput value={epgUrl} readOnly style={{ flex: 1 }} size="xs" />
                    <CopyButton value={epgUrl}>
                      {({ copied, copy }) => (
                        <Tooltip label={copied ? 'Copied' : 'Copy'}>
                          <ActionIcon color={copied ? 'teal' : 'gray'} onClick={copy} size="sm">
                            {copied ? <Check size={12} /> : <Copy size={12} />}
                          </ActionIcon>
                        </Tooltip>
                      )}
                    </CopyButton>
                  </Flex>

                  {/* Xtream Codes */}
                  <Flex align="center" gap="sm">
                    <Text size="xs" w={100} weight={600} c="dimmed">XC Server Host</Text>
                    <TextInput value={xcHostUrl} readOnly style={{ flex: 1 }} size="xs" />
                    <CopyButton value={xcHostUrl}>
                      {({ copied, copy }) => (
                        <Tooltip label={copied ? 'Copied' : 'Copy'}>
                          <ActionIcon color={copied ? 'teal' : 'gray'} onClick={copy} size="sm">
                            {copied ? <Check size={12} /> : <Copy size={12} />}
                          </ActionIcon>
                        </Tooltip>
                      )}
                    </CopyButton>
                  </Flex>

                  <Group spacing="lg" mt={4}>
                    <Text size="xs" c="dimmed">
                      <strong>XC Username:</strong> <Text component="span" c="white" family="monospace">{selectedPlaylist.token}</Text>
                    </Text>
                    <Text size="xs" c="dimmed">
                      <strong>XC Password:</strong> <Text component="span" c="white" family="monospace">custom</Text>
                    </Text>
                  </Group>
                </Stack>
              </Card>

              {/* Matrix Content Mapper */}
              <Flex gap="md" style={{ flex: 1, minHeight: 0 }}>
                {/* Channel Groups Card */}
                <Card
                  flex={1}
                  p="md"
                  style={{
                    backgroundColor: '#18181b',
                    border: '1px solid #27272a',
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <Group position="apart" mb="xs">
                    <Text weight={600} size="sm" c="dimmed">
                      LIVE CHANNEL GROUPS ({selectedGroups.length} / {channelGroups.length} selected)
                    </Text>
                    <Group spacing={4}>
                      <Button variant="subtle" size="xs" p={0} onClick={selectAllGroups}>
                        Select All
                      </Button>
                      <Text size="xs" c="dimmed">|</Text>
                      <Button variant="subtle" size="xs" p={0} color="red" onClick={deselectAllGroups}>
                        Clear
                      </Button>
                    </Group>
                  </Group>
                  <TextInput
                    placeholder="Search groups..."
                    value={groupSearch}
                    onChange={(e) => setGroupSearch(e.target.value)}
                    size="xs"
                    mb="sm"
                  />
                  <ScrollArea flex={1}>
                    {loadingGroupsAndCats ? (
                      <Loader size="xs" />
                    ) : filteredGroups.length > 0 ? (
                      <Stack spacing="xs">
                        {filteredGroups.map((group) => (
                          <Checkbox
                            key={group.id}
                            label={`${group.name} (${group.channels_count || 0} channels)`}
                            checked={selectedGroups.includes(group.id)}
                            onChange={() => toggleGroup(group.id)}
                            size="xs"
                          />
                        ))}
                      </Stack>
                    ) : (
                      <Text size="xs" c="dimmed" align="center" py="xl">
                        No groups match search.
                      </Text>
                    )}
                  </ScrollArea>
                </Card>

                {/* VOD Categories Card */}
                <Card
                  flex={1}
                  p="md"
                  style={{
                    backgroundColor: '#18181b',
                    border: '1px solid #27272a',
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <Group position="apart" mb="xs">
                    <Text weight={600} size="sm" c="dimmed">
                      VOD CATEGORIES ({selectedCats.length} / {vodCategories.length} selected)
                    </Text>
                    <Group spacing={4}>
                      <Button variant="subtle" size="xs" p={0} onClick={selectAllCats}>
                        Select All
                      </Button>
                      <Text size="xs" c="dimmed">|</Text>
                      <Button variant="subtle" size="xs" p={0} color="red" onClick={deselectAllCats}>
                        Clear
                      </Button>
                    </Group>
                  </Group>
                  <TextInput
                    placeholder="Search categories..."
                    value={catSearch}
                    onChange={(e) => setCatSearch(e.target.value)}
                    size="xs"
                    mb="sm"
                  />
                  <ScrollArea flex={1}>
                    {loadingGroupsAndCats ? (
                      <Loader size="xs" />
                    ) : filteredCats.length > 0 ? (
                      <Stack spacing="xs">
                        {filteredCats.map((cat) => (
                          <Checkbox
                            key={cat.id}
                            label={`${cat.name} (${cat.category_type})`}
                            checked={selectedCats.includes(cat.id)}
                            onChange={() => toggleCat(cat.id)}
                            size="xs"
                          />
                        ))}
                      </Stack>
                    ) : (
                      <Text size="xs" c="dimmed" align="center" py="xl">
                        No VOD categories match search.
                      </Text>
                    )}
                  </ScrollArea>
                </Card>
              </Flex>

              {/* Save Button Row */}
              <Group position="right">
                <Button
                  color="blue"
                  onClick={handleSaveMappings}
                  loading={savingMappings}
                  leftSection={<Check size={16} />}
                >
                  Save Mappings
                </Button>
              </Group>
            </Flex>
          ) : (
            <Flex flex={1} justify="center" align="center" direction="column" style={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px' }}>
              <ListPlus size={64} color="#52525b" strokeWidth={1} />
              <Text c="dimmed" mt="md" size="sm">
                Select or create a Custom Playlist to configure mappings.
              </Text>
            </Flex>
          )}
        </Flex>

        {/* Create / Edit Modal */}
        <Modal
          opened={modalOpened}
          onClose={() => setModalOpened(false)}
          title={editPlaylist ? 'Edit Custom Playlist' : 'Create Custom Playlist'}
          size="sm"
          centered
        >
          <Stack spacing="md">
            <TextInput
              label="Playlist Name"
              placeholder="e.g. My Custom playlist"
              value={playlistName}
              onChange={(e) => setPlaylistName(e.target.value)}
              required
            />
            <Switch
              label="Active Status"
              checked={playlistActive}
              onChange={(e) => setPlaylistActive(e.currentTarget.checked)}
            />
            <Group position="right" mt="md">
              <Button variant="outline" color="gray" onClick={() => setModalOpened(false)}>
                Cancel
              </Button>
              <Button color="blue" onClick={handleSavePlaylist} loading={savingPlaylist}>
                Save Playlist
              </Button>
            </Group>
          </Stack>
        </Modal>
      </Flex>
    </ErrorBoundary>
  );
};

export default CustomPlaylistsPage;
