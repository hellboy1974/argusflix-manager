import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Box, Button, Text, Group, ActionIcon, Stack, TextInput, Select, Collapse } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { GripVertical, Eye, EyeOff, Edit2, Check, X } from 'lucide-react';
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
import {
  NAV_ITEMS,
  DEFAULT_ADMIN_ORDER,
  DEFAULT_USER_ORDER,
  getOrderedNavItems,
} from '../../../config/navigation';
import { USER_LEVELS } from '../../../constants';
import { IconRegistry } from '../../../config/icons';

const ICON_OPTIONS = Object.keys(IconRegistry).map(key => ({
  value: key,
  label: key,
}));

const DraggableNavItem = ({ 
  item, 
  isHidden, 
  canHide, 
  onToggleVisibility, 
  onUpdateItem 
}) => {
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

  const [isEditing, setIsEditing] = useState(false);
  const [editLabel, setEditLabel] = useState(item.label);
  const [editIcon, setEditIcon] = useState('');

  // Find the string name of the current icon component
  useEffect(() => {
    let currentIconName = '';
    for (const [name, comp] of Object.entries(IconRegistry)) {
      if (item.icon === comp) {
        currentIconName = name;
        break;
      }
    }
    setEditIcon(currentIconName);
  }, [item.icon, isEditing]);

  const style = {
    transform: CSS.Transform.toString(transform),
    transition: transition,
    opacity: isDragging ? 0.8 : isHidden ? 0.5 : 1,
    zIndex: isDragging ? 1 : 0,
    position: 'relative',
  };

  const IconComponent = item.icon;

  const handleSave = () => {
    onUpdateItem(item.id, editLabel, editIcon);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditLabel(item.label);
  };

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
      <Group justify="space-between" wrap="nowrap">
        <Group gap="sm" style={{ flexGrow: 1 }}>
          <ActionIcon
            {...attributes}
            {...listeners}
            variant="transparent"
            size="sm"
            style={{ cursor: 'grab' }}
          >
            <GripVertical size={16} color="#888" />
          </ActionIcon>
          
          {IconComponent && (
            <IconComponent size={18} color={isHidden ? '#666' : '#ccc'} />
          )}
          
          <Text size="sm" c={isHidden ? 'dimmed' : 'gray.3'} style={{ flexGrow: 1 }}>
            {item.label}
          </Text>
        </Group>

        <Group gap="xs" wrap="nowrap">
          <ActionIcon
            variant="transparent"
            size="sm"
            onClick={() => setIsEditing(!isEditing)}
            title="Edit Item"
          >
            <Edit2 size={16} color={isEditing ? '#4dabf7' : '#888'} />
          </ActionIcon>
          {canHide && (
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

      <Collapse in={isEditing}>
        <Box pt="sm" pb="xs">
          <Group align="flex-end" wrap="nowrap">
            <TextInput
              label="Label"
              size="xs"
              value={editLabel}
              onChange={(e) => setEditLabel(e.currentTarget.value)}
              style={{ flexGrow: 1 }}
            />
            <Select
              label="Icon"
              size="xs"
              data={ICON_OPTIONS}
              value={editIcon}
              onChange={setEditIcon}
              searchable
              style={{ width: '150px' }}
            />
            <ActionIcon color="green" variant="light" onClick={handleSave} title="Save" size="md">
              <Check size={16} />
            </ActionIcon>
            <ActionIcon color="red" variant="light" onClick={handleCancel} title="Cancel" size="md">
              <X size={16} />
            </ActionIcon>
          </Group>
        </Box>
      </Collapse>
    </Box>
  );
};

const NavOrderForm = ({ active }) => {
  const user = useAuthStore((s) => s.user);
  const getNavOrder = useAuthStore((s) => s.getNavOrder);
  const setNavOrder = useAuthStore((s) => s.setNavOrder);
  const getHiddenNav = useAuthStore((s) => s.getHiddenNav);
  const toggleNavVisibility = useAuthStore((s) => s.toggleNavVisibility);
  const updateUserPreferences = useAuthStore((s) => s.updateUserPreferences);

  const isAdmin = user?.user_level >= USER_LEVELS.ADMIN;
  const canEdit = isAdmin || user?.custom_properties?.can_edit_navigation === true;
  const defaultOrder = isAdmin ? DEFAULT_ADMIN_ORDER : DEFAULT_USER_ORDER;

  const [items, setItems] = useState([]);
  const [isSaving, setIsSaving] = useState(false);

  // Refs for debouncing
  const saveTimeoutRef = useRef(null);
  const pendingOrderRef = useRef(null);

  const sensors = useSensors(
    useSensor(MouseSensor, {}),
    useSensor(TouchSensor, {}),
    useSensor(KeyboardSensor, {})
  );

  useEffect(() => {
    if (active && canEdit) {
      const savedOrder = getNavOrder();
      const customProps = user?.custom_properties || {};
      const orderedItems = getOrderedNavItems(savedOrder, isAdmin, [], customProps);
      setItems(orderedItems);
    }
  }, [active, canEdit, isAdmin, getNavOrder, user?.custom_properties]);

  useEffect(() => {
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, []);

  const debouncedSave = useCallback(
    async (newOrder) => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }

      pendingOrderRef.current = newOrder;

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
          const savedOrder = getNavOrder();
          const customProps = user?.custom_properties || {};
          const orderedItems = getOrderedNavItems(savedOrder, isAdmin, [], customProps);
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
    [setNavOrder, getNavOrder, isAdmin, user]
  );

  const handleDragEnd = ({ active, over }) => {
    if (!over || active.id === over.id) return;

    const oldIndex = items.findIndex((item) => item.id === active.id);
    const newIndex = items.findIndex((item) => item.id === over.id);
    const newItems = arrayMove(items, oldIndex, newIndex);

    setItems(newItems);

    const newOrder = newItems.map((item) => item.id);
    debouncedSave(newOrder);
  };

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

  const handleUpdateItem = async (itemId, newLabel, newIcon) => {
    setIsSaving(true);
    try {
      const currentLabels = user?.custom_properties?.navLabels || {};
      const currentIcons = user?.custom_properties?.navIcons || {};

      const newLabels = { ...currentLabels };
      if (newLabel && newLabel !== NAV_ITEMS[itemId]?.label) {
        newLabels[itemId] = newLabel;
      } else {
        delete newLabels[itemId];
      }

      const newIconsObj = { ...currentIcons };
      if (newIcon) {
        newIconsObj[itemId] = newIcon;
      } else {
        delete newIconsObj[itemId];
      }

      await updateUserPreferences({
        navLabels: newLabels,
        navIcons: newIconsObj,
      });

      notifications.show({
        title: 'Navigation',
        message: 'Item updated successfully',
        color: 'green',
        autoClose: 2000,
      });
    } catch {
      notifications.show({
        title: 'Error',
        message: 'Failed to update navigation item',
        color: 'red',
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = async () => {
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
      const orderedItems = getOrderedNavItems(defaultOrder, isAdmin, [], {});
      setItems(orderedItems);
      notifications.show({
        title: 'Navigation',
        message: 'Reset to default order and labels',
        color: 'blue',
        autoClose: 2000,
      });
    } catch {
      notifications.show({
        title: 'Error',
        message: 'Failed to reset navigation order',
        color: 'red',
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (!active) {
    return null;
  }

  if (!canEdit) {
    return (
      <Box p="md">
        <Text c="dimmed">You do not have permission to edit the navigation sidebar.</Text>
      </Box>
    );
  }

  const hiddenNav = getHiddenNav();

  return (
    <Stack gap="md">
      <Text size="sm" c="dimmed">
        Drag and drop to reorder the sidebar navigation items. Click the edit icon to customize labels and icons.
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
              onUpdateItem={handleUpdateItem}
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
    </Stack>
  );
};

export default NavOrderForm;
