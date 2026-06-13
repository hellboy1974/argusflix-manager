import React, { useEffect } from 'react';
import {
  Modal,
  TextInput,
  Textarea,
  NumberInput,
  Button,
  Group,
  Stack,
  LoadingOverlay,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import useVODStore from '../../store/useVODStore';

export const VODEditModal = ({ opened, onClose, vod, type }) => {
  const updateVOD = useVODStore((s) => s.updateVOD);
  const loading = useVODStore((s) => s.loading);

  const form = useForm({
    initialValues: {
      name: '',
      description: '',
      year: '',
      rating: '',
      genre: '',
      tmdb_id: '',
      imdb_id: '',
    },
  });

  useEffect(() => {
    if (vod && opened) {
      form.setValues({
        name: vod.name || '',
        description: vod.description || '',
        year: vod.year || '',
        rating: vod.rating || '',
        genre: vod.genre || '',
        tmdb_id: vod.tmdb_id || '',
        imdb_id: vod.imdb_id || '',
      });
    }
  }, [vod, opened]);

  const handleSubmit = async (values) => {
    // Clean up empty strings to null for IDs
    const payload = {
      ...values,
      year: values.year || null,
      tmdb_id: values.tmdb_id || null,
      imdb_id: values.imdb_id || null,
    };
    
    try {
      await updateVOD(type, vod.id, payload);
      onClose();
    } catch (e) {
      // Error is handled in store
    }
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Edit VOD Metadata"
      size="lg"
      pos="relative"
    >
      <LoadingOverlay visible={loading} />
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack spacing="md">
          <TextInput
            label="Name"
            placeholder="Movie or Series Name"
            {...form.getInputProps('name')}
            required
          />
          <Textarea
            label="Description / Overview"
            placeholder="Synopsis"
            minRows={4}
            {...form.getInputProps('description')}
          />
          <Group grow>
            <NumberInput
              label="Year"
              placeholder="Release Year"
              {...form.getInputProps('year')}
            />
            <TextInput
              label="Rating"
              placeholder="e.g. 8.5"
              {...form.getInputProps('rating')}
            />
            <TextInput
              label="Genre"
              placeholder="Action, Comedy"
              {...form.getInputProps('genre')}
            />
          </Group>
          <Group grow>
            <TextInput
              label="TMDB ID"
              placeholder="e.g. 12345"
              {...form.getInputProps('tmdb_id')}
            />
            <TextInput
              label="IMDB ID"
              placeholder="e.g. tt1234567"
              {...form.getInputProps('imdb_id')}
            />
          </Group>
          
          <Group position="right" mt="xl">
            <Button variant="subtle" onClick={onClose} color="gray">
              Cancel
            </Button>
            <Button type="submit" color="indigo">
              Save Changes
            </Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
};

export default VODEditModal;
