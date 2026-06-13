import React, { useState, useEffect } from 'react';
import { Box, Title, Text, Select, Button, Paper, Group, Divider, ActionIcon, Modal, TextInput, Stack } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Trash, Settings as SettingsIcon, GripVertical } from 'lucide-react';
import { notifications } from '@mantine/notifications';
import ErrorBoundary from '../components/ErrorBoundary';
import API from '../api';

const WIDGET_TYPES = [
  { value: 'hero', label: 'Hero Banner' },
  { value: 'continue_watching', label: 'Continue Watching' },
  { value: 'category_row', label: 'Category Row' },
  { value: 'trending', label: 'Trending / Popular' },
  { value: 'recent_live_tv', label: 'Recent Live TV' },
  { value: 'recently_added', label: 'Recently Added (Per Server)' },
  { value: 'now_playing', label: 'Now Playing / EPG Live' },
  { value: 'favorites', label: 'Favorites' },
  { value: 'custom_banner', label: 'Custom Banner / Announcement' },
];

function SortableItem({ id, widget, onRemove, onConfigure }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const widgetConfig = WIDGET_TYPES.find(w => w.value === widget.widget_type);

  return (
    <Paper ref={setNodeRef} style={style} withBorder p="md" mb="sm" shadow="sm">
      <Group justify="space-between">
        <Group>
          <div {...attributes} {...listeners} style={{ cursor: 'grab' }}>
            <GripVertical size={20} color="gray" />
          </div>
          <Text fw={500}>{widgetConfig?.label || widget.widget_type}</Text>
        </Group>
        <Group gap="xs">
          <ActionIcon variant="light" color="blue" onClick={() => onConfigure(widget)} title="Configure Widget">
            <SettingsIcon size={16} />
          </ActionIcon>
          <ActionIcon variant="light" color="red" onClick={() => onRemove(id)} title="Remove Widget">
            <Trash size={16} />
          </ActionIcon>
        </Group>
      </Group>
    </Paper>
  );
}

const PageContent = () => {
  const [widgets, setWidgets] = useState([]);
  const [profiles, setProfiles] = useState([]);
  const [pages, setPages] = useState([]);
  const [selectedProfileId, setSelectedProfileId] = useState('');
  const [selectedPageId, setSelectedPageId] = useState('');
  
  const [configModalOpened, { open: openConfigModal, close: closeConfigModal }] = useDisclosure(false);
  const [configuringWidget, setConfiguringWidget] = useState(null);
  const [tempSettings, setTempSettings] = useState({});
  
  const [newWidgetType, setNewWidgetType] = useState('hero');

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  useEffect(() => {
    const fetchProfiles = async () => {
      const data = await API.getAppProfiles();
      setProfiles(data);
      if (data.length > 0) {
        setSelectedProfileId(String(data[0].id));
      }
    };
    fetchProfiles();
  }, []);

  useEffect(() => {
    if (selectedProfileId) {
      const fetchPages = async () => {
        const data = await API.getAppPages(selectedProfileId);
        setPages(data);
        if (data.length > 0) {
          setSelectedPageId(String(data[0].id));
        } else {
          setWidgets([]);
        }
      };
      fetchPages();
    }
  }, [selectedProfileId]);

  useEffect(() => {
    if (selectedPageId) {
      const selectedPage = pages.find(p => String(p.id) === selectedPageId);
      if (selectedPage && selectedPage.widgets) {
        setWidgets(selectedPage.widgets);
      }
    }
  }, [selectedPageId, pages]);

  const handleConfigureWidget = (widget) => {
    setConfiguringWidget(widget);
    setTempSettings(widget.settings || {});
    openConfigModal();
  };

  const saveWidgetConfig = () => {
    setWidgets(widgets.map(w => w.id === configuringWidget.id ? { ...w, settings: tempSettings } : w));
    closeConfigModal();
  };

  const handleDragEnd = (event) => {
    const { active, over } = event;

    if (active.id !== over.id) {
      setWidgets((items) => {
        const oldIndex = items.findIndex(i => i.id === active.id);
        const newIndex = items.findIndex(i => i.id === over.id);
        
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  };

  const handleAddWidget = () => {
    const newWidget = {
      id: 'temp_' + Math.random().toString(36).substr(2, 9),
      widget_type: newWidgetType,
      order: widgets.length,
    };
    setWidgets([...widgets, newWidget]);
  };

  const handleRemoveWidget = (id) => {
    setWidgets(widgets.filter(w => w.id !== id));
  };

  const handleSaveLayout = async () => {
    if (!selectedPageId) return;
    const success = await API.saveAppWidgets(selectedPageId, widgets.map((w, index) => ({ ...w, order: index })));
    if (success) {
      notifications.show({
        title: 'Success',
        message: 'Layout saved successfully.',
        color: 'green',
      });
      // Optionally trigger re-fetch to get real IDs instead of temp_ ids
      const data = await API.getAppPages(selectedProfileId);
      setPages(data);
    }
  };

  return (
    <>
      <Box p="md" h="100%">
      <Title order={2} mb="md">App Page Builder</Title>
      
      <Group align="flex-start" h="100%">
        {/* Sidebar */}
        <Paper withBorder p="md" w={300}>
          <Title order={4} mb="sm">Settings</Title>
          <Select 
            label="Profile" 
            data={profiles.map(p => ({ value: String(p.id), label: p.name }))} 
            value={selectedProfileId}
            onChange={setSelectedProfileId}
            mb="sm"
          />
          <Select 
            label="Page" 
            data={pages.map(p => ({ value: String(p.id), label: p.title }))} 
            value={selectedPageId}
            onChange={setSelectedPageId}
            mb="md"
          />
          
          <Divider mb="md" />
          
          <Title order={5} mb="sm">Add Widget</Title>
          <Select 
            data={WIDGET_TYPES} 
            value={newWidgetType}
            onChange={setNewWidgetType}
            mb="sm"
          />
          <Button fullWidth onClick={handleAddWidget}>Add Widget</Button>
        </Paper>

        {/* Canvas */}
        <Paper withBorder p="md" style={{ flex: 1, minHeight: '500px' }}>
          <Group justify="space-between" mb="md">
            <Title order={4}>Canvas - {pages.find(p => String(p.id) === selectedPageId)?.title || 'Home Screen'}</Title>
            <Button color="green" onClick={handleSaveLayout}>Save Layout</Button>
          </Group>
          
          <Box bg="gray.1" p="md" style={{ borderRadius: '8px', minHeight: '400px' }}>
            <DndContext 
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={handleDragEnd}
            >
              <SortableContext 
                items={widgets.map(w => w.id)}
                strategy={verticalListSortingStrategy}
              >
                {widgets.map((widget) => (
                  <SortableItem 
                    key={widget.id} 
                    id={widget.id} 
                    widget={widget} 
                    onRemove={handleRemoveWidget}
                    onConfigure={handleConfigureWidget}
                  />
                ))}
              </SortableContext>
            </DndContext>
            
            {widgets.length === 0 && (
              <Text c="dimmed" ta="center" mt="xl">No widgets added yet. Add some from the sidebar.</Text>
            )}
          </Box>
        </Paper>
      </Group>
    </Box>
      
      <Modal opened={configModalOpened} onClose={closeConfigModal} title="Configure Widget">
        {configuringWidget && (
          <Stack>
            <Text size="sm" c="dimmed">
              Widget Type: {WIDGET_TYPES.find(w => w.value === configuringWidget.widget_type)?.label}
            </Text>
            
            {configuringWidget.widget_type === 'recently_added' && (
              <TextInput
                label="Server ID / Source ID"
                description="Optional: Filter this widget to only show contents from a specific server."
                value={tempSettings.server_id || ''}
                onChange={(e) => setTempSettings({ ...tempSettings, server_id: e.currentTarget.value })}
              />
            )}
            
            {configuringWidget.widget_type === 'category_row' && (
              <TextInput
                label="Category ID"
                description="The ID of the category or genre to display."
                value={tempSettings.category_id || ''}
                onChange={(e) => setTempSettings({ ...tempSettings, category_id: e.currentTarget.value })}
              />
            )}

            {configuringWidget.widget_type === 'custom_banner' && (
              <>
                <TextInput
                  label="Banner Title"
                  value={tempSettings.title || ''}
                  onChange={(e) => setTempSettings({ ...tempSettings, title: e.currentTarget.value })}
                />
                <TextInput
                  label="Banner Text / Description"
                  value={tempSettings.text || ''}
                  onChange={(e) => setTempSettings({ ...tempSettings, text: e.currentTarget.value })}
                />
              </>
            )}

            <Button onClick={saveWidgetConfig} mt="md">Save Configuration</Button>
          </Stack>
        )}
      </Modal>
    </>
  );
};

const AppBuilder = () => {
  return (
    <ErrorBoundary>
      <PageContent />
    </ErrorBoundary>
  );
};

export default AppBuilder;
