import React, { useState, useMemo } from 'react';
import {
  Modal,
  TextInput,
  Button,
  Group,
  Stack,
  Text,
  Box,
  ScrollArea,
  Divider,
} from '@mantine/core';

const VODRegexRenameModal = ({
  opened,
  onClose,
  items = [],
  onApply = async () => {},
  loading = false,
  title = 'Regex Find & Replace',
}) => {
  const [findPat, setFindPat] = useState('');
  const [replacePat, setReplacePat] = useState('');

  // Live client-side regex preview
  const previewList = useMemo(() => {
    if (!findPat) return [];
    try {
      const regex = new RegExp(findPat, 'g');
      return items.map((item) => {
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
  }, [items, findPat, replacePat]);

  const handleApply = () => {
    onApply(findPat, replacePat);
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={title}
      size="md"
      centered
    >
      <Stack gap="md">
        <Text size="xs" c="dimmed">
          Apply a regex find & replace to the names of the {items.length} selected items.
        </Text>
        <TextInput
          label="Find Pattern (Regex)"
          placeholder="e.g. ^DE:\s*"
          value={findPat}
          onChange={(e) => setFindPat(e.target.value)}
          required
        />
        <TextInput
          label="Replace With"
          placeholder="e.g. My Custom Title (or leave empty)"
          value={replacePat}
          onChange={(e) => setReplacePat(e.target.value)}
        />

        {findPat && (
          <Box mt="xs">
            <Text size="xs" fw={600} mb="xs" c="dimmed">
              LIVE PREVIEW:
            </Text>
            <ScrollArea
              h={180}
              p="xs"
              style={{
                border: '1px solid #27272a',
                borderRadius: '4px',
                backgroundColor: '#09090b',
              }}
            >
              <Stack gap={4}>
                {previewList.map((row) => (
                  <Group key={row.id} wrap="nowrap" justify="space-between">
                    <Text
                      size="xs"
                      c="dimmed"
                      style={{
                        flex: 1,
                        textOverflow: 'ellipsis',
                        overflow: 'hidden',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {row.before}
                    </Text>
                    <Text size="xs" c="blue" mx="xs">
                      →
                    </Text>
                    <Text
                      size="xs"
                      c={row.changed ? 'green' : 'dimmed'}
                      fw={row.changed ? 600 : 400}
                      style={{
                        flex: 1,
                        textOverflow: 'ellipsis',
                        overflow: 'hidden',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {row.after || '‹empty›'}
                    </Text>
                  </Group>
                ))}
                {previewList.length === 0 && (
                  <Text size="xs" c="dimmed" fs="italic">
                    No items match the regex pattern.
                  </Text>
                )}
              </Stack>
            </ScrollArea>
          </Box>
        )}

        <Group justify="right" mt="md">
          <Button variant="outline" color="gray" onClick={onClose} size="xs">
            Cancel
          </Button>
          <Button
            color="blue"
            onClick={handleApply}
            loading={loading}
            disabled={!findPat}
            size="xs"
          >
            Apply
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
};

export default VODRegexRenameModal;
