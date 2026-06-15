import React, { useState, useEffect } from 'react';
import {
  Container,
  Title,
  Paper,
  Table,
  Group,
  ActionIcon,
  Switch,
  TextInput,
  Button,
  Text,
  LoadingOverlay,
} from '@mantine/core';
import { GripVertical, Save } from 'lucide-react';
import { useListState } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import API from '../api';

const MetadataProviders = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [providers, setProviders] = useListState([]);

  useEffect(() => {
    loadProviders();
  }, []);

  const loadProviders = async () => {
    setLoading(true);
    try {
      const data = await API.getMetadataProviders();
      // Sort by priority just in case
      data.sort((a, b) => a.priority - b.priority);
      setProviders.setState(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDragEnd = ({ destination, source }) => {
    if (!destination) return;
    setProviders.reorder({ from: source.index, to: destination.index });
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // Update priorities based on current array order, and patch all changes
      for (let i = 0; i < providers.length; i++) {
        const provider = providers[i];
        await API.patchMetadataProvider(provider.id, {
          priority: i,
          api_key: provider.api_key,
          is_active: provider.is_active,
        });
      }
      notifications.show({
        title: 'Success',
        message: 'Metadata providers updated successfully',
        color: 'green',
      });
      loadProviders();
    } catch (e) {
      console.error(e);
    } finally {
      setSaving(false);
    }
  };

  const updateProviderField = (index, field, value) => {
    setProviders.setItemProp(index, field, value);
  };

  return (
    <Container size="lg" pos="relative">
      <LoadingOverlay visible={loading || saving} zIndex={1000} overlayProps={{ radius: "sm", blur: 2 }} />
      <Group justify="space-between" mb="lg">
        <Title order={2}>Metadata Providers</Title>
        <Button onClick={handleSave} leftSection={<Save size={16} />}>
          Save Changes
        </Button>
      </Group>

      <Text c="dimmed" mb="md">
        Configure API keys and prioritize which provider is queried first for metadata and images. Drag the handles to reorder.
      </Text>

      <Paper shadow="sm" radius="md" p="md" withBorder>
        <DragDropContext onDragEnd={handleDragEnd}>
          <Table verticalSpacing="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th style={{ width: 40 }}></Table.Th>
                <Table.Th>Provider</Table.Th>
                <Table.Th>API Key</Table.Th>
                <Table.Th style={{ width: 80, textAlign: 'center' }}>Active</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Droppable droppableId="providers-list" direction="vertical">
              {(provided) => (
                <Table.Tbody {...provided.droppableProps} ref={provided.innerRef}>
                  {providers.map((item, index) => (
                    <Draggable key={item.id.toString()} index={index} draggableId={item.id.toString()}>
                      {(provided, snapshot) => (
                        <Table.Tr
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          style={{
                            ...provided.draggableProps.style,
                            backgroundColor: snapshot.isDragging ? 'var(--mantine-color-default-hover)' : undefined,
                          }}
                        >
                          <Table.Td>
                            <div {...provided.dragHandleProps}>
                              <ActionIcon variant="subtle" color="gray" size="sm">
                                <GripVertical size={16} />
                              </ActionIcon>
                            </div>
                          </Table.Td>
                          <Table.Td fw={500}>{item.name}</Table.Td>
                          <Table.Td>
                            <TextInput
                              placeholder={`API Key for ${item.name}`}
                              value={item.api_key || ''}
                              onChange={(e) => updateProviderField(index, 'api_key', e.currentTarget.value)}
                            />
                          </Table.Td>
                          <Table.Td style={{ textAlign: 'center' }}>
                            <Switch
                              checked={item.is_active}
                              onChange={(e) => updateProviderField(index, 'is_active', e.currentTarget.checked)}
                            />
                          </Table.Td>
                        </Table.Tr>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Table.Tbody>
              )}
            </Droppable>
          </Table>
        </DragDropContext>
      </Paper>
    </Container>
  );
};

export default MetadataProviders;
