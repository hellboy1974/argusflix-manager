import React, { useState } from 'react';
import {
  Modal,
  Stack,
  TextInput,
  Button,
  Group,
  Text,
  Loader,
  Image,
  Box,
  Badge,
  Flex,
  Tabs,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { Film, Tv } from 'lucide-react';
import API from '../../api';

const ManualMetadataMatchModal = ({ opened, onClose, item, type, onSuccess }) => {
  const [searchBy, setSearchBy] = useState('title');
  const [tmdbId, setTmdbId] = useState('');
  const [title, setTitle] = useState(item?.name || '');
  const [year, setYear] = useState(item?.year || '');
  
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  
  const [applying, setApplying] = useState(false);

  // Reset state when opening/closing
  React.useEffect(() => {
    if (opened && item) {
      setTitle(item.name || '');
      setYear(item.year || '');
      setTmdbId('');
      setResults([]);
      setSearched(false);
    }
  }, [opened, item]);

  const handleSearch = async () => {
    setLoading(true);
    setSearched(true);
    setResults([]);
    
    try {
      const payload = {};
      if (searchBy === 'id') {
        if (!tmdbId) {
          notifications.show({ title: 'Error', message: 'TMDB ID is required', color: 'red' });
          setLoading(false);
          return;
        }
        payload.tmdb_id = tmdbId;
      } else {
        if (!title) {
          notifications.show({ title: 'Error', message: 'Title is required', color: 'red' });
          setLoading(false);
          return;
        }
        payload.title = title;
        if (year) payload.year = year;
      }

      let res;
      if (type === 'movie') {
        res = await API.searchMoviesMetadata(payload);
      } else {
        res = await API.searchSeriesMetadata(payload);
      }
      
      if (res && res.results) {
        setResults(res.results);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (metadata) => {
    setApplying(true);
    try {
      if (type === 'movie') {
        await API.applyMovieMetadata(item.id, metadata);
      } else {
        await API.applySeriesMetadata(item.id, metadata);
      }
      notifications.show({
        title: 'Success',
        message: 'Successfully applied metadata!',
        color: 'green',
      });
      onSuccess();
      onClose();
    } catch (error) {
      console.error(error);
    } finally {
      setApplying(false);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title={`Manual Metadata Match - ${type === 'movie' ? 'Movie' : 'Series'}`} size="lg">
      <Stack spacing="md">
        <Tabs value={searchBy} onChange={setSearchBy}>
          <Tabs.List>
            <Tabs.Tab value="title">Search by Title</Tabs.Tab>
            <Tabs.Tab value="id">Search by TMDB ID</Tabs.Tab>
          </Tabs.List>

          <Tabs.Panel value="title" pt="xs">
            <Group grow align="flex-end">
              <TextInput
                label="Title"
                placeholder="Avatar"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
              <TextInput
                label="Year (Optional)"
                placeholder="2009"
                value={year}
                onChange={(e) => setYear(e.target.value)}
              />
            </Group>
          </Tabs.Panel>

          <Tabs.Panel value="id" pt="xs">
            <TextInput
              label="TMDB ID"
              placeholder="19995"
              value={tmdbId}
              onChange={(e) => setTmdbId(e.target.value)}
              required
            />
          </Tabs.Panel>
        </Tabs>

        <Button onClick={handleSearch} loading={loading} fullWidth>
          Search
        </Button>

        {searched && !loading && results.length === 0 && (
          <Text c="dimmed" align="center" mt="md">No results found.</Text>
        )}

        {results.length > 0 && (
          <Stack spacing="sm" mt="sm">
            <Text weight={500}>Select a result to apply:</Text>
            {results.map((res, idx) => (
              <Flex key={idx} p="sm" gap="md" style={{ border: '1px solid #27272a', borderRadius: '8px' }}>
                {res.poster_url ? (
                  <Image src={res.poster_url} width={60} height={90} fit="cover" radius="md" />
                ) : (
                  <Box w={60} h={90} style={{ backgroundColor: '#18181b', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {type === 'movie' ? <Film size={24} color="#52525b" /> : <Tv size={24} color="#52525b" />}
                  </Box>
                )}
                
                <Stack spacing={4} flex={1}>
                  <Text weight={600} size="sm">{res.name}</Text>
                  <Group spacing="xs">
                    {res.year && <Badge size="xs" color="blue">{res.year}</Badge>}
                    {res.tmdb_id && <Badge size="xs" color="cyan">TMDB: {res.tmdb_id}</Badge>}
                    {res.rating && <Badge size="xs" color="yellow">{res.rating}</Badge>}
                  </Group>
                  <Text size="xs" c="dimmed" lineClamp={2}>{res.description}</Text>
                </Stack>
                
                <Button 
                  size="xs" 
                  color="indigo" 
                  onClick={() => handleApply(res)}
                  loading={applying}
                  style={{ alignSelf: 'center' }}
                >
                  Apply
                </Button>
              </Flex>
            ))}
          </Stack>
        )}
      </Stack>
    </Modal>
  );
};

export default ManualMetadataMatchModal;
