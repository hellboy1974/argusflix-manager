import React, { useState, useMemo } from 'react';
import {
  Card,
  Text,
  TextInput,
  Checkbox,
  ScrollArea,
  Badge,
  Group,
  Stack,
  ActionIcon,
  Modal,
  Button,
  Select,
  Box,
  Tooltip,
  Divider,
  Popover,
} from '@mantine/core';
import {
  Search,
  Move,
  Copy,
  Edit,
  Trash2,
  Settings,
  HelpCircle,
  FileEdit,
  Check,
  Link,
  ListPlus,
} from 'lucide-react';
import { notifications } from '@mantine/notifications';
import API from '../api';

const CategorySidebar = ({
  categories = [],
  selectedId = null,
  onSelect = () => {},
  onBulkAction = () => {},
  type = 'live-tv', // 'live-tv', 'movie', 'series', 'playlist'
  playlists = [], // For mapping operations
  currentPlaylist = null, // For playlist page
}) => {
  const [search, setSearch] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);

  // Modal states
  const [activeModal, setActiveModal] = useState(null); // 'rename' | 'move' | 'copy' | 'regex' | 'delete'
  const [loading, setLoading] = useState(false);

  // Single/Bulk Rename State
  const [renameMappings, setRenameMappings] = useState({});

  // Move/Copy State
  const [targetGroupId, setTargetGroupId] = useState('');
  const [targetGroupName, setTargetGroupName] = useState('');
  const [targetPlaylistId, setTargetPlaylistId] = useState('');

  // Regex State
  const [findPat, setFindPat] = useState('');
  const [replacePat, setReplacePat] = useState('');

  // Quick-mapping Popover state
  const [openedPopoverId, setOpenedPopoverId] = useState(null);

  // Bulk Playlist Assignment State
  const [selectedPlaylistIds, setSelectedPlaylistIds] = useState([]);

  // Filter categories by search query
  const filteredCategories = useMemo(() => {
    return categories.filter((c) =>
      (c.name || '').toLowerCase().includes(search.toLowerCase())
    );
  }, [categories, search]);

  const selectedItems = useMemo(() => {
    return categories.filter((c) => selectedIds.includes(c.id));
  }, [categories, selectedIds]);

  const toggleSelectAll = () => {
    if (selectedIds.length === filteredCategories.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredCategories.map((c) => c.id));
    }
  };

  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((x) => x !== id));
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  // Open Actions Modals
  const openRenameModal = () => {
    const initialMappings = {};
    selectedItems.forEach((item) => {
      initialMappings[item.id] = item.name;
    });
    setRenameMappings(initialMappings);
    setActiveModal('rename');
  };

  const openMoveModal = () => {
    setTargetGroupId('');
    setTargetGroupName('');
    setTargetPlaylistId('');
    setActiveModal('move');
  };

  const openCopyModal = () => {
    setTargetGroupId('');
    setTargetGroupName('');
    setTargetPlaylistId('');
    setActiveModal('copy');
  };

  const openRegexModal = () => {
    setFindPat('');
    setReplacePat('');
    setActiveModal('regex');
  };

  const openDeleteModal = () => {
    setActiveModal('delete');
  };

  // Execute Rename
  const handleRename = async () => {
    setLoading(true);
    try {
      if (type === 'live-tv') {
        await API.bulkRenameChannelGroups({ rename_mappings: renameMappings });
      } else if (type === 'movie' || type === 'series') {
        await API.bulkRenameVODCategories({ rename_mappings: renameMappings });
      }
      notifications.show({
        title: 'Success',
        message: 'Successfully renamed categories',
        color: 'green',
      });
      setSelectedIds([]);
      setActiveModal(null);
      onBulkAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Execute Move
  const handleMove = async () => {
    setLoading(true);
    try {
      if (type === 'playlist' && currentPlaylist) {
        // Move category mappings from current playlist to another playlist
        if (!targetPlaylistId) return;
        const targetPlaylist = playlists.find((p) => String(p.id) === targetPlaylistId);
        if (!targetPlaylist) return;

        // Copy selected category IDs to target playlist
        const selectedLive = selectedItems.filter(c => c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('live-', ''), 10) : c.id);
        const selectedVod = selectedItems.filter(c => !c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('vod-', ''), 10) : c.id);

        const newTargetLive = Array.from(new Set([...targetPlaylist.mapped_live_groups, ...selectedLive]));
        const newTargetVod = Array.from(new Set([...targetPlaylist.mapped_vod_categories, ...selectedVod]));

        await API.updateCustomPlaylist(targetPlaylist.id, {
          live_groups: newTargetLive,
          vod_categories: newTargetVod,
        });

        // Remove from current playlist
        const newCurrentLive = currentPlaylist.mapped_live_groups.filter(id => !selectedLive.includes(id));
        const newCurrentVod = currentPlaylist.mapped_vod_categories.filter(id => !selectedVod.includes(id));

        await API.updateCustomPlaylist(currentPlaylist.id, {
          live_groups: newCurrentLive,
          vod_categories: newCurrentVod,
        });

        notifications.show({
          title: 'Success',
          message: `Moved category mappings to custom playlist '${targetPlaylist.name}'`,
          color: 'green',
        });
      } else if (type === 'live-tv') {
        await API.bulkMoveChannelGroups({
          source_ids: selectedIds,
          target_id: targetGroupId || null,
          target_name: targetGroupName || null,
        });
        notifications.show({
          title: 'Success',
          message: 'Successfully moved channels to target group',
          color: 'green',
        });
      } else if (type === 'movie' || type === 'series') {
        await API.bulkMoveVODCategories({
          source_ids: selectedIds,
          target_id: targetGroupId || null,
          target_name: targetGroupName || null,
        });
        notifications.show({
          title: 'Success',
          message: 'Successfully moved VOD items to target category',
          color: 'green',
        });
      }
      setSelectedIds([]);
      setActiveModal(null);
      onBulkAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Execute Copy
  const handleCopy = async () => {
    setLoading(true);
    try {
      if (type === 'playlist' && currentPlaylist) {
        // Copy category mappings from current playlist to another playlist
        if (!targetPlaylistId) return;
        const targetPlaylist = playlists.find((p) => String(p.id) === targetPlaylistId);
        if (!targetPlaylist) return;

        const selectedLive = selectedItems.filter(c => c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('live-', ''), 10) : c.id);
        const selectedVod = selectedItems.filter(c => !c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('vod-', ''), 10) : c.id);

        const newTargetLive = Array.from(new Set([...targetPlaylist.mapped_live_groups, ...selectedLive]));
        const newTargetVod = Array.from(new Set([...targetPlaylist.mapped_vod_categories, ...selectedVod]));

        await API.updateCustomPlaylist(targetPlaylist.id, {
          live_groups: newTargetLive,
          vod_categories: newTargetVod,
        });

        notifications.show({
          title: 'Success',
          message: `Copied category mappings to custom playlist '${targetPlaylist.name}'`,
          color: 'green',
        });
      } else if (type === 'live-tv') {
        await API.bulkCopyChannelGroups({
          source_ids: selectedIds,
          target_id: targetGroupId || null,
          target_name: targetGroupName || null,
        });
        notifications.show({
          title: 'Success',
          message: 'Successfully duplicated channels into target group',
          color: 'green',
        });
      }
      setSelectedIds([]);
      setActiveModal(null);
      onBulkAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Execute Regex Rename
  const handleRegexRename = async () => {
    setLoading(true);
    try {
      if (type === 'live-tv') {
        await API.bulkRenameChannelGroups({
          ids: selectedIds,
          find: findPat,
          replace: replacePat,
        });
      } else if (type === 'movie' || type === 'series') {
        await API.bulkRenameVODCategories({
          ids: selectedIds,
          find: findPat,
          replace: replacePat,
        });
      } else if (type === 'playlist') {
        const liveIds = selectedItems.filter(c => c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('live-', ''), 10) : c.id);
        const vodIds = selectedItems.filter(c => !c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('vod-', ''), 10) : c.id);

        if (liveIds.length > 0) {
          await API.bulkRenameChannelGroups({
            ids: liveIds,
            find: findPat,
            replace: replacePat,
          });
        }
        if (vodIds.length > 0) {
          await API.bulkRenameVODCategories({
            ids: vodIds,
            find: findPat,
            replace: replacePat,
          });
        }
      }
      notifications.show({
        title: 'Success',
        message: 'Successfully updated categories using regex',
        color: 'green',
      });
      setSelectedIds([]);
      setActiveModal(null);
      onBulkAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Execute Delete Categories
  const handleDelete = async () => {
    setLoading(true);
    try {
      if (type === 'playlist' && currentPlaylist) {
        // Remove category mappings from custom playlist
        const selectedLive = selectedItems.filter(c => c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('live-', ''), 10) : c.id);
        const selectedVod = selectedItems.filter(c => !c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('vod-', ''), 10) : c.id);

        const newLive = currentPlaylist.mapped_live_groups.filter(id => !selectedLive.includes(id));
        const newVod = currentPlaylist.mapped_vod_categories.filter(id => !selectedVod.includes(id));

        await API.updateCustomPlaylist(currentPlaylist.id, {
          live_groups: newLive,
          vod_categories: newVod,
        });

        notifications.show({
          title: 'Success',
          message: 'Removed category mappings from playlist',
          color: 'green',
        });
      } else {
        // Global deletion
        for (const id of selectedIds) {
          if (type === 'live-tv') {
            await API.deleteChannelGroup(id);
          } else if (type === 'movie' || type === 'series') {
            await API.deleteVODCategory(id);
          }
        }
        notifications.show({
          title: 'Success',
          message: `Successfully deleted selected categories`,
          color: 'green',
        });
      }
      setSelectedIds([]);
      setActiveModal(null);
      onBulkAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const openAssignModal = () => {
    setSelectedPlaylistIds([]);
    setActiveModal('assign');
  };

  const handleBulkAssign = async () => {
    setLoading(true);
    try {
      const selectedLive = selectedItems.filter(c => type === 'live-tv' || !!c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('live-', ''), 10) : c.id);
      const selectedVod = selectedItems.filter(c => type !== 'live-tv' && !c.isLiveGroup).map(c => typeof c.id === 'string' ? parseInt(c.id.replace('vod-', ''), 10) : c.id);

      for (const playlistId of selectedPlaylistIds) {
        const playlist = playlists.find((p) => String(p.id) === String(playlistId));
        if (!playlist) continue;

        const newLive = Array.from(new Set([...(playlist.mapped_live_groups || []), ...selectedLive]));
        const newVod = Array.from(new Set([...(playlist.mapped_vod_categories || []), ...selectedVod]));

        await API.updateCustomPlaylist(playlist.id, {
          live_groups: newLive,
          vod_categories: newVod,
        });
      }

      notifications.show({
        title: 'Success',
        message: `Assigned selected categories to ${selectedPlaylistIds.length} playlists`,
        color: 'green',
      });
      setSelectedIds([]);
      setActiveModal(null);
      onBulkAction();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePlaylistMapping = async (playlist, cat) => {
    const isLive = type === 'live-tv' || !!cat.isLiveGroup;
    const rawId = typeof cat.id === 'string'
      ? parseInt(cat.id.replace(isLive ? 'live-' : 'vod-', ''), 10)
      : cat.id;

    let newLive = [...(playlist.mapped_live_groups || [])];
    let newVod = [...(playlist.mapped_vod_categories || [])];

    const isMapped = isLive ? newLive.includes(rawId) : newVod.includes(rawId);

    if (isMapped) {
      if (isLive) {
        newLive = newLive.filter((id) => id !== rawId);
      } else {
        newVod = newVod.filter((id) => id !== rawId);
      }
    } else {
      if (isLive) {
        newLive.push(rawId);
      } else {
        newVod.push(rawId);
      }
    }

    try {
      await API.updateCustomPlaylist(playlist.id, {
        live_groups: newLive,
        vod_categories: newVod,
      });
      notifications.show({
        title: isMapped ? 'Mapping Removed' : 'Mapped Successfully',
        message: `${isMapped ? 'Removed' : 'Added'} '${cat.name}' ${isMapped ? 'from' : 'to'} playlist '${playlist.name}'`,
        color: 'green',
      });
      onBulkAction();
    } catch (e) {
      console.error(e);
    }
  };

  // Live Regex Preview calculation
  const regexPreviewList = useMemo(() => {
    if (!findPat) return [];
    try {
      const regex = new RegExp(findPat, 'g');
      return selectedItems.map((item) => {
        const newName = (item.name || '').replace(regex, replacePat);
        return {
          id: item.id,
          before: item.name,
          after: newName,
          changed: newName !== item.name,
        };
      });
    } catch (e) {
      return [];
    }
  }, [selectedItems, findPat, replacePat]);

  // Options for move/copy dropdowns
  const groupSelectOptions = useMemo(() => {
    return categories
      .filter((c) => !selectedIds.includes(c.id))
      .map((c) => ({ value: String(c.id), label: c.name }));
  }, [categories, selectedIds]);

  const playlistSelectOptions = useMemo(() => {
    return playlists
      .filter((p) => p.id !== currentPlaylist?.id)
      .map((p) => ({ value: String(p.id), label: p.name }));
  }, [playlists, currentPlaylist]);

  const getSidebarHeader = () => {
    switch (type) {
      case 'live-tv':
        return 'GROUPS';
      case 'movie':
      case 'series':
        return 'CATEGORIES';
      case 'playlist':
        return 'PLAYLIST MAPPINGS';
      default:
        return 'CATEGORIES';
    }
  };

  return (
    <Card
      w={280}
      p="md"
      h="100%"
      style={{
        backgroundColor: '#18181b',
        border: '1px solid #27272a',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        borderRadius: '8px',
      }}
    >
      <Group justify="space-between" mb="xs">
        <Text size="xs" weight={700} c="dimmed" style={{ letterSpacing: '0.5px' }}>
          {getSidebarHeader()} ({categories.length})
        </Text>
        {filteredCategories.length > 0 && (
          <Checkbox
            size="xs"
            checked={
              selectedIds.length > 0 &&
              selectedIds.length === filteredCategories.length
            }
            indeterminate={
              selectedIds.length > 0 &&
              selectedIds.length < filteredCategories.length
            }
            onChange={toggleSelectAll}
            label={
              <Text size="10px" c="dimmed" weight={500}>
                Select All
              </Text>
            }
          />
        )}
      </Group>

      <TextInput
        placeholder="Filter categories..."
        leftSection={<Search size={14} />}
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        size="xs"
        mb="sm"
        style={{
          input: {
            backgroundColor: '#09090b',
            border: '1px solid #27272a',
          },
        }}
      />

      <ScrollArea style={{ flex: 1 }} scrollbarSize={6}>
        <Stack spacing={4}>
          {filteredCategories.map((cat) => {
            const isSelected = selectedIds.includes(cat.id);
            const isActive = selectedId === cat.id;
            const count =
              cat.channel_count !== undefined
                ? cat.channel_count
                : type === 'series'
                  ? cat.series_count
                  : cat.movie_count !== undefined
                    ? cat.movie_count
                    : cat.count || 0;

            const categoryLabel = cat.isLiveGroup
              ? `${cat.name} (Live)`
              : cat.isLiveGroup === false
                ? `${cat.name} (VOD)`
                : cat.name;

            const isLive = type === 'live-tv' || !!cat.isLiveGroup;
            const rawId = typeof cat.id === 'string'
              ? parseInt(cat.id.replace(isLive ? 'live-' : 'vod-', ''), 10)
              : cat.id;

            const mappedPlaylists = isLive
              ? playlists.filter((p) => (p.mapped_live_groups || []).includes(rawId))
              : playlists.filter((p) => (p.mapped_vod_categories || []).includes(rawId));

            return (
              <Box
                key={cat.id}
                p="xs"
                style={{
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  backgroundColor: isActive
                    ? '#27272a'
                    : isSelected
                      ? '#1e1b4b'
                      : 'transparent',
                  border: isActive
                    ? '1px solid #3b82f6'
                    : '1px solid transparent',
                  transition: 'background-color 0.2s',
                  '&:hover': {
                    backgroundColor: '#27272a',
                  },
                }}
                onClick={() => onSelect(cat.id)}
              >
                <Checkbox
                  checked={isSelected}
                  onChange={(e) => {
                    e.stopPropagation();
                    toggleSelect(cat.id);
                  }}
                  size="xs"
                  mr="xs"
                />
                <Text
                  size="sm"
                  style={{
                    flex: 1,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                    color: isActive ? 'white' : '#d4d4d8',
                    fontWeight: isActive || isSelected ? 600 : 400,
                  }}
                >
                  {categoryLabel}
                </Text>

                {/* Playlist Mapping Indicator & Quick Mapping Popover */}
                {type !== 'playlist' && (
                  <Popover
                    opened={openedPopoverId === cat.id}
                    onClose={() => setOpenedPopoverId(null)}
                    position="right"
                    withArrow
                    shadow="md"
                    trapFocus
                  >
                    <Popover.Target>
                      <Tooltip
                        label={
                          mappedPlaylists.length > 0 ? (
                            <Stack spacing={2} p={2}>
                              <Text size="10px" weight={700}>MAPPED TO PLAYLISTS:</Text>
                              {mappedPlaylists.map(p => (
                                <Text key={p.id} size="10px" c="blue">{p.name}</Text>
                              ))}
                            </Stack>
                          ) : (
                            "Map to Playlists"
                          )
                        }
                        position="top"
                        withArrow
                      >
                        <ActionIcon
                          size="xs"
                          variant="subtle"
                          color={mappedPlaylists.length > 0 ? "blue" : "gray"}
                          mr={4}
                          onClick={(e) => {
                            e.stopPropagation();
                            setOpenedPopoverId(openedPopoverId === cat.id ? null : cat.id);
                          }}
                        >
                          <Link size={12} />
                        </ActionIcon>
                      </Tooltip>
                    </Popover.Target>
                    <Popover.Dropdown onClick={(e) => e.stopPropagation()}>
                      <Text size="xs" weight={700} mb="xs" c="dimmed">
                        MAP TO PLAYLISTS
                      </Text>
                      {playlists.length > 0 ? (
                        <Stack spacing="xs">
                          {playlists.map((playlist) => {
                            const isChecked = isLive
                              ? (playlist.mapped_live_groups || []).includes(rawId)
                              : (playlist.mapped_vod_categories || []).includes(rawId);

                            return (
                              <Checkbox
                                key={playlist.id}
                                label={playlist.name}
                                checked={isChecked}
                                onChange={() => handleTogglePlaylistMapping(playlist, cat)}
                                size="xs"
                              />
                            );
                          })}
                        </Stack>
                      ) : (
                        <Text size="10px" c="dimmed">No playlists configured.</Text>
                      )}
                    </Popover.Dropdown>
                  </Popover>
                )}

                <Badge
                  color={isActive ? 'blue' : 'gray'}
                  variant="light"
                  size="xs"
                  ml="xs"
                >
                  {count}
                </Badge>
              </Box>
            );
          })}
          {filteredCategories.length === 0 && (
            <Text size="xs" c="dimmed" align="center" mt="xl">
              No categories found.
            </Text>
          )}
        </Stack>
      </ScrollArea>

      {/* Floating Bulk Action Bar when categories are checked */}
      {selectedIds.length > 0 && (
        <Card
          p="xs"
          mt="xs"
          style={{
            backgroundColor: '#09090b',
            border: '1px solid #3b82f6',
            borderRadius: '6px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
          }}
        >
          <Group justify="space-between" align="center">
            <Text size="xs" weight={600} c="blue">
              {selectedIds.length} Selected
            </Text>
            <Group gap={4}>
              {type !== 'playlist' && (
                <Tooltip label="Rename">
                  <ActionIcon
                    variant="subtle"
                    color="blue"
                    size="sm"
                    onClick={openRenameModal}
                  >
                    <Edit size={14} />
                  </ActionIcon>
                </Tooltip>
              )}

              <Tooltip label={type === 'playlist' ? 'Move to Playlist' : 'Move Items'}>
                <ActionIcon
                  variant="subtle"
                  color="violet"
                  size="sm"
                  onClick={openMoveModal}
                >
                  <Move size={14} />
                </ActionIcon>
              </Tooltip>

              {(type === 'live-tv' || type === 'playlist') && (
                <Tooltip label={type === 'playlist' ? 'Copy to Playlist' : 'Copy Items'}>
                  <ActionIcon
                    variant="subtle"
                    color="teal"
                    size="sm"
                    onClick={openCopyModal}
                  >
                    <Copy size={14} />
                  </ActionIcon>
                </Tooltip>
              )}

              <Tooltip label="Regex Edit">
                <ActionIcon
                  variant="subtle"
                  color="cyan"
                  size="sm"
                  onClick={openRegexModal}
                >
                  <FileEdit size={14} />
                </ActionIcon>
              </Tooltip>

              {type !== 'playlist' && (
                <Tooltip label="Assign to Playlists">
                  <ActionIcon
                    variant="subtle"
                    color="blue"
                    size="sm"
                    onClick={openAssignModal}
                  >
                    <ListPlus size={14} />
                  </ActionIcon>
                </Tooltip>
              )}

              <Tooltip label={type === 'playlist' ? 'Remove Mapping' : 'Delete Categories'}>
                <ActionIcon
                  variant="subtle"
                  color="red"
                  size="sm"
                  onClick={openDeleteModal}
                >
                  <Trash2 size={14} />
                </ActionIcon>
              </Tooltip>
            </Group>
          </Group>
        </Card>
      )}

      {/* RENAME MODAL */}
      <Modal
        opened={activeModal === 'rename'}
        onClose={() => setActiveModal(null)}
        title="Rename Category"
        size="md"
        centered
      >
        <Stack spacing="md">
          {selectedItems.map((item) => (
            <TextInput
              key={item.id}
              label={`Original: ${item.name}`}
              value={renameMappings[item.id] || ''}
              onChange={(e) =>
                setRenameMappings({
                  ...renameMappings,
                  [item.id]: e.target.value,
                })
              }
              size="sm"
            />
          ))}
          <Group justify="right" mt="md">
            <Button variant="outline" color="gray" onClick={() => setActiveModal(null)}>
              Cancel
            </Button>
            <Button color="blue" onClick={handleRename} loading={loading}>
              Save Changes
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* MOVE MODAL */}
      <Modal
        opened={activeModal === 'move'}
        onClose={() => setActiveModal(null)}
        title={type === 'playlist' ? 'Move Mappings to Playlist' : 'Move Items to Category'}
        size="sm"
        centered
      >
        <Stack spacing="md">
          {type === 'playlist' ? (
            <>
              <Text size="sm" c="dimmed">
                Move the selected category mappings from this playlist to another custom playlist.
              </Text>
              <Select
                label="Target Custom Playlist"
                placeholder="Choose playlist..."
                data={playlistSelectOptions}
                value={targetPlaylistId}
                onChange={setTargetPlaylistId}
                required
              />
            </>
          ) : (
            <>
              <Text size="sm" c="dimmed">
                Move all channels/VOD items from selected categories to a target category. Source categories will be deleted if they become empty.
              </Text>
              <Select
                label="Select Existing Category"
                placeholder="Choose category..."
                data={groupSelectOptions}
                value={targetGroupId}
                onChange={(val) => {
                  setTargetGroupId(val);
                  setTargetGroupName('');
                }}
                clearable
              />
              <Text size="xs" align="center" c="dimmed">
                — OR CREATE NEW —
              </Text>
              <TextInput
                label="New Category Name"
                placeholder="e.g. My New Category"
                value={targetGroupName}
                onChange={(e) => {
                  setTargetGroupName(e.target.value);
                  setTargetGroupId('');
                }}
              />
            </>
          )}

          <Group justify="right" mt="md">
            <Button variant="outline" color="gray" onClick={() => setActiveModal(null)}>
              Cancel
            </Button>
            <Button
              color="blue"
              onClick={handleMove}
              loading={loading}
              disabled={
                type === 'playlist'
                  ? !targetPlaylistId
                  : !targetGroupId && !targetGroupName.trim()
              }
            >
              Move Content
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* COPY MODAL */}
      <Modal
        opened={activeModal === 'copy'}
        onClose={() => setActiveModal(null)}
        title={type === 'playlist' ? 'Copy Mappings to Playlist' : 'Duplicate Channels into Category'}
        size="sm"
        centered
      >
        <Stack spacing="md">
          {type === 'playlist' ? (
            <>
              <Text size="sm" c="dimmed">
                Copy the selected category mappings to another custom playlist.
              </Text>
              <Select
                label="Target Custom Playlist"
                placeholder="Choose playlist..."
                data={playlistSelectOptions}
                value={targetPlaylistId}
                onChange={setTargetPlaylistId}
                required
              />
            </>
          ) : (
            <>
              <Text size="sm" c="dimmed">
                Duplicate all channels inside selected categories into a target category. This creates new channels pointing to the same streams.
              </Text>
              <Select
                label="Select Existing Category"
                placeholder="Choose category..."
                data={groupSelectOptions}
                value={targetGroupId}
                onChange={(val) => {
                  setTargetGroupId(val);
                  setTargetGroupName('');
                }}
                clearable
              />
              <Text size="xs" align="center" c="dimmed">
                — OR CREATE NEW —
              </Text>
              <TextInput
                label="New Category Name"
                placeholder="e.g. My New Category"
                value={targetGroupName}
                onChange={(e) => {
                  setTargetGroupName(e.target.value);
                  setTargetGroupId('');
                }}
              />
            </>
          )}

          <Group justify="right" mt="md">
            <Button variant="outline" color="gray" onClick={() => setActiveModal(null)}>
              Cancel
            </Button>
            <Button
              color="blue"
              onClick={handleCopy}
              loading={loading}
              disabled={
                type === 'playlist'
                  ? !targetPlaylistId
                  : !targetGroupId && !targetGroupName.trim()
              }
            >
              Copy Content
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* REGEX RENAME MODAL */}
      <Modal
        opened={activeModal === 'regex'}
        onClose={() => setActiveModal(null)}
        title="Regex Category Rename"
        size="md"
        centered
      >
        <Stack spacing="md">
          <TextInput
            label="Find Pattern (Regex)"
            placeholder="e.g. ^DE:\s*"
            value={findPat}
            onChange={(e) => setFindPat(e.target.value)}
            required
          />
          <TextInput
            label="Replace With"
            placeholder="e.g. empty, or custom text"
            value={replacePat}
            onChange={(e) => setReplacePat(e.target.value)}
          />

          {findPat && (
            <Box mt="xs">
              <Text size="xs" weight={600} mb="xs" c="dimmed">
                LIVE PREVIEW:
              </Text>
              <ScrollArea h={180} p="xs" style={{ border: '1px solid #27272a', borderRadius: '4px', backgroundColor: '#09090b' }}>
                <Stack spacing={4}>
                  {regexPreviewList.map((preview) => (
                    <Group key={preview.id} wrap="nowrap" justify="space-between" size="xs">
                      <Text size="xs" c="dimmed" style={{ flex: 1, textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                        {preview.before}
                      </Text>
                      <Text size="xs" c="blue" mx="xs">
                        →
                      </Text>
                      <Text
                        size="xs"
                        c={preview.changed ? 'green' : 'dimmed'}
                        weight={preview.changed ? 600 : 400}
                        style={{ flex: 1, textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}
                      >
                        {preview.after || '‹empty›'}
                      </Text>
                    </Group>
                  ))}
                </Stack>
              </ScrollArea>
            </Box>
          )}

          <Group justify="right" mt="md">
            <Button variant="outline" color="gray" onClick={() => setActiveModal(null)}>
              Cancel
            </Button>
            <Button color="blue" onClick={handleRegexRename} loading={loading} disabled={!findPat}>
              Apply Regex
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* DELETE MODAL */}
      <Modal
        opened={activeModal === 'delete'}
        onClose={() => setActiveModal(null)}
        title={type === 'playlist' ? 'Remove Mappings' : 'Delete Categories'}
        size="sm"
        centered
      >
        <Stack spacing="md">
          <Text size="sm">
            {type === 'playlist'
              ? `Are you sure you want to remove these ${selectedIds.length} category mappings from this playlist? This does not delete any global categories or content.`
              : `Are you sure you want to delete these ${selectedIds.length} categories? All channels/VOD items belonging to them will be unassigned (moved to Uncategorized/Default Group).`}
          </Text>
          <Group justify="right" mt="md">
            <Button variant="outline" color="gray" onClick={() => setActiveModal(null)}>
              Cancel
            </Button>
            <Button color="red" onClick={handleDelete} loading={loading}>
              Confirm Delete
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* ASSIGN TO PLAYLIST MODAL */}
      <Modal
        opened={activeModal === 'assign'}
        onClose={() => setActiveModal(null)}
        title="Assign Selected Categories to Playlists"
        size="sm"
        centered
      >
        <Stack spacing="md">
          <Text size="sm" c="dimmed">
            Select the custom playlists you want to assign these {selectedIds.length} categories to:
          </Text>
          {playlists.length > 0 ? (
            <Stack spacing="xs">
              {playlists.map((p) => (
                <Checkbox
                  key={p.id}
                  label={p.name}
                  checked={selectedPlaylistIds.includes(p.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedPlaylistIds([...selectedPlaylistIds, p.id]);
                    } else {
                      setSelectedPlaylistIds(selectedPlaylistIds.filter(id => id !== p.id));
                    }
                  }}
                  size="xs"
                />
              ))}
            </Stack>
          ) : (
            <Text size="xs" c="dimmed" fs="italic">No custom playlists configured.</Text>
          )}
          <Group justify="right" mt="md">
            <Button variant="outline" color="gray" onClick={() => setActiveModal(null)}>
              Cancel
            </Button>
            <Button
              color="blue"
              onClick={handleBulkAssign}
              loading={loading}
              disabled={selectedPlaylistIds.length === 0}
            >
              Assign Categories
            </Button>
          </Group>
        </Stack>
      </Modal>
    </Card>
  );
};

export default CategorySidebar;
