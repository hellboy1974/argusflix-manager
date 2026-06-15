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
import { Save, ArrowUp, ArrowDown } from 'lucide-react';
import { useListState } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
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

  const moveUp = (index) => {
    if (index === 0) return;
    setProviders.reorder({ from: index, to: index - 1 });
  };

  const moveDown = (index) => {
    if (index === providers.length - 1) return;
    setProviders.reorder({ from: index, to: index + 1 });
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
        Configure API keys and prioritize which provider is queried first for metadata and images. Use the Up/Down arrows to reorder.
      </Text>

      <Paper shadow="sm" radius="md" p="md" withBorder>
        <Table verticalSpacing="sm">
          <Table.Thead>
            <Table.Tr>
              <Table.Th style={{ width: 100, textAlign: 'center' }}>Priority</Table.Th>
              <Table.Th>Provider</Table.Th>
              <Table.Th>API Key</Table.Th>
              <Table.Th style={{ width: 80, textAlign: 'center' }}>Active</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {providers.map((item, index) => (
              <Table.Tr key={item.id.toString()}>
                <Table.Td>
                  <Group gap="xs" wrap="nowrap" justify="center">
                    <ActionIcon
                      variant="subtle"
                      color="gray"
                      size="sm"
                      disabled={index === 0}
                      onClick={() => moveUp(index)}
                    >
                      <ArrowUp size={16} />
                    </ActionIcon>
                    <ActionIcon
                      variant="subtle"
                      color="gray"
                      size="sm"
                      disabled={index === providers.length - 1}
                      onClick={() => moveDown(index)}
                    >
                      <ArrowDown size={16} />
                    </ActionIcon>
                  </Group>
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
            ))}
          </Table.Tbody>
        </Table>
      </Paper>
    </Container>
  );
};

export default MetadataProviders;
