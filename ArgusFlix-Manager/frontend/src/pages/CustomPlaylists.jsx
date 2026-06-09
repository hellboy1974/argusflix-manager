import React, { useEffect, useState, useMemo, useCallback } from 'react';
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
  Tabs,
  Collapse,
  Select,
  Pagination,
  Image,
} from '@mantine/core';
import {
  Plus,
  Trash,
  Edit,
  Copy,
  Check,
  ExternalLink,
  ListPlus,
  Search,
  ChevronDown,
  ChevronUp,
  Move,
  Film,
  Tv,
  ListOrdered,
} from 'lucide-react';
import { notifications } from '@mantine/notifications';
import API from '../api';
import ErrorBoundary from '../components/ErrorBoundary';
import CategorySidebar from '../components/CategorySidebar';
import VODRegexRenameModal from '../components/modals/VODRegexRenameModal.jsx';
import { Allotment } from 'allotment';
import 'allotment/dist/style.css';

const CustomPlaylistsPage = () => {
  const [playlists, setPlaylists] = useState([]);
  const [channelGroups, setChannelGroups] = useState([]);
  const [vodCategories, setVodCategories] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  
  // Loading states
  const [loading, setLoading] = useState(false);
  const [loadingGroupsAndCats, setLoadingGroupsAndCats] = useState(false);
  const [savingMappings, setSavingMappings] = useState(false);
  const [loadingItems, setLoadingItems] = useState(false);

  // Modal states
  const [playlistModalOpened, setPlaylistModalOpened] = useState(false);
  const [editPlaylist, setEditPlaylist] = useState(null);
  const [playlistName, setPlaylistName] = useState('');
  const [playlistActive, setPlaylistActive] = useState(true);
  const [savingPlaylist, setSavingPlaylist] = useState(false);

  // Mappings Modal
  const [mappingsModalOpen, setMappingsModalOpen] = useState(false);
  const [tempSelectedGroups, setTempSelectedGroups] = useState([]);
  const [tempSelectedCats, setTempSelectedCats] = useState([]);
  const [groupMappingSearch, setGroupMappingSearch] = useState('');
  const [catMappingSearch, setCatMappingSearch] = useState('');

  // Right pane details / items table state
  const [activeTab, setActiveTab] = useState('live-tv');
  const [selectedCategoryId, setSelectedCategoryId] = useState(null);
  const [items, setItems] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [searchVal, setSearchVal] = useState('');
  const [selectedItemIds, setSelectedItemIds] = useState([]);
  
  // Credentials Collapsible
  const [credentialsOpen, setCredentialsOpen] = useState(false);

  const handlePlaylistSelect = (playlist) => {
    setSelectedPlaylist(playlist);
    setSelectedCategoryId(null);
    setCurrentPage(1);
    setSearchVal('');
    setSelectedItemIds([]);
  };

  const handleTabChange = (val) => {
    setActiveTab(val);
    setSelectedCategoryId(null);
    setCurrentPage(1);
    setSearchVal('');
    setSelectedItemIds([]);
  };

  // Bulk Item Action Modals
  const [regexRenameOpen, setRegexRenameOpen] = useState(false);
  const [regexLoading, setRegexLoading] = useState(false);
  const [moveModalOpen, setMoveModalOpen] = useState(false);
  const [moveLoading, setMoveLoading] = useState(false);
  const [targetCategoryId, setTargetCategoryId] = useState('');
  const [newCategoryName, setNewCategoryName] = useState('');
  const [isCopyAction, setIsCopyAction] = useState(false); // Move vs Copy for Channels

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await API.getCustomPlaylists();
      setPlaylists(data || []);
      if (data && data.length > 0 && !selectedPlaylist) {
        setSelectedPlaylist(data[0]);
      } else if (selectedPlaylist) {
        // Refresh selected playlist state
        const refreshed = data.find(p => p.id === selectedPlaylist.id);
        if (refreshed) setSelectedPlaylist(refreshed);
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

  // Fetch right pane items dynamically
  const fetchCategoryItems = async () => {
    if (!selectedCategoryId || !selectedPlaylist) {
      setItems([]);
      setTotalCount(0);
      return;
    }
    setLoadingItems(true);
    try {
      if (activeTab === 'live-tv') {
        const group = channelGroups.find((g) => g.id === selectedCategoryId);
        if (!group) return;
        const params = new URLSearchParams({
          channel_group: group.name,
          page: String(currentPage),
          page_size: String(pageSize),
        });
        if (searchVal) params.append('name', searchVal);
        const data = await API.getChannelsPage(params);
        setItems(data?.results || data || []);
        setTotalCount(data?.count || (data || []).length);
      } else if (activeTab === 'movies') {
        const cat = vodCategories.find((c) => c.id === selectedCategoryId);
        if (!cat) return;
        const params = new URLSearchParams({
          category: cat.name,
          page: String(currentPage),
          page_size: String(pageSize),
        });
        if (searchVal) params.append('name', searchVal);
        const data = await API.getMovies(params);
        setItems(data?.results || data || []);
        setTotalCount(data?.count || (data || []).length);
      } else if (activeTab === 'series') {
        const cat = vodCategories.find((c) => c.id === selectedCategoryId);
        if (!cat) return;
        const params = new URLSearchParams({
          category: cat.name,
          page: String(currentPage),
          page_size: String(pageSize),
        });
        if (searchVal) params.append('name', searchVal);
        const data = await API.getSeries(params);
        setItems(data?.results || data || []);
        setTotalCount(data?.count || (data || []).length);
      }
    } catch (e) {
      console.error('Failed to load category items', e);
    } finally {
      setLoadingItems(false);
    }
  };

  useEffect(() => {
    setSelectedItemIds([]);
    fetchCategoryItems();
  }, [selectedCategoryId, currentPage, pageSize, searchVal, activeTab]);

  const handleOpenCreateModal = () => {
    setEditPlaylist(null);
    setPlaylistName('');
    setPlaylistActive(true);
    setPlaylistModalOpened(true);
  };

  const handleOpenEditModal = (playlist, e) => {
    e.stopPropagation();
    setEditPlaylist(playlist);
    setPlaylistName(playlist.name);
    setPlaylistActive(playlist.is_active);
    setPlaylistModalOpened(true);
  };

  const handleSavePlaylist = async () => {
    if (!playlistName.trim()) return;
    setSavingPlaylist(true);
    try {
      if (editPlaylist) {
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
      setPlaylistModalOpened(false);
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

  // Open mapping editor modal
  const handleOpenMappingsModal = () => {
    if (!selectedPlaylist) return;
    setTempSelectedGroups(selectedPlaylist.mapped_live_groups || []);
    setTempSelectedCats(selectedPlaylist.mapped_vod_categories || []);
    setGroupMappingSearch('');
    setCatMappingSearch('');
    setMappingsModalOpen(true);
  };

  const handleSaveMappings = async () => {
    if (!selectedPlaylist) return;
    setSavingMappings(true);
    try {
      const updated = await API.updateCustomPlaylist(selectedPlaylist.id, {
        live_groups: tempSelectedGroups,
        vod_categories: tempSelectedCats,
      });
      notifications.show({
        title: 'Success',
        message: 'Mappings saved successfully',
        color: 'green',
      });
      setPlaylists(playlists.map((p) => (p.id === updated.id ? updated : p)));
      setSelectedPlaylist(updated);
      setMappingsModalOpen(false);
    } catch (e) {
      console.error(e);
    } finally {
      setSavingMappings(false);
    }
  };

  // Middle panel Tabbed categories filtering
  const sidebarCategories = useMemo(() => {
    if (!selectedPlaylist) return [];

    if (activeTab === 'live-tv') {
      return channelGroups
        .filter((g) => selectedPlaylist.mapped_live_groups.includes(g.id))
        .map((g) => ({
          id: g.id,
          name: g.name,
          isLiveGroup: true,
          channel_count: g.channels_count || g.channel_count,
        }));
    } else if (activeTab === 'movies') {
      return vodCategories
        .filter((c) => c.category_type === 'movie' && selectedPlaylist.mapped_vod_categories.includes(c.id))
        .map((c) => ({
          id: c.id,
          name: c.name,
          isLiveGroup: false,
          movie_count: c.movie_count,
        }));
    } else if (activeTab === 'series') {
      return vodCategories
        .filter((c) => c.category_type === 'series' && selectedPlaylist.mapped_vod_categories.includes(c.id))
        .map((c) => ({
          id: c.id,
          name: c.name,
          isLiveGroup: false,
          series_count: c.series_count,
        }));
    }
    return [];
  }, [selectedPlaylist, activeTab, channelGroups, vodCategories]);

  // Bulk Regex Rename Apply
  const handleApplyRegexRename = async (find, replace) => {
    setRegexLoading(true);
    try {
      if (activeTab === 'live-tv') {
        await API.bulkRegexRenameChannels(selectedItemIds, find, replace);
      } else if (activeTab === 'movies') {
        await API.bulkRegexRenameMovies({ movie_ids: selectedItemIds, find, replace });
      } else if (activeTab === 'series') {
        await API.bulkRegexRenameSeries({ series_ids: selectedItemIds, find, replace });
      }
      notifications.show({
        title: 'Success',
        message: 'Successfully renamed selected items',
        color: 'green',
      });
      setSelectedItemIds([]);
      setRegexRenameOpen(false);
      fetchCategoryItems();
    } catch (e) {
      console.error(e);
    } finally {
      setRegexLoading(false);
    }
  };

  // Open Bulk Copy/Move Popover/Modal
  const handleOpenMoveCopyModal = (copyAction = false) => {
    setIsCopyAction(copyAction);
    setTargetCategoryId('');
    setNewCategoryName('');
    setMoveModalOpen(true);
  };

  const handleExecuteMoveCopy = async () => {
    if (!targetCategoryId && !newCategoryName.trim()) return;
    setMoveLoading(true);
    try {
      if (activeTab === 'live-tv') {
        if (isCopyAction) {
          // Copy Channels
          await API.bulkCopyChannels({
            channel_ids: selectedItemIds,
            target_group_id: targetCategoryId || null,
            target_name: newCategoryName || null,
          });
          notifications.show({
            title: 'Channels Copied',
            message: 'Successfully copied channels to target group',
            color: 'green',
          });
        } else {
          // Move Channels (Update Group)
          const target = targetCategoryId
            ? { channel_group_id: Number(targetCategoryId) }
            : { channel_group_id: null, channel_group_name: newCategoryName };
          await API.updateChannels(selectedItemIds, target);
          notifications.show({
            title: 'Channels Moved',
            message: 'Successfully moved channels to target group',
            color: 'green',
          });
        }
      } else if (activeTab === 'movies') {
        // Move Movies
        let catId = targetCategoryId;
        if (newCategoryName.trim()) {
          const created = await API.addVODCategory({ name: newCategoryName, category_type: 'movie' });
          catId = created.id;
        }
        await API.bulkMoveMovies({ movie_ids: selectedItemIds, category_id: catId });
        notifications.show({
          title: 'Movies Moved',
          message: 'Successfully moved movies to target category',
          color: 'green',
        });
      } else if (activeTab === 'series') {
        // Move Series
        let catId = targetCategoryId;
        if (newCategoryName.trim()) {
          const created = await API.addVODCategory({ name: newCategoryName, category_type: 'series' });
          catId = created.id;
        }
        await API.bulkMoveSeries({ series_ids: selectedItemIds, category_id: catId });
        notifications.show({
          title: 'Series Moved',
          message: 'Successfully moved series to target category',
          color: 'green',
        });
      }

      setSelectedItemIds([]);
      setMoveModalOpen(false);
      loadGroupsAndCategories();
      fetchCategoryItems();
    } catch (e) {
      console.error(e);
    } finally {
      setMoveLoading(false);
    }
  };

  // Move/Copy target selections
  const moveCopyTargetOptions = useMemo(() => {
    if (activeTab === 'live-tv') {
      return channelGroups.map((g) => ({ value: String(g.id), label: g.name }));
    } else {
      return vodCategories
        .filter((c) => c.category_type === (activeTab === 'movies' ? 'movie' : 'series'))
        .map((c) => ({ value: String(c.id), label: c.name }));
    }
  }, [activeTab, channelGroups, vodCategories]);

  // URLs
  const originHost = window.location.origin;
  const m3uUrl = selectedPlaylist ? `${originHost}/output/custom/${selectedPlaylist.token}/m3u` : '';
  const epgUrl = selectedPlaylist ? `${originHost}/output/custom/${selectedPlaylist.token}/xmltv` : '';
  const xcHostUrl = selectedPlaylist ? `${originHost}/output/custom/${selectedPlaylist.token}` : '';

  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <ErrorBoundary>
      <Flex direction="column" h="100vh" p="sm" style={{ overflow: 'hidden', backgroundColor: '#09090b' }}>
        {/* Top Header */}
        <Group justify="space-between" mb="xs">
          <Group gap="xs">
            <ListPlus size={24} color="#3b82f6" />
            <Title order={3} style={{ letterSpacing: '-0.5px' }}>Custom Playlists</Title>
          </Group>
          <Button leftSection={<Plus size={16} />} color="blue" onClick={handleOpenCreateModal} size="xs">
            New Playlist
          </Button>
        </Group>

        {/* Multi-Pane Workspace */}
        <Box style={{ flex: 1, minHeight: 0 }}>
          <Allotment minSize={200}>
            {/* 1. Left Pane: Playlists list */}
            <Allotment.Pane preferredSize={280} minSize={240} maxSize={400}>
              <Card
                h="100%"
                p="sm"
                style={{
                  backgroundColor: '#18181b',
                  border: '1px solid #27272a',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <Text fw={600} mb="sm" size="xs" c="dimmed">
                  PLAYLISTS ({playlists.length})
                </Text>
                <ScrollArea style={{ flex: 1 }}>
                  {loading ? (
                    <Flex justify="center" p="xl">
                      <Loader size="sm" />
                    </Flex>
                  ) : playlists.length > 0 ? (
                    <Stack gap="xs">
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
                          onClick={() => handlePlaylistSelect(playlist)}
                        >
                          <Flex justify="space-between" align="center">
                            <Box style={{ flex: 1, minWidth: 0, marginRight: 8 }}>
                              <Text size="sm" fw={600} style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                {playlist.name}
                              </Text>
                              <Group gap={4} mt={4}>
                                <Badge color={playlist.is_active ? 'green' : 'red'} size="5px" variant="dot" />
                                <Text size="10px" c="dimmed" style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                  {playlist.mapped_live_groups.length} groups / {playlist.mapped_vod_categories.length} VOD cats
                                </Text>
                              </Group>
                            </Box>
                            <Group gap={4}>
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
                      No custom playlists configured. Create one to get started.
                    </Text>
                  )}
                </ScrollArea>
              </Card>
            </Allotment.Pane>

            {/* 2. Middle Pane: Tabbed Category Mappings */}
            {selectedPlaylist ? (
              <Allotment.Pane preferredSize={300} minSize={250} maxSize={450}>
                <Card
                  h="100%"
                  p="sm"
                  style={{
                    backgroundColor: '#18181b',
                    border: '1px solid #27272a',
                    display: 'flex',
                    flexDirection: 'column',
                    overflow: 'hidden',
                  }}
                >
                  <Flex justify="space-between" align="center" mb="xs">
                    <Text fw={600} size="xs" c="dimmed">MAPPED CONTENT</Text>
                    <Button variant="subtle" size="xs" px={6} onClick={handleOpenMappingsModal}>
                      Manage Mappings
                    </Button>
                  </Flex>

                  <Tabs value={activeTab} onChange={handleTabChange} variant="pills" color="blue" size="xs" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <Tabs.List grow mb="xs">
                      <Tabs.Tab value="live-tv" leftSection={<ListOrdered size={12} />}>Live</Tabs.Tab>
                      <Tabs.Tab value="movies" leftSection={<Film size={12} />}>Movies</Tabs.Tab>
                      <Tabs.Tab value="series" leftSection={<Tv size={12} />}>Series</Tabs.Tab>
                    </Tabs.List>

                    <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
                      <CategorySidebar
                        categories={sidebarCategories}
                        selectedId={selectedCategoryId}
                        onSelect={(id) => setSelectedCategoryId(selectedCategoryId === id ? null : id)}
                        onBulkAction={() => {
                          loadData();
                          loadGroupsAndCategories();
                        }}
                        type="playlist"
                        playlists={playlists}
                        currentPlaylist={selectedPlaylist}
                      />
                    </Box>
                  </Tabs>
                </Card>
              </Allotment.Pane>
            ) : null}

            {/* 3. Right Pane: Paginated Items Table */}
            {selectedPlaylist ? (
              <Allotment.Pane minSize={400}>
                <Flex direction="column" h="100%" gap="xs">
                  {/* Credentials / Collapse trigger */}
                  <Card p="xs" style={{ backgroundColor: '#18181b', border: '1px solid #27272a' }}>
                    <Flex justify="space-between" align="center">
                      <Title order={5} style={{ letterSpacing: '-0.2px' }}>
                        Credentials & Stream Integration
                      </Title>
                      <Button
                        variant="subtle"
                        size="xs"
                        rightSection={credentialsOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                        onClick={() => setCredentialsOpen(!credentialsOpen)}
                      >
                        {credentialsOpen ? 'Hide Links' : 'Show Links'}
                      </Button>
                    </Flex>

                    <Collapse in={credentialsOpen} mt="xs">
                      <Stack gap="xs">
                        <Flex align="center" gap="sm">
                          <Text size="xs" w={120} fw={600} c="dimmed">M3U Link</Text>
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

                        <Flex align="center" gap="sm">
                          <Text size="xs" w={120} fw={600} c="dimmed">XMLTV EPG</Text>
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

                        <Divider label="Xtream Codes Integration Options" labelPosition="center" my="xs" />

                        {/* Option 1: Standard (Token as Username) */}
                        <Box p="xs" style={{ backgroundColor: '#09090b', borderRadius: '4px', border: '1px dashed #27272a' }}>
                          <Text size="xs" fw={700} c="blue" mb="xs">Option 1: Standard (Token as Username)</Text>
                          <Stack gap={6}>
                            <Flex align="center" gap="sm">
                              <Text size="xs" w={100} fw={600} c="dimmed">XC Server URL</Text>
                              <TextInput value={originHost} readOnly style={{ flex: 1 }} size="xs" />
                              <CopyButton value={originHost}>
                                {({ copied, copy }) => (
                                  <Tooltip label={copied ? 'Copied' : 'Copy'}>
                                    <ActionIcon color={copied ? 'teal' : 'gray'} onClick={copy} size="sm">
                                      {copied ? <Check size={12} /> : <Copy size={12} />}
                                    </ActionIcon>
                                  </Tooltip>
                                )}
                              </CopyButton>
                            </Flex>
                            <Group gap="lg">
                              <Text size="xs" c="dimmed">
                                <strong>XC Username:</strong> <Text component="span" c="white" family="monospace">{selectedPlaylist.token}</Text>
                              </Text>
                              <Text size="xs" c="dimmed">
                                <strong>XC Password:</strong> <Text component="span" c="white" family="monospace">custom</Text>
                              </Text>
                            </Group>
                          </Stack>
                        </Box>

                        {/* Option 2: Alternative (Token in Server URL) */}
                        <Box p="xs" style={{ backgroundColor: '#09090b', borderRadius: '4px', border: '1px dashed #27272a' }}>
                          <Text size="xs" fw={700} c="cyan" mb="xs">Option 2: Alternative (Token in Server URL)</Text>
                          <Stack gap={6}>
                            <Flex align="center" gap="sm">
                              <Text size="xs" w={100} fw={600} c="dimmed">XC Server URL</Text>
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
                            <Group gap="lg">
                              <Text size="xs" c="dimmed">
                                <strong>XC Username:</strong> <Text component="span" c="white" family="monospace">custom</Text>
                              </Text>
                              <Text size="xs" c="dimmed">
                                <strong>XC Password:</strong> <Text component="span" c="white" family="monospace">custom</Text>
                              </Text>
                            </Group>
                          </Stack>
                        </Box>
                      </Stack>
                    </Collapse>
                  </Card>

                  {/* List / Table Card */}
                  <Card
                    style={{
                      flex: 1,
                      backgroundColor: '#18181b',
                      border: '1px solid #27272a',
                      display: 'flex',
                      flexDirection: 'column',
                      overflow: 'hidden',
                    }}
                    p="sm"
                  >
                    {selectedCategoryId ? (
                      <Flex direction="column" h="100%" gap="sm">
                        {/* Table Header controls */}
                        <Flex justify="space-between" align="center" wrap="wrap" gap="xs">
                          <TextInput
                            placeholder="Search within mapping..."
                            leftSection={<Search size={14} />}
                            value={searchVal}
                            onChange={(e) => {
                              setSearchVal(e.target.value);
                              setCurrentPage(1);
                            }}
                            size="xs"
                            style={{ flex: 1, minWidth: 200 }}
                          />

                          <Group gap="xs">
                            {selectedItemIds.length > 0 && (
                              <Group gap={6}>
                                <Button size="xs" color="cyan" onClick={() => setRegexRenameOpen(true)}>
                                  Regex Rename ({selectedItemIds.length})
                                </Button>
                                <Button size="xs" color="violet" leftSection={<Move size={12} />} onClick={() => handleOpenMoveCopyModal(false)}>
                                  Move
                                </Button>
                                {activeTab === 'live-tv' && (
                                  <Button size="xs" color="teal" leftSection={<Copy size={12} />} onClick={() => handleOpenMoveCopyModal(true)}>
                                    Copy
                                  </Button>
                                )}
                              </Group>
                            )}
                            <Select
                              value={String(pageSize)}
                              onChange={(val) => {
                                setPageSize(Number(val));
                                setCurrentPage(1);
                              }}
                              data={['10', '25', '50', '100'].map((v) => ({ value: v, label: `${v} / page` }))}
                              size="xs"
                              style={{ width: 100 }}
                            />
                          </Group>
                        </Flex>

                        {/* Table View */}
                        <Box style={{ flex: 1, overflow: 'auto', border: '1px solid #27272a', borderRadius: '8px' }}>
                          {loadingItems ? (
                            <Flex justify="center" align="center" h="100%">
                              <Loader size="md" />
                            </Flex>
                          ) : items.length > 0 ? (
                            <Table striped highlightOnHover verticalSpacing="xs">
                              <TableThead>
                                <TableTr style={{ borderColor: '#27272a' }}>
                                  <TableTh style={{ width: '40px' }}>
                                    <Checkbox
                                      size="xs"
                                      checked={items.length > 0 && selectedItemIds.length === items.length}
                                      indeterminate={selectedItemIds.length > 0 && selectedItemIds.length < items.length}
                                      onChange={(e) => {
                                        if (e.target.checked) {
                                          setSelectedItemIds(items.map((i) => i.id));
                                        } else {
                                          setSelectedItemIds([]);
                                        }
                                      }}
                                    />
                                  </TableTh>
                                  {activeTab === 'live-tv' ? (
                                    <>
                                      <TableTh style={{ width: '60px' }}>Logo</TableTh>
                                      <TableTh style={{ width: '80px' }}>Number</TableTh>
                                      <TableTh>Name</TableTh>
                                    </>
                                  ) : (
                                    <>
                                      <TableTh style={{ width: '60px' }}>Poster</TableTh>
                                      <TableTh>Title</TableTh>
                                      <TableTh style={{ width: '100px' }}>Year</TableTh>
                                      <TableTh>{activeTab === 'movies' ? 'Genre' : 'Episodes'}</TableTh>
                                    </>
                                  )}
                                </TableTr>
                              </TableThead>
                              <TableTbody>
                                {items.map((item) => {
                                  const imgUrl = activeTab === 'live-tv'
                                    ? (item.logo?.url || '')
                                    : (item.movie_image || item.series_image || item.logo?.url || '');

                                  return (
                                    <TableTr key={item.id} style={{ borderColor: '#27272a' }}>
                                      <TableTd>
                                        <Checkbox
                                          size="xs"
                                          checked={selectedItemIds.includes(item.id)}
                                          onChange={(e) => {
                                            if (e.target.checked) {
                                              setSelectedItemIds([...selectedItemIds, item.id]);
                                            } else {
                                              setSelectedItemIds(selectedItemIds.filter((id) => id !== item.id));
                                            }
                                          }}
                                        />
                                      </TableTd>
                                      <TableTd>
                                        {imgUrl ? (
                                          <Image
                                            src={imgUrl}
                                            height={activeTab === 'live-tv' ? 24 : 40}
                                            width={activeTab === 'live-tv' ? 24 : 28}
                                            fit="contain"
                                            style={{ borderRadius: '4px' }}
                                          />
                                        ) : (
                                          <Box
                                            style={{
                                              height: activeTab === 'live-tv' ? 24 : 40,
                                              width: activeTab === 'live-tv' ? 24 : 28,
                                              backgroundColor: '#27272a',
                                              borderRadius: '4px',
                                              display: 'flex',
                                              alignItems: 'center',
                                              justifyContent: 'center',
                                            }}
                                          >
                                            {activeTab === 'live-tv' ? <ListOrdered size={12} /> : activeTab === 'movies' ? <Film size={12} /> : <Tv size={12} />}
                                          </Box>
                                        )}
                                      </TableTd>
                                      {activeTab === 'live-tv' ? (
                                        <>
                                          <TableTd>{item.channel_number || '-'}</TableTd>
                                          <TableTd fw={500}>{item.name}</TableTd>
                                        </>
                                      ) : (
                                        <>
                                          <TableTd fw={500}>{item.name}</TableTd>
                                          <TableTd c="dimmed" size="xs">{item.year || '-'}</TableTd>
                                          <TableTd c="dimmed" size="xs">
                                            {activeTab === 'movies' ? (item.genre || '-') : (item.episode_count || 0)}
                                          </TableTd>
                                        </>
                                      )}
                                    </TableTr>
                                  );
                                })}
                              </TableTbody>
                            </Table>
                          ) : (
                            <Flex justify="center" align="center" h="100%" p="xl">
                              <Text size="sm" c="dimmed">No content items found under this category.</Text>
                            </Flex>
                          )}
                        </Box>

                        {/* Pagination */}
                        {totalPages > 1 && (
                          <Flex justify="center">
                            <Pagination
                              page={currentPage}
                              onChange={setCurrentPage}
                              total={totalPages}
                              size="sm"
                            />
                          </Flex>
                        )}
                      </Flex>
                    ) : (
                      <Flex justify="center" align="center" h="100%" direction="column" p="xl">
                        <ListPlus size={48} color="#52525b" strokeWidth={1} />
                        <Text c="dimmed" mt="sm" size="xs">
                          Select a mapped category in the middle panel to inspect content items.
                        </Text>
                      </Flex>
                    )}
                  </Card>
                </Flex>
              </Allotment.Pane>
            ) : (
              <Flex flex={1} justify="center" align="center" direction="column" style={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px' }}>
                <ListPlus size={64} color="#52525b" strokeWidth={1} />
                <Text c="dimmed" mt="md" size="sm">
                  Select or create a Custom Playlist to configure mappings.
                </Text>
              </Flex>
            )}
          </Allotment>
        </Box>

        {/* 4. Mappings Editor Modal */}
        {selectedPlaylist && (
          <Modal
            opened={mappingsModalOpen}
            onClose={() => setMappingsModalOpen(false)}
            title={`Manage Mappings - ${selectedPlaylist.name}`}
            size="lg"
            centered
          >
            <Tabs defaultValue="live" color="blue" size="sm">
              <Tabs.List grow mb="md">
                <Tabs.Tab value="live">Live TV Groups</Tabs.Tab>
                <Tabs.Tab value="movies">VOD Movie Categories</Tabs.Tab>
                <Tabs.Tab value="series">VOD Series Categories</Tabs.Tab>
              </Tabs.List>

              <Tabs.Panel value="live">
                <TextInput
                  placeholder="Search groups..."
                  value={groupMappingSearch}
                  onChange={(e) => setGroupMappingSearch(e.target.value)}
                  size="xs"
                  mb="sm"
                />
                <Group gap="xs" mb="sm">
                  <Button
                    variant="outline"
                    size="xs"
                    onClick={() => {
                      const visible = channelGroups.filter((g) => g.name.toLowerCase().includes(groupMappingSearch.toLowerCase())).map((g) => g.id);
                      setTempSelectedGroups(Array.from(new Set([...tempSelectedGroups, ...visible])));
                    }}
                  >
                    Select All
                  </Button>
                  <Button
                    variant="outline"
                    color="red"
                    size="xs"
                    onClick={() => {
                      const visible = channelGroups.filter((g) => g.name.toLowerCase().includes(groupMappingSearch.toLowerCase())).map((g) => g.id);
                      setTempSelectedGroups(tempSelectedGroups.filter((id) => !visible.includes(id)));
                    }}
                  >
                    Clear Filtered
                  </Button>
                </Group>
                <ScrollArea h={300} style={{ border: '1px solid #27272a', borderRadius: '6px', padding: 8 }}>
                  <Stack gap="xs">
                    {channelGroups
                      .filter((g) => g.name.toLowerCase().includes(groupMappingSearch.toLowerCase()))
                      .map((group) => (
                        <Checkbox
                          key={group.id}
                          label={`${group.name} (${group.channels_count || group.channel_count || 0} channels)`}
                          checked={tempSelectedGroups.includes(group.id)}
                          onChange={() => {
                            if (tempSelectedGroups.includes(group.id)) {
                              setTempSelectedGroups(tempSelectedGroups.filter((id) => id !== group.id));
                            } else {
                              setTempSelectedGroups([...tempSelectedGroups, group.id]);
                            }
                          }}
                          size="xs"
                        />
                      ))}
                  </Stack>
                </ScrollArea>
              </Tabs.Panel>

              <Tabs.Panel value="movies">
                <TextInput
                  placeholder="Search movie categories..."
                  value={catMappingSearch}
                  onChange={(e) => setCatMappingSearch(e.target.value)}
                  size="xs"
                  mb="sm"
                />
                <Group gap="xs" mb="sm">
                  <Button
                    variant="outline"
                    size="xs"
                    onClick={() => {
                      const visible = vodCategories
                        .filter((c) => c.category_type === 'movie' && c.name.toLowerCase().includes(catMappingSearch.toLowerCase()))
                        .map((c) => c.id);
                      setTempSelectedCats(Array.from(new Set([...tempSelectedCats, ...visible])));
                    }}
                  >
                    Select All
                  </Button>
                  <Button
                    variant="outline"
                    color="red"
                    size="xs"
                    onClick={() => {
                      const visible = vodCategories
                        .filter((c) => c.category_type === 'movie' && c.name.toLowerCase().includes(catMappingSearch.toLowerCase()))
                        .map((c) => c.id);
                      setTempSelectedCats(tempSelectedCats.filter((id) => !visible.includes(id)));
                    }}
                  >
                    Clear Filtered
                  </Button>
                </Group>
                <ScrollArea h={300} style={{ border: '1px solid #27272a', borderRadius: '6px', padding: 8 }}>
                  <Stack gap="xs">
                    {vodCategories
                      .filter((c) => c.category_type === 'movie' && c.name.toLowerCase().includes(catMappingSearch.toLowerCase()))
                      .map((cat) => (
                        <Checkbox
                          key={cat.id}
                          label={`${cat.name} (${cat.movie_count || 0} movies)`}
                          checked={tempSelectedCats.includes(cat.id)}
                          onChange={() => {
                            if (tempSelectedCats.includes(cat.id)) {
                              setTempSelectedCats(tempSelectedCats.filter((id) => id !== cat.id));
                            } else {
                              setTempSelectedCats([...tempSelectedCats, cat.id]);
                            }
                          }}
                          size="xs"
                        />
                      ))}
                  </Stack>
                </ScrollArea>
              </Tabs.Panel>

              <Tabs.Panel value="series">
                <TextInput
                  placeholder="Search series categories..."
                  value={catMappingSearch}
                  onChange={(e) => setCatMappingSearch(e.target.value)}
                  size="xs"
                  mb="sm"
                />
                <Group gap="xs" mb="sm">
                  <Button
                    variant="outline"
                    size="xs"
                    onClick={() => {
                      const visible = vodCategories
                        .filter((c) => c.category_type === 'series' && c.name.toLowerCase().includes(catMappingSearch.toLowerCase()))
                        .map((c) => c.id);
                      setTempSelectedCats(Array.from(new Set([...tempSelectedCats, ...visible])));
                    }}
                  >
                    Select All
                  </Button>
                  <Button
                    variant="outline"
                    color="red"
                    size="xs"
                    onClick={() => {
                      const visible = vodCategories
                        .filter((c) => c.category_type === 'series' && c.name.toLowerCase().includes(catMappingSearch.toLowerCase()))
                        .map((c) => c.id);
                      setTempSelectedCats(tempSelectedCats.filter((id) => !visible.includes(id)));
                    }}
                  >
                    Clear Filtered
                  </Button>
                </Group>
                <ScrollArea h={300} style={{ border: '1px solid #27272a', borderRadius: '6px', padding: 8 }}>
                  <Stack gap="xs">
                    {vodCategories
                      .filter((c) => c.category_type === 'series' && c.name.toLowerCase().includes(catMappingSearch.toLowerCase()))
                      .map((cat) => (
                        <Checkbox
                          key={cat.id}
                          label={`${cat.name} (${cat.series_count || 0} series)`}
                          checked={tempSelectedCats.includes(cat.id)}
                          onChange={() => {
                            if (tempSelectedCats.includes(cat.id)) {
                              setTempSelectedCats(tempSelectedCats.filter((id) => id !== cat.id));
                            } else {
                              setTempSelectedCats([...tempSelectedCats, cat.id]);
                            }
                          }}
                          size="xs"
                        />
                      ))}
                  </Stack>
                </ScrollArea>
              </Tabs.Panel>
            </Tabs>

            <Group justify="right" mt="md">
              <Button variant="outline" color="gray" onClick={() => setMappingsModalOpen(false)}>
                Cancel
              </Button>
              <Button color="blue" onClick={handleSaveMappings} loading={savingMappings}>
                Save Mappings
              </Button>
            </Group>
          </Modal>
        )}

        {/* 5. Create / Edit Playlist Modal */}
        <Modal
          opened={playlistModalOpened}
          onClose={() => setPlaylistModalOpened(false)}
          title={editPlaylist ? 'Edit Custom Playlist' : 'Create Custom Playlist'}
          size="sm"
          centered
        >
          <Stack gap="md">
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
            <Group justify="right" mt="md">
              <Button variant="outline" color="gray" onClick={() => setPlaylistModalOpened(false)}>
                Cancel
              </Button>
              <Button color="blue" onClick={handleSavePlaylist} loading={savingPlaylist}>
                Save Playlist
              </Button>
            </Group>
          </Stack>
        </Modal>

        {/* 6. VOD/Channels Bulk Regex Rename Modal */}
        <VODRegexRenameModal
          opened={regexRenameOpen}
          onClose={() => setRegexRenameOpen(false)}
          items={items.filter((i) => selectedItemIds.includes(i.id))}
          loading={regexLoading}
          onApply={handleApplyRegexRename}
          title={activeTab === 'live-tv' ? 'Regex Channels Rename' : activeTab === 'movies' ? 'Regex Movies Rename' : 'Regex Series Rename'}
        />

        {/* 7. Bulk Move / Copy Modal */}
        <Modal
          opened={moveModalOpen}
          onClose={() => setMoveModalOpen(false)}
          title={isCopyAction ? 'Copy Selected to Group' : 'Move Selected to Category/Group'}
          size="sm"
          centered
        >
          <Stack gap="md">
            <Select
              label={activeTab === 'live-tv' ? 'Target Group' : 'Target Category'}
              placeholder="Select target..."
              data={moveCopyTargetOptions}
              value={targetCategoryId}
              onChange={setTargetCategoryId}
              searchable
            />
            
            <TextInput
              label={activeTab === 'live-tv' ? 'Or create target group' : 'Or create target category'}
              placeholder="Type new name..."
              value={newCategoryName}
              onChange={(e) => setNewCategoryName(e.target.value)}
            />

            <Group justify="right" mt="md">
              <Button variant="outline" color="gray" onClick={() => setMoveModalOpen(false)}>
                Cancel
              </Button>
              <Button color="blue" onClick={handleExecuteMoveCopy} loading={moveLoading} disabled={!targetCategoryId && !newCategoryName.trim()}>
                {isCopyAction ? 'Copy Items' : 'Move Items'}
              </Button>
            </Group>
          </Stack>
        </Modal>
      </Flex>
    </ErrorBoundary>
  );
};

export default CustomPlaylistsPage;
