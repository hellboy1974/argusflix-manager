import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Box, Button, Text, Group, ActionIcon, Stack, Modal, TextInput, Select, Alert } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { GripVertical, Eye, EyeOff } from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import {
  closestCenter,
  DndContext,
  KeyboardSensor,
  MouseSensor,
  TouchSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';
import useAuthStore from '../../../store/auth';
import { usePluginStore } from '../../../store/plugins.jsx';
import {
  NAV_ITEMS,
  DEFAULT_ADMIN_ORDER,
  DEFAULT_USER_ORDER,
  getOrderedNavItems,
} from '../../../config/navigation';
import { USER_LEVELS } from '../../../constants';

const AVAILABLE_ICONS = [
  { value: 'ListOrdered', label: 'List Ordered' },
  { value: 'Play', label: 'Play' },
  { value: 'Database', label: 'Database' },
  { value: 'LayoutGrid', label: 'Layout Grid' },
  { value: 'ChartLine', label: 'Chart Line' },
  { value: 'Video', label: 'Video' },
  { value: 'PlugZap', label: 'Plug Zap' },
  { value: 'Package', label: 'Package' },
  { value: 'Download', label: 'Download' },
  { value: 'User', label: 'User' },
  { value: 'FileImage', label: 'File Image' },
  { value: 'Webhook', label: 'Webhook' },
  { value: 'Logs', label: 'Logs' },
  { value: 'Blocks', label: 'Blocks' },
  { value: 'MonitorCog', label: 'Monitor Cog' },
  { value: 'Terminal', label: 'Terminal' },
  { value: 'Settings', label: 'Settings' },
  { value: 'Wrench', label: 'Wrench' },
  { value: 'Tv', label: 'TV' },
  { value: 'Clapperboard', label: 'Clapperboard' },
  { value: 'Shield', label: 'Shield' },
  { value: 'Key', label: 'Key' },
  { value: 'Eye', label: 'Eye' },
  { value: 'Activity', label: 'Activity' },
  { value: 'Folder', label: 'Folder' },
];

const DraggableNavItem = ({ item, isHidden, canHide, onToggleVisibility, onEditClick, canEdit }) => {
  const {
    transform,
    transition,
    setNodeRef,
    isDragging,
    attributes,
    listeners,
  } = useSortable({
    id: item.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition: transition,
    opacity: isDragging ? 0.8 : isHidden ? 0.5 : 1,
    zIndex: isDragging ? 1 : 0,
    position: 'relative',
  };

  const IconComponent = item.icon;

  return (
    <Box
      ref={setNodeRef}
      style={{
        ...style,
        padding: '10px 12px',
        border: '1px solid #444',
        borderRadius: '6px',
        backgroundColor: isDragging ? '#3A3A3E' : '#2A2A2E',
        marginBottom: 6,
      }}
    >
      <Group justify="space-between">
        <Group gap="sm">
          {canEdit && (
            <ActionIcon
              {...attributes}
              {...listeners}
              variant="transparent"
              size="sm"
              style={{ cursor: 'grab' }}
            >
              <GripVertical size={16} color="#888" />
            </ActionIcon>
          )}
          {IconComponent && (
            <IconComponent size={18} color={isHidden ? '#666' : '#ccc'} />
          )}
          <Text size="sm" c={isHidden ? 'dimmed' : 'gray.3'}>
            {item.label}
          </Text>
        </Group>
        <Group gap="xs">
          {canEdit && (
            <ActionIcon
              variant="transparent"
              size="sm"
              onClick={() => onEditClick(item)}
              title="Edit label and icon"
            >
              <LucideIcons.Edit2 size={16} color="#888" />
            </ActionIcon>
          )}
          {canHide && canEdit && (
            <ActionIcon
              variant="transparent"
              size="sm"
              onClick={() => onToggleVisibility(item.id)}
              title={isHidden ? 'Show in navigation' : 'Hide from navigation'}
            >
              {isHidden ? (
                <EyeOff size={16} color="#666" />
              ) : (
                <Eye size={16} color="#888" />
              )}
            </ActionIcon>
          )}
        </Group>
      </Group>
    </Box>
  );
};

const NavOrderForm = ({ active }) => {
  // All store selectors grouped together
  const user = useAuthStore((s) => s.user);
  const getNavOrder = useAuthStore((s) => s.getNavOrder);
  const setNavOrder = useAuthStore((s) => s.setNavOrder);
  const getHiddenNav = useAuthStore((s) => s.getHiddenNav);
  const toggleNavVisibility = useAuthStore((s) => s.toggleNavVisibility);
  const updateUserPreferences = useAuthStore((s) => s.updateUserPreferences);
  const updateNavLabel = useAuthStore((s) => s.updateNavLabel);
  const updateNavIcon = useAuthStore((s) => s.updateNavIcon);

  const plugins = usePluginStore((s) => s.plugins);

  const isAdmin = user?.user_level >= USER_LEVELS.ADMIN;
  const canEditNavigation = isAdmin || user?.custom_properties?.can_edit_navigation === true;
  const defaultOrder = isAdmin ? DEFAULT_ADMIN_ORDER : DEFAULT_USER_ORDER;

  const [items, setItems] = useState([]);
  const [isSaving, setIsSaving] = useState(false);

  // Editing modal state
  const [editingItem, setEditingItem] = useState(null);
  const [editLabel, setEditLabel] = useState('');
  const [editIcon, setEditIcon] = useState('');

  // Refs for debouncing
  const saveTimeoutRef = useRef(null);
  const pendingOrderRef = useRef(null);

  const sensors = useSensors(
    useSensor(MouseSensor, {}),
    useSensor(TouchSensor, {}),
    useSensor(KeyboardSensor, {})
  );

  useEffect(() => {
    if (active) {
      const savedOrder = getNavOrder();
      
      // Compute active dynamic UI plugins
      const activeUiPlugins = plugins
        .filter((p) => p.enabled && p.has_ui)
        .map((p) => {
          const iconName = p.icon || 'PlugZap';
          const IconComponent = LucideIcons[iconName] || LucideIcons.PlugZap;
          return {
            id: `plugin-${p.key}`,
            label: p.name,
            icon: IconComponent,
            path: `/toolbox/${p.key}`,
            adminOnly: p.admin_only !== false,
          };
        });

      const orderedItems = getOrderedNavItems(savedOrder, isAdmin, [], activeUiPlugins);
      
      // Apply customized labels and icons from user custom_properties
      const customLabels = user?.custom_properties?.navLabels || {};
      const customIcons = user?.custom_properties?.navIcons || {};

      const mappedItems = orderedItems.map((item) => {
        const mappedItem = { ...item };
        if (customLabels[item.id]) {
          mappedItem.label = customLabels[item.id];
        }
        if (customIcons[item.id]) {
          const iconName = customIcons[item.id];
          mappedItem.icon = LucideIcons[iconName] || item.icon;
        }
        return mappedItem;
      });

      setItems(mappedItems);
    }
  }, [active, isAdmin, getNavOrder, plugins, user]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, []);

  // Debounced save function
  const debouncedSave = useCallback(
    async (newOrder) => {
      // Clear any pending save
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }

      // Store the pending order
      pendingOrderRef.current = newOrder;

      // Schedule save after 800ms of inactivity
      saveTimeoutRef.current = setTimeout(async () => {
        const orderToSave = pendingOrderRef.current;
        if (!orderToSave) return;

        setIsSaving(true);
        try {
          await setNavOrder(orderToSave);
          notifications.show({
            title: 'Navigation',
            message: 'Order saved successfully',
            color: 'green',
            autoClose: 2000,
          });
        } catch {
          // Revert on failure
          const savedOrder = getNavOrder();
          const orderedItems = getOrderedNavItems(savedOrder, isAdmin);
          setItems(orderedItems);
          notifications.show({
            title: 'Error',
            message: 'Failed to save navigation order',
            color: 'red',
          });
        } finally {
          setIsSaving(false);
          pendingOrderRef.current = null;
        }
      }, 800);
    },
    [setNavOrder, getNavOrder, isAdmin]
  );

  const handleDragEnd = ({ active, over }) => {
    if (!over || active.id === over.id) return;

    const oldIndex = items.findIndex((item) => item.id === active.id);
    const newIndex = items.findIndex((item) => item.id === over.id);
    const newItems = arrayMove(items, oldIndex, newIndex);

    // Optimistic update
    setItems(newItems);

    // Debounced save to backend
    const newOrder = newItems.map((item) => item.id);
    debouncedSave(newOrder);
  };

  // Wrapped visibility toggle with error handling
  const handleToggleVisibility = useCallback(
    async (itemId) => {
      try {
        await toggleNavVisibility(itemId);
        notifications.show({
          title: 'Navigation',
          message: 'Visibility updated',
          color: 'green',
          autoClose: 2000,
        });
      } catch {
        notifications.show({
          title: 'Error',
          message: 'Failed to update visibility',
          color: 'red',
        });
      }
    },
    [toggleNavVisibility]
  );

  const handleEditClick = (item) => {
    setEditingItem(item);
    
    // Find customized or default label
    const customLabels = user?.custom_properties?.navLabels || {};
    setEditLabel(customLabels[item.id] || item.label);

    // Find customized or default icon name
    let defaultIconName = 'Terminal';
    const defaultNav = NAV_ITEMS[item.id];
    if (defaultNav) {
      const found = Object.keys(LucideIcons).find(key => LucideIcons[key] === defaultNav.icon);
      if (found) defaultIconName = found;
    } else {
      const pluginKey = item.id.replace('plugin-', '');
      const plug = plugins.find(p => p.key === pluginKey);
      if (plug) {
        defaultIconName = plug.icon || 'PlugZap';
      }
    }
    const customIcons = user?.custom_properties?.navIcons || {};
    setEditIcon(customIcons[item.id] || defaultIconName);
  };

  const handleSaveDetails = async () => {
    if (!editingItem) return;
    setIsSaving(true);
    try {
      await updateNavLabel(editingItem.id, editLabel);
      await updateNavIcon(editingItem.id, editIcon);
      
      // Update local state items
      setItems((prev) =>
        prev.map((item) => {
          if (item.id === editingItem.id) {
            return {
              ...item,
              label: editLabel,
              icon: LucideIcons[editIcon] || item.icon,
            };
          }
          return item;
        })
      );

      notifications.show({
        title: 'Navigation',
        message: 'Details updated successfully',
        color: 'green',
        autoClose: 2000,
      });
      setEditingItem(null);
    } catch {
      notifications.show({
        title: 'Error',
        message: 'Failed to save details',
        color: 'red',
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = async () => {
    // Cancel any pending debounced save
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
      pendingOrderRef.current = null;
    }

    setIsSaving(true);
    try {
      await updateUserPreferences({
        navOrder: defaultOrder,
        hiddenNav: [],
        navLabels: {},
        navIcons: {},
      });
      
      // Re-read and map
      const activeUiPlugins = plugins
        .filter((p) => p.enabled && p.has_ui)
        .map((p) => {
          const iconName = p.icon || 'PlugZap';
          const IconComponent = LucideIcons[iconName] || LucideIcons.PlugZap;
          return {
            id: `plugin-${p.key}`,
            label: p.name,
            icon: IconComponent,
            path: `/toolbox/${p.key}`,
            adminOnly: p.admin_only !== false,
          };
        });
        
      const orderedItems = getOrderedNavItems(defaultOrder, isAdmin, [], activeUiPlugins);
      setItems(orderedItems);
      
      notifications.show({
        title: 'Navigation',
        message: 'Reset to default order and settings',
        color: 'blue',
        autoClose: 2000,
      });
    } catch {
      notifications.show({
        title: 'Error',
        message: 'Failed to reset navigation settings',
        color: 'red',
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (!active) {
    return null;
  }

  // Cache hiddenNav before render loop to avoid calling getter N times
  const hiddenNav = getHiddenNav();

  return (
    <Stack gap="md">
      {!canEditNavigation && (
        <Alert color="blue" title="Info">
          Sie haben keine Berechtigung, die Menüeinträge anzupassen. Bitte wenden Sie sich an einen Administrator.
        </Alert>
      )}

      {canEditNavigation && (
        <>
          <Text size="sm" c="dimmed">
            Drag and drop to reorder the sidebar navigation items. Click the edit icon to rename items or change their icon.
          </Text>

          <DndContext
            collisionDetection={closestCenter}
            modifiers={[restrictToVerticalAxis]}
            onDragEnd={handleDragEnd}
            sensors={sensors}
          >
            <SortableContext
              items={items.map((item) => item.id)}
              strategy={verticalListSortingStrategy}
            >
              {items.map((item) => (
                <DraggableNavItem
                  key={item.id}
                  item={item}
                  isHidden={hiddenNav.includes(item.id)}
                  canHide={item.canHide !== false}
                  onToggleVisibility={handleToggleVisibility}
                  onEditClick={handleEditClick}
                  canEdit={canEditNavigation}
                />
              ))}
            </SortableContext>
          </DndContext>

          <Group justify="flex-end">
            <Button
              variant="subtle"
              color="gray"
              onClick={handleReset}
              disabled={isSaving}
            >
              Reset to Default
            </Button>
          </Group>
        </>
      )}

      <Modal
        opened={!!editingItem}
        onClose={() => setEditingItem(null)}
        title={`Edit Menu Item: ${editingItem?.label || ''}`}
        size="md"
      >
        <Stack gap="md">
          <TextInput
            label="Menu Label"
            value={editLabel}
            onChange={(e) => setEditLabel(e.currentTarget.value)}
            required
          />
          <Select
            label="Menu Icon"
            data={AVAILABLE_ICONS}
            value={editIcon}
            onChange={setEditIcon}
            searchable
            required
          />
          <Group justify="flex-end" mt="md">
            <Button variant="outline" color="gray" onClick={() => setEditingItem(null)}>
              Cancel
            </Button>
            <Button onClick={handleSaveDetails} loading={isSaving}>
              Save Changes
            </Button>
          </Group>
        </Stack>
      </Modal>
    </Stack>
  );
};

export default NavOrderForm;
