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
  Divider,
  Tabs,
  TabsList,
  TabsPanel,
  TabsTab,
  ActionIcon,
} from '@mantine/core';
import { Play, Copy, Search, Tv } from 'lucide-react';
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
  getEpisodeAirdate,
  getEpisodeStreamUrl,
  getTmdbUrlLink,
  getYouTubeEmbedUrl,
  groupEpisodesBySeason,
  imdbUrl,
  sortBySeasonNumber,
  sortEpisodesList,
  tmdbUrl,
} from '../utils/components/SeriesModalUtils.js';
import { YouTubeTrailerModal } from '../components/modals/YouTubeTrailerModal.jsx';
import {
  filterCategoriesToEnabled,
  getCategoryOptions,
} from '../utils/pages/VODsUtils.js';

const EpisodeDetails = ({ episode, displaySeries }) => {
  return (
    <Stack spacing="sm">
      <Flex gap="md" direction={{ base: 'column', xs: 'row' }}>
        {episode.movie_image && (
          <Image
            src={episode.movie_image}
            width={120}
            height={80}
            alt={episode.name}
            fit="cover"
            style={{ borderRadius: '4px', flexShrink: 0 }}
          />
        )}
        <Box flex={1}>
          {episode.description && (
            <Box>
              <Text size="xs" weight={500} mb={2}>Description</Text>
              <Text size="xs" c="dimmed">{episode.description}</Text>
            </Box>
          )}
        </Box>
      </Flex>

      <Group spacing="md" wrap="wrap">
        {episode.rating && (
          <Box>
            <Text size="10px" weight={500} c="dimmed" mb={2}>Rating</Text>
            <Badge color="yellow" size="xs">{episode.rating}</Badge>
          </Box>
        )}
        {(episode.imdb_id || displaySeries.tmdb_id) && (
          <Box>
            <Text size="10px" weight={500} c="dimmed" mb={2}>Links</Text>
            <Group spacing={4}>
              {episode.imdb_id && (
                <Badge
                  color="yellow"
                  size="xs"
                  component="a"
                  href={imdbUrl(episode.imdb_id)}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ cursor: 'pointer' }}
                >
                  IMDb
                </Badge>
              )}
              {displaySeries.tmdb_id && (
                <Badge
                  color="cyan"
                  size="xs"
                  component="a"
                  href={getTmdbUrlLink(displaySeries, episode)}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ cursor: 'pointer' }}
                >
                  TMDb
                </Badge>
              )}
            </Group>
          </Box>
        )}
        {episode.director && (
          <Box>
            <Text size="10px" weight={500} c="dimmed" mb={2}>Director</Text>
            <Text size="xs">{episode.director}</Text>
          </Box>
        )}
        {episode.actors && (
          <Box>
            <Text size="10px" weight={500} c="dimmed" mb={2}>Cast</Text>
            <Text size="xs" lineClamp={1}>{episode.actors}</Text>
          </Box>
        )}
      </Group>

      {(episode.bitrate || episode.video || episode.audio) && (
        <Box>
          <Text size="10px" weight={500} c="dimmed" mb={2}>Technical Specs</Text>
          <Group spacing="lg">
            {episode.bitrate && episode.bitrate > 0 && (
              <Text size="10px" c="dimmed">
                <strong>Bitrate:</strong> {episode.bitrate} kbps
              </Text>
            )}
            {episode.video && Object.keys(episode.video).length > 0 && (
              <Text size="10px" c="dimmed">
                <strong>Video:</strong> {episode.video.codec_long_name || episode.video.codec_name}
                {episode.video.width && episode.video.height ? ` (${episode.video.width}x${episode.video.height})` : ''}
              </Text>
            )}
            {episode.audio && Object.keys(episode.audio).length > 0 && (
              <Text size="10px" c="dimmed">
                <strong>Audio:</strong> {episode.audio.codec_long_name || episode.audio.codec_name}
              </Text>
            )}
          </Group>
        </Box>
      )}

      {episode.m3u_account && (
        <Group spacing="xs">
          <Text size="10px" weight={500} c="dimmed">Provider: </Text>
          <Badge color="blue" variant="light" size="xs">
            {episode.m3u_account.name || episode.m3u_account}
          </Badge>
        </Group>
      )}
    </Stack>
  );
};

const SeriesDetailsPanel = ({ selectedSeries }) => {
  const { fetchSeriesInfo, fetchSeriesProviders } = useVODStore();
  const showVideo = useVideoStore((s) => s.showVideo);
  const env_mode = useSettingsStore((s) => s.environment.env_mode);

  const [detailedSeries, setDetailedSeries] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [activeTab, setActiveTab] = useState(null);
  const [expandedEpisode, setExpandedEpisode] = useState(null);
  const [providers, setProviders] = useState([]);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [loadingProviders, setLoadingProviders] = useState(false);
  const [trailerModalOpened, setTrailerModalOpened] = useState(false);
  const [trailerUrl, setTrailerUrl] = useState('');

  useEffect(() => {
    if (selectedSeries) {
      setDetailedSeries(null);
      setProviders([]);
      setSelectedProvider(null);
      setActiveTab(null);
      setExpandedEpisode(null);
      setLoadingDetails(true);

      fetchSeriesInfo(selectedSeries.id)
        .then((details) => {
          setDetailedSeries(details);
        })
        .catch((error) => {
          console.warn('Failed to fetch series details, using basic info:', error);
          setDetailedSeries(selectedSeries);
        })
        .finally(() => {
          setLoadingDetails(false);
        });

      setLoadingProviders(true);
      fetchSeriesProviders(selectedSeries.id)
        .then((providersData) => {
          setProviders(providersData);
          if (providersData.length > 0) {
            setSelectedProvider(providersData[0]);
          }
        })
        .catch((error) => {
          console.error('Failed to fetch series providers:', error);
          setProviders([]);
        })
        .finally(() => {
          setLoadingProviders(false);
        });
    } else {
      setDetailedSeries(null);
      setProviders([]);
      setSelectedProvider(null);
      setActiveTab(null);
    }
  }, [selectedSeries, fetchSeriesInfo, fetchSeriesProviders]);

  const seriesEpisodes = React.useMemo(() => {
    if (!detailedSeries) return [];
    if (detailedSeries.episodesList) {
      return sortEpisodesList(detailedSeries.episodesList);
    }
    return [];
  }, [detailedSeries]);

  const episodesBySeason = React.useMemo(() => {
    return groupEpisodesBySeason(seriesEpisodes);
  }, [seriesEpisodes]);

  const seasons = React.useMemo(() => {
    return sortBySeasonNumber(episodesBySeason);
  }, [episodesBySeason]);

  useEffect(() => {
    if (seasons.length > 0) {
      if (!activeTab || !seasons.includes(parseInt(activeTab.replace('season-', '')))) {
        setActiveTab(`season-${seasons[0]}`);
      }
    }
  }, [seasons, activeTab]);

  if (!selectedSeries) {
    return (
      <Flex h="100%" justify="center" align="center" direction="column" p="xl" style={{ backgroundColor: '#18181b' }}>
        <Tv size={64} color="#52525b" strokeWidth={1} />
        <Text c="dimmed" mt="md" size="sm">
          Select a series from the list to view its seasons, episodes, and stream providers.
        </Text>
      </Flex>
    );
  }

  const displaySeries = detailedSeries || selectedSeries;

  const handlePlayEpisode = (episode) => {
    const streamUrl = getEpisodeStreamUrl(episode, selectedProvider, env_mode);
    showVideo(streamUrl, 'vod', episode);
  };

  const handleCopyEpisodeLink = async (episode) => {
    const streamUrl = getEpisodeStreamUrl(episode, selectedProvider, env_mode);
    await copyToClipboard(streamUrl, {
      successTitle: 'Link Copied!',
      successMessage: 'Episode link copied to clipboard',
    });
  };

  const onClickYouTubeTrailer = () => {
    if (displaySeries.youtube_trailer) {
      setTrailerUrl(getYouTubeEmbedUrl(displaySeries.youtube_trailer));
      setTrailerModalOpened(true);
    }
  };

  return (
    <ScrollArea h="100%" p="md" style={{ backgroundColor: '#18181b', position: 'relative' }}>
      {displaySeries.backdrop_path && displaySeries.backdrop_path.length > 0 && (
        <>
          <Image
            src={displaySeries.backdrop_path[0]}
            alt={`${displaySeries.name} backdrop`}
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
              Loading full series details and episodes...
            </Text>
          </Group>
        )}

        <Flex gap="md" direction={{ base: 'column', sm: 'row' }}>
          {(displaySeries.series_image || displaySeries.logo?.url) ? (
            <Image
              src={displaySeries.series_image || displaySeries.logo.url}
              width={160}
              height={240}
              alt={displaySeries.name}
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
              <Tv size={40} color="#52525b" />
            </Box>
          )}

          <Stack spacing="xs" flex={1}>
            <Title order={2} style={{ letterSpacing: '-0.5px' }}>{displaySeries.name}</Title>
            {displaySeries.o_name && displaySeries.o_name !== displaySeries.name && (
              <Text size="xs" c="dimmed" fs="italic">
                Original Title: {displaySeries.o_name}
              </Text>
            )}

            <Group spacing="xs" wrap="wrap">
              {displaySeries.year && <Badge color="blue">{displaySeries.year}</Badge>}
              {displaySeries.rating && <Badge color="yellow">{displaySeries.rating}</Badge>}
              {displaySeries.age && <Badge color="orange">{displaySeries.age}</Badge>}
              <Badge color="purple">Series</Badge>
              {displaySeries.episode_count && <Badge color="gray">{displaySeries.episode_count} episodes</Badge>}
              {displaySeries.imdb_id && (
                <Badge
                  color="yellow"
                  component="a"
                  href={imdbUrl(displaySeries.imdb_id)}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ cursor: 'pointer' }}
                >
                  IMDb
                </Badge>
              )}
              {displaySeries.tmdb_id && (
                <Badge
                  color="cyan"
                  component="a"
                  href={tmdbUrl(displaySeries.tmdb_id, 'tv')}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ cursor: 'pointer' }}
                >
                  TMDb
                </Badge>
              )}
            </Group>

            {displaySeries.genre && (
              <Text size="sm">
                <Text component="span" c="dimmed" weight={500}>Genre: </Text>
                {displaySeries.genre}
              </Text>
            )}

            {displaySeries.director && (
              <Text size="sm">
                <Text component="span" c="dimmed" weight={500}>Director: </Text>
                {displaySeries.director}
              </Text>
            )}

            {displaySeries.cast && (
              <Text size="sm" lineClamp={2}>
                <Text component="span" c="dimmed" weight={500}>Cast: </Text>
                {displaySeries.cast}
              </Text>
            )}
          </Stack>
        </Flex>

        {displaySeries.description && (
          <Stack spacing={4}>
            <Text size="sm" weight={600}>Overview</Text>
            <Text size="sm" c="dimmed" style={{ lineHeight: '1.6' }}>
              {displaySeries.description}
            </Text>
          </Stack>
        )}

        {displaySeries.youtube_trailer && (
          <Button
            variant="outline"
            color="red"
            size="sm"
            onClick={onClickYouTubeTrailer}
            style={{ alignSelf: 'flex-start' }}
          >
            Watch Trailer
          </Button>
        )}

        <Divider my="xs" style={{ borderColor: '#27272a' }} />

        {/* Providers Selection */}
        <Stack spacing="xs">
          <Text size="sm" weight={600}>Stream Source Selection</Text>
          {loadingProviders && (
            <Group spacing="xs">
              <Loader size="xs" />
              <Text size="xs" c="dimmed">Fetching series streams...</Text>
            </Group>
          )}

          {providers.length > 0 ? (
            providers.length === 1 ? (
              <Group>
                <Text size="sm">Provider: </Text>
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
                placeholder="Select provider stream..."
                style={{ maxWidth: 350 }}
                disabled={loadingProviders}
              />
            )
          ) : (
            !loadingProviders && (
              <Text size="sm" c="dimmed" fs="italic">
                No provider accounts mapped.
              </Text>
            )
          )}
        </Stack>

        <Divider my="xs" style={{ borderColor: '#27272a' }} />

        {/* Episodes Tabs Table */}
        <Stack spacing="xs">
          <Text size="sm" weight={600}>Episodes</Text>
          {loadingDetails ? (
            <Flex justify="center" py="xl">
              <Loader size="sm" />
            </Flex>
          ) : seasons.length > 0 ? (
            <Tabs value={activeTab} onChange={setActiveTab}>
              <TabsList style={{ borderBottom: '1px solid #27272a' }}>
                {seasons.map((season) => (
                  <TabsTab key={season} value={`season-${season}`}>
                    Season {season}
                  </TabsTab>
                ))}
              </TabsList>

              {seasons.map((season) => (
                <TabsPanel key={season} value={`season-${season}`} pt="sm">
                  <Table striped highlightOnHover verticalSpacing="xs">
                    <TableThead>
                      <TableTr style={{ borderColor: '#27272a' }}>
                        <TableTh style={{ width: '50px' }}>Ep</TableTh>
                        <TableTh>Title</TableTh>
                        <TableTh style={{ width: '80px' }}>Duration</TableTh>
                        <TableTh style={{ width: '70px' }}>Action</TableTh>
                      </TableTr>
                    </TableThead>
                    <TableTbody>
                      {episodesBySeason[season]?.map((episode) => (
                        <React.Fragment key={episode.id}>
                          <TableTr
                            style={{ cursor: 'pointer', borderColor: '#27272a' }}
                            onClick={() => setExpandedEpisode(expandedEpisode === episode.id ? null : episode.id)}
                          >
                            <TableTd>
                              <Badge size="xs" variant="outline">
                                {episode.episode_number || '?'}
                              </Badge>
                            </TableTd>
                            <TableTd>
                              <Text size="sm" weight={500}>{episode.name}</Text>
                              {episode.air_date && (
                                <Text size="10px" c="dimmed">{getEpisodeAirdate(episode)}</Text>
                              )}
                            </TableTd>
                            <TableTd>
                              <Text size="xs" c="dimmed">
                                {formatDuration(episode.duration_secs)}
                              </Text>
                            </TableTd>
                            <TableTd>
                              <Group spacing={4} wrap="nowrap">
                                <ActionIcon
                                  variant="filled"
                                  color="blue"
                                  size="sm"
                                  disabled={!selectedProvider}
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handlePlayEpisode(episode);
                                  }}
                                >
                                  <Play size={12} />
                                </ActionIcon>
                                <ActionIcon
                                  variant="outline"
                                  color="gray"
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleCopyEpisodeLink(episode);
                                  }}
                                >
                                  <Copy size={12} />
                                </ActionIcon>
                              </Group>
                            </TableTd>
                          </TableTr>
                          {expandedEpisode === episode.id && (
                            <TableTr>
                              <TableTd colSpan={4} style={{ backgroundColor: '#27272a', borderColor: '#27272a' }}>
                                <EpisodeDetails episode={episode} displaySeries={displaySeries} />
                              </TableTd>
                            </TableTr>
                          )}
                        </React.Fragment>
                      ))}
                    </TableTbody>
                  </Table>
                </TabsPanel>
              ))}
            </Tabs>
          ) : (
            <Text c="dimmed" size="xs" fs="italic">No episodes listed for this series.</Text>
          )}
        </Stack>
      </Stack>

      <YouTubeTrailerModal
        opened={trailerModalOpened}
        onClose={() => setTrailerModalOpened(false)}
        trailerUrl={trailerUrl}
      />
    </ScrollArea>
  );
};

const SeriesPage = () => {
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

  const [selectedSeries, setSelectedSeries] = useState(null);
  const [categories, setCategories] = useState({});
  const [searchVal, setSearchVal] = useState(filters.search || '');

  const [splitSizes, setSplitSizes] = useLocalStorage('series-splitter-sizes', [55, 45]);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  useEffect(() => {
    setCategories(filterCategoriesToEnabled(allCategories));
  }, [allCategories]);

  useEffect(() => {
    // Force filters type to series
    setFilters({ type: 'series', search: searchVal });
  }, []);

  useEffect(() => {
    fetchContent();
  }, [filters, currentPage, pageSize]);

  const handleSearchChange = (val) => {
    setSearchVal(val);
    setFilters({ type: 'series', search: val });
  };

  const handleCategoryChange = (val) => {
    setFilters({ type: 'series', category: val || '' });
    setPage(1);
  };

  const categoryOptions = getCategoryOptions(categories, { type: 'series' });
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
          {/* Left Pane: Table and Filters */}
          <Flex direction="column" h="100%" p="md" style={{ backgroundColor: '#09090b', overflow: 'hidden' }}>
            <Stack spacing="sm" mb="md">
              <Title order={3}>Series</Title>
              <Flex gap="sm" direction={{ base: 'column', sm: 'row' }}>
                <TextInput
                  placeholder="Search series..."
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
                    {currentPageContent.map((series) => {
                      const posterUrl = series.series_image || series.logo?.url;
                      return (
                        <TableTr
                          key={series.id}
                          style={{
                            cursor: 'pointer',
                            backgroundColor: selectedSeries?.id === series.id ? '#27272a' : undefined,
                            borderColor: '#27272a',
                          }}
                          onClick={() => setSelectedSeries(series)}
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
                                <Tv size={14} color="#52525b" />
                              </Box>
                            )}
                          </TableTd>
                          <TableTd>
                            <Text size="sm" weight={500}>
                              {series.name}
                            </Text>
                          </TableTd>
                          <TableTd>
                            <Text size="xs" c="dimmed">
                              {series.year || '-'}
                            </Text>
                          </TableTd>
                          <TableTd>
                            <Text size="xs" c="dimmed" lineClamp={1}>
                              {series.genre || '-'}
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
                    No series found matching your search.
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

          {/* Right Pane: Series Details */}
          <SeriesDetailsPanel selectedSeries={selectedSeries} />
        </Allotment>
      </Box>
    </ErrorBoundary>
  );
};

export default SeriesPage;
