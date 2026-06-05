import React, { useEffect, useState, useRef } from 'react';
import {
  Box,
  Flex,
  Group,
  Image,
  Text,
  Title,
  Select,
  Badge,
  Loader,
  Stack,
  Button,
  TextInput,
  Pagination,
  Table,
  TableTbody,
  TableTd,
  TableTh,
  TableThead,
  TableTr,
  ScrollArea,
} from '@mantine/core';
import { Play, Copy, Search, Film } from 'lucide-react';
import { Allotment } from 'allotment';
import 'allotment/dist/style.css';
import { copyToClipboard } from '../utils';
import useVODStore from '../store/useVODStore';
import useVideoStore from '../store/useVideoStore';
import useSettingsStore from '../store/settings';
import ErrorBoundary from '../components/ErrorBoundary';
import useLocalStorage from '../hooks/useLocalStorage';
import {
  formatDuration,
  formatStreamLabel,
  getYouTubeEmbedUrl,
  imdbUrl,
  tmdbUrl,
} from '../utils/components/SeriesModalUtils.js';
import { YouTubeTrailerModal } from '../components/modals/YouTubeTrailerModal.jsx';
import {
  formatAudioDetails,
  formatVideoDetails,
  getMovieStreamUrl,
  getTechnicalDetails,
} from '../utils/components/VODModalUtils.js';
import {
  filterCategoriesToEnabled,
  getCategoryOptions,
} from '../utils/pages/VODsUtils.js';

const MovieDetailsPanel = ({ selectedMovie }) => {
  const showVideo = useVideoStore((s) => s.showVideo);
  const env_mode = useSettingsStore((s) => s.environment.env_mode);
  const { fetchMovieDetailsFromProvider, fetchMovieProviders } = useVODStore();

  const [detailedMovie, setDetailedMovie] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [providers, setProviders] = useState([]);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [loadingProviders, setLoadingProviders] = useState(false);
  const [trailerModalOpened, setTrailerModalOpened] = useState(false);
  const [trailerUrl, setTrailerUrl] = useState('');

  useEffect(() => {
    if (selectedMovie) {
      setDetailedMovie(null);
      setProviders([]);
      setSelectedProvider(null);
      setLoadingDetails(true);

      fetchMovieDetailsFromProvider(selectedMovie.id)
        .then((details) => {
          setDetailedMovie(details);
        })
        .catch((error) => {
          console.warn('Failed to fetch provider details, using basic info:', error);
          setDetailedMovie(selectedMovie);
        })
        .finally(() => {
          setLoadingDetails(false);
        });

      setLoadingProviders(true);
      fetchMovieProviders(selectedMovie.id)
        .then((providersData) => {
          setProviders(providersData);
          if (providersData.length > 0) {
            setSelectedProvider(providersData[0]);
          }
        })
        .catch((error) => {
          console.error('Failed to fetch providers:', error);
          setProviders([]);
        })
        .finally(() => {
          setLoadingProviders(false);
        });
    } else {
      setDetailedMovie(null);
      setProviders([]);
      setSelectedProvider(null);
    }
  }, [selectedMovie, fetchMovieDetailsFromProvider, fetchMovieProviders]);

  if (!selectedMovie) {
    return (
      <Flex h="100%" justify="center" align="center" direction="column" p="xl" style={{ backgroundColor: '#18181b' }}>
        <Film size={64} color="#52525b" strokeWidth={1} />
        <Text c="dimmed" mt="md" size="sm">
          Select a movie from the list to view its details, trailer, streams, and playback settings.
        </Text>
      </Flex>
    );
  }

  const displayMovie = detailedMovie || selectedMovie;

  const getStreamUrl = () => {
    if (!displayMovie) return null;
    return getMovieStreamUrl(selectedMovie, selectedProvider, env_mode);
  };

  const handlePlayMovie = () => {
    const streamUrl = getStreamUrl();
    if (!streamUrl) return;
    showVideo(streamUrl, 'vod', displayMovie);
  };

  const handleCopyLink = async () => {
    const streamUrl = getStreamUrl();
    if (!streamUrl) return;
    await copyToClipboard(streamUrl, {
      successTitle: 'Link Copied!',
      successMessage: 'Stream link copied to clipboard',
    });
  };

  const onClickYouTubeTrailer = () => {
    if (displayMovie.youtube_trailer) {
      setTrailerUrl(getYouTubeEmbedUrl(displayMovie.youtube_trailer));
      setTrailerModalOpened(true);
    }
  };

  const techDetails = getTechnicalDetails(selectedProvider, displayMovie);
  const hasTechDetails = techDetails.bitrate || techDetails.video || techDetails.audio;
  const hasVideo = techDetails.video && Object.keys(techDetails.video).length > 0;
  const hasAudio = techDetails.audio && Object.keys(techDetails.audio).length > 0;

  return (
    <ScrollArea h="100%" p="md" style={{ backgroundColor: '#18181b', position: 'relative' }}>
      {displayMovie.backdrop_path && displayMovie.backdrop_path.length > 0 && (
        <>
          <Image
            src={displayMovie.backdrop_path[0]}
            alt={`${displayMovie.name} backdrop`}
            fit="cover"
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '350px',
              objectFit: 'cover',
              zIndex: 0,
              opacity: 0.15,
              filter: 'blur(4px) brightness(0.6)',
            }}
          />
          <Box
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '350px',
              background: 'linear-gradient(180deg, rgba(24,24,27,0) 50%, rgba(24,24,27,1) 100%)',
              zIndex: 1,
            }}
          />
        </>
      )}

      <Stack spacing="md" style={{ position: 'relative', zIndex: 2 }} mt="md">
        {loadingDetails && (
          <Group spacing="xs">
            <Loader size="xs" />
            <Text size="xs" color="dimmed">
              Loading full movie details...
            </Text>
          </Group>
        )}

        <Flex gap="md" direction={{ base: 'column', sm: 'row' }}>
          {(displayMovie.movie_image || displayMovie.logo?.url) ? (
            <Image
              src={displayMovie.movie_image || displayMovie.logo.url}
              width={160}
              height={240}
              alt={displayMovie.name}
              fit="contain"
              style={{ borderRadius: '8px', flexShrink: 0, boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
            />
          ) : (
            <Box
              style={{
                width: 160,
                height: 240,
                backgroundColor: '#27272a',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '8px',
                flexShrink: 0,
              }}
            >
              <Film size={40} color="#52525b" />
            </Box>
          )}

          <Stack spacing="xs" flex={1}>
            <Title order={2} style={{ letterSpacing: '-0.5px' }}>{displayMovie.name}</Title>
            {displayMovie.o_name && displayMovie.o_name !== displayMovie.name && (
              <Text size="xs" c="dimmed" fs="italic">
                Original Title: {displayMovie.o_name}
              </Text>
            )}

            <Group spacing="xs" wrap="wrap">
              {displayMovie.year && <Badge color="blue">{displayMovie.year}</Badge>}
              {displayMovie.duration_secs && <Badge color="gray">{formatDuration(displayMovie.duration_secs)}</Badge>}
              {displayMovie.rating && <Badge color="yellow">{displayMovie.rating}</Badge>}
              {displayMovie.age && <Badge color="orange">{displayMovie.age}</Badge>}
              {displayMovie.imdb_id && (
                <Badge
                  color="yellow"
                  component="a"
                  href={imdbUrl(displayMovie.imdb_id)}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ cursor: 'pointer' }}
                >
                  IMDb
                </Badge>
              )}
              {displayMovie.tmdb_id && (
                <Badge
                  color="cyan"
                  component="a"
                  href={tmdbUrl(displayMovie.tmdb_id, 'movie')}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ cursor: 'pointer' }}
                >
                  TMDb
                </Badge>
              )}
            </Group>

            {displayMovie.genre && (
              <Text size="sm">
                <Text component="span" c="dimmed" weight={500}>Genre: </Text>
                {displayMovie.genre}
              </Text>
            )}

            {displayMovie.director && (
              <Text size="sm">
                <Text component="span" c="dimmed" weight={500}>Director: </Text>
                {displayMovie.director}
              </Text>
            )}

            {displayMovie.actors && (
              <Text size="sm" lineClamp={2}>
                <Text component="span" c="dimmed" weight={500}>Cast: </Text>
                {displayMovie.actors}
              </Text>
            )}
          </Stack>
        </Flex>

        {displayMovie.description && (
          <Stack spacing={4}>
            <Text size="sm" weight={600}>Overview</Text>
            <Text size="sm" c="dimmed" style={{ lineHeight: '1.6' }}>
              {displayMovie.description}
            </Text>
          </Stack>
        )}

        <Divider my="xs" style={{ borderColor: '#27272a' }} />

        {/* Streams & Providers Section */}
        <Stack spacing="xs">
          <Text size="sm" weight={600}>Available Streams</Text>
          
          {loadingProviders && (
            <Group spacing="xs">
              <Loader size="xs" />
              <Text size="xs" c="dimmed">Fetching streams...</Text>
            </Group>
          )}

          {providers.length > 0 ? (
            <Stack spacing="sm">
              {providers.length === 1 ? (
                <Group>
                  <Text size="sm">Source: </Text>
                  <Badge color="blue" variant="light">
                    {providers[0].m3u_account.name}
                  </Badge>
                </Group>
              ) : (
                <Select
                  data={providers.map((p) => ({
                    value: p.id.toString(),
                    label: formatStreamLabel(p),
                  }))}
                  value={selectedProvider?.id?.toString() || ''}
                  onChange={(val) => {
                    const found = providers.find((p) => p.id.toString() === val);
                    setSelectedProvider(found);
                  }}
                  placeholder="Select stream provider..."
                  style={{ maxWidth: 350 }}
                  disabled={loadingProviders}
                />
              )}

              <Group spacing="xs">
                <Button
                  leftSection={<Play size={16} />}
                  color="blue"
                  size="sm"
                  onClick={handlePlayMovie}
                  disabled={!selectedProvider}
                >
                  Play Movie
                </Button>
                {displayMovie.youtube_trailer && (
                  <Button
                    variant="outline"
                    color="red"
                    size="sm"
                    onClick={onClickYouTubeTrailer}
                  >
                    Watch Trailer
                  </Button>
                )}
                <Button
                  leftSection={<Copy size={16} />}
                  variant="outline"
                  color="gray"
                  size="sm"
                  onClick={handleCopyLink}
                  disabled={!selectedProvider}
                >
                  Copy URL
                </Button>
              </Group>
            </Stack>
          ) : (
            !loadingProviders && (
              <Text size="sm" c="dimmed" fs="italic">
                No stream sources found for this movie.
              </Text>
            )
          )}
        </Stack>

        {/* Technical details */}
        {hasTechDetails && selectedProvider && (
          <Stack spacing={4} mt="xs">
            <Text size="sm" weight={600}>Technical Specification</Text>
            <Box p="sm" style={{ backgroundColor: '#27272a', borderRadius: '6px' }}>
              {techDetails.bitrate && techDetails.bitrate > 0 && (
                <Text size="xs" c="dimmed" mb={2}>
                  <strong>Bitrate:</strong> {techDetails.bitrate} kbps
                </Text>
              )}
              {hasVideo && (
                <Text size="xs" c="dimmed" mb={2}>
                  <strong>Video Codec:</strong> {formatVideoDetails(techDetails.video)}
                </Text>
              )}
              {hasAudio && (
                <Text size="xs" c="dimmed">
                  <strong>Audio Tracks:</strong> {formatAudioDetails(techDetails.audio)}
                </Text>
              )}
            </Box>
          </Stack>
        )}
      </Stack>

      <YouTubeTrailerModal
        opened={trailerModalOpened}
        onClose={() => setTrailerModalOpened(false)}
        trailerUrl={trailerUrl}
      />
    </ScrollArea>
  );
};

const Divider = ({ ...props }) => (
  <Box style={{ borderBottom: '1px solid #27272a' }} {...props} />
);

const MoviesPage = () => {
  const currentPageContent = useVODStore((s) => s.currentPageContent);
  const allCategories = useVODStore((s) => s.categories);
  const filters = useVODStore((s) => s.filters);
  const currentPage = useVODStore((s) => s.currentPage);
  const totalCount = useVODStore((s) => s.totalCount);
  const pageSize = useVODStore((s) => s.pageSize);
  const loading = useVODStore((s) => s.loading);

  const setFilters = useVODStore((s) => s.setFilters);
  const setPage = useVODStore((s) => s.setPage);
  const setPageSize = useVODStore((s) => s.setPageSize);
  const fetchContent = useVODStore((s) => s.fetchContent);
  const fetchCategories = useVODStore((s) => s.fetchCategories);

  const [selectedMovie, setSelectedMovie] = useState(null);
  const [categories, setCategories] = useState({});
  const [searchVal, setSearchVal] = useState(filters.search || '');

  const [splitSizes, setSplitSizes] = useLocalStorage('movies-splitter-sizes', [55, 45]);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  useEffect(() => {
    setCategories(filterCategoriesToEnabled(allCategories));
  }, [allCategories]);

  useEffect(() => {
    // Force filters type to movies
    setFilters({ type: 'movies', search: searchVal });
  }, []);

  useEffect(() => {
    fetchContent();
  }, [filters, currentPage, pageSize]);

  // Handle Search Input Change
  const handleSearchChange = (val) => {
    setSearchVal(val);
    setFilters({ type: 'movies', search: val });
  };

  const handleCategoryChange = (val) => {
    setFilters({ type: 'movies', category: val || '' });
    setPage(1);
  };

  const categoryOptions = getCategoryOptions(categories, { type: 'movies' });
  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <ErrorBoundary>
      <Box h="100vh" w="100%" display="flex" style={{ overflow: 'hidden' }}>
        <Allotment
          defaultSizes={splitSizes}
          onChange={setSplitSizes}
          onResize={setSplitSizes}
          className="custom-allotment"
          minSize={250}
        >
          {/* Left Pane: Table and Search */}
          <Flex direction="column" h="100%" p="md" style={{ backgroundColor: '#09090b', overflow: 'hidden' }}>
            <Stack spacing="sm" mb="md">
              <Title order={3}>Movies</Title>
              <Flex gap="sm" direction={{ base: 'column', sm: 'row' }}>
                <TextInput
                  placeholder="Search movies..."
                  leftSection={<Search size={14} />}
                  value={searchVal}
                  onChange={(e) => handleSearchChange(e.target.value)}
                  style={{ flex: 1 }}
                />
                <Select
                  placeholder="All Categories"
                  data={categoryOptions}
                  value={filters.category}
                  onChange={handleCategoryChange}
                  clearable
                  style={{ width: '220px' }}
                />
                <Select
                  value={String(pageSize)}
                  onChange={(val) => {
                    setPageSize(Number(val));
                    setPage(1);
                  }}
                  data={['10', '25', '50', '100'].map((v) => ({ value: v, label: `${v} / page` }))}
                  style={{ width: '120px' }}
                />
              </Flex>
            </Stack>

            <Box flex={1} style={{ overflow: 'auto', border: '1px solid #27272a', borderRadius: '8px' }}>
              {loading ? (
                <Flex justify="center" align="center" h="100%">
                  <Loader size="md" />
                </Flex>
              ) : currentPageContent.length > 0 ? (
                <Table striped highlightOnHover verticalSpacing="sm">
                  <TableThead>
                    <TableTr style={{ borderColor: '#27272a' }}>
                      <TableTh style={{ width: '70px' }}>Poster</TableTh>
                      <TableTh>Title</TableTh>
                      <TableTh style={{ width: '80px' }}>Year</TableTh>
                      <TableTh>Genre</TableTh>
                    </TableTr>
                  </TableThead>
                  <TableTbody>
                    {currentPageContent.map((movie) => {
                      const posterUrl = movie.movie_image || movie.logo?.url;
                      return (
                        <TableTr
                          key={movie.id}
                          style={{
                            cursor: 'pointer',
                            backgroundColor: selectedMovie?.id === movie.id ? '#27272a' : undefined,
                            borderColor: '#27272a',
                          }}
                          onClick={() => setSelectedMovie(movie)}
                        >
                          <TableTd>
                            {posterUrl ? (
                              <Image
                                src={posterUrl}
                                height={45}
                                width={30}
                                fit="cover"
                                style={{ borderRadius: '4px' }}
                              />
                            ) : (
                              <Box
                                style={{
                                  height: 45,
                                  width: 30,
                                  backgroundColor: '#18181b',
                                  borderRadius: '4px',
                                  display: 'flex',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                }}
                              >
                                <Film size={14} color="#52525b" />
                              </Box>
                            )}
                          </TableTd>
                          <TableTd>
                            <Text size="sm" weight={500}>
                              {movie.name}
                            </Text>
                          </TableTd>
                          <TableTd>
                            <Text size="xs" c="dimmed">
                              {movie.year || '-'}
                            </Text>
                          </TableTd>
                          <TableTd>
                            <Text size="xs" c="dimmed" lineClamp={1}>
                              {movie.genre || '-'}
                            </Text>
                          </TableTd>
                        </TableTr>
                      );
                    })}
                  </TableTbody>
                </Table>
              ) : (
                <Flex justify="center" align="center" h="100%" direction="column" p="xl">
                  <Text size="sm" c="dimmed">
                    No movies found matching your search.
                  </Text>
                </Flex>
              )}
            </Box>

            {totalPages > 1 && (
              <Flex justify="center" mt="md">
                <Pagination
                  page={currentPage}
                  onChange={setPage}
                  total={totalPages}
                  size="sm"
                />
              </Flex>
            )}
          </Flex>

          {/* Right Pane: Movie Details */}
          <MovieDetailsPanel selectedMovie={selectedMovie} />
        </Allotment>
      </Box>
    </ErrorBoundary>
  );
};

export default MoviesPage;
