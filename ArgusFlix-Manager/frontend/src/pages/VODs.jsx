import React, { Suspense, useEffect, useState } from 'react';
import {
  Box,
  Button,
  Checkbox,
  Flex,
  Grid,
  GridCol,
  Group,
  Loader,
  LoadingOverlay,
  Pagination,
  SegmentedControl,
  Select,
  Stack,
  Switch,
  TextInput,
  Title,
  Paper,
  Text,
} from '@mantine/core';
import { Search, Trash, RotateCcw, CheckSquare } from 'lucide-react';
import { useDisclosure } from '@mantine/hooks';
import useVODStore from '../store/useVODStore';
import ErrorBoundary from '../components/ErrorBoundary.jsx';
import {
  filterCategoriesToEnabled,
  getCategoryOptions,
} from '../utils/pages/VODsUtils.js';
const SeriesModal = React.lazy(() => import('../components/SeriesModal'));
const VODModal = React.lazy(() => import('../components/VODModal'));
const VODCard = React.lazy(() => import('../components/cards/VODCard'));
const SeriesCard = React.lazy(() => import('../components/cards/SeriesCard'));

const MIN_CARD_WIDTH = 260;
const MAX_CARD_WIDTH = 320;

const useCardColumns = () => {
  const [columns, setColumns] = useState(4);

  useEffect(() => {
    const calcColumns = () => {
      const container = document.getElementById('vods-container');
      const width = container ? container.offsetWidth : window.innerWidth;
      let colCount = Math.floor(width / MIN_CARD_WIDTH);
      if (colCount < 1) colCount = 1;
      if (colCount > 6) colCount = 6;
      setColumns(colCount);
    };
    calcColumns();
    window.addEventListener('resize', calcColumns);
    return () => window.removeEventListener('resize', calcColumns);
  }, []);

  return columns;
};

const VODsPage = () => {
  const currentPageContent = useVODStore((s) => s.currentPageContent);
  const allCategories = useVODStore((s) => s.categories);
  const filters = useVODStore((s) => s.filters);
  const currentPage = useVODStore((s) => s.currentPage);
  const totalCount = useVODStore((s) => s.totalCount);
  const pageSize = useVODStore((s) => s.pageSize);
  const setFilters = useVODStore((s) => s.setFilters);
  const setPage = useVODStore((s) => s.setPage);
  const setPageSize = useVODStore((s) => s.setPageSize);
  const bulkSoftDeleteVODs = useVODStore((s) => s.bulkSoftDeleteVODs);
  const bulkRestoreVODs = useVODStore((s) => s.bulkRestoreVODs);

  const [selectMode, setSelectMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState(new Set());

  // Persist page size in localStorage
  useEffect(() => {
    const stored = localStorage.getItem('vodsPageSize');
    if (stored && !isNaN(Number(stored)) && Number(stored) !== pageSize) {
      setPageSize(Number(stored));
    }
    // eslint-disable-next-line
  }, []);

  const handlePageSizeChange = (value) => {
    setPageSize(Number(value));
    localStorage.setItem('vodsPageSize', value);
  };
  const fetchContent = useVODStore((s) => s.fetchContent);
  const fetchCategories = useVODStore((s) => s.fetchCategories);

  const [selectedSeries, setSelectedSeries] = useState(null);
  const [selectedVOD, setSelectedVOD] = useState(null);
  const [
    seriesModalOpened,
    { open: openSeriesModal, close: closeSeriesModal },
  ] = useDisclosure(false);
  const [vodModalOpened, { open: openVODModal, close: closeVODModal }] =
    useDisclosure(false);
  const [initialLoad, setInitialLoad] = useState(true);
  const columns = useCardColumns();
  const [categories, setCategories] = useState({});

  const getDisplayData = () => {
    return (currentPageContent || []).map((item) => ({
      ...item,
      _vodType: item.contentType === 'movie' ? 'movie' : 'series',
    }));
  };

  useEffect(() => {
    setCategories(filterCategoriesToEnabled(allCategories));
  }, [allCategories]);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  useEffect(() => {
    fetchContent().finally(() => setInitialLoad(false));
  }, [filters, currentPage, pageSize, fetchContent]);

  const handleVODCardClick = (vod) => {
    if (selectMode) {
      toggleSelection(vod.id);
      return;
    }
    setSelectedVOD(vod);
    openVODModal();
  };

  const handleSeriesClick = (series) => {
    if (selectMode) {
      toggleSelection(series.id);
      return;
    }
    setSelectedSeries(series);
    openSeriesModal();
  };

  const toggleSelection = (id) => {
    const newSelection = new Set(selectedIds);
    if (newSelection.has(id)) {
      newSelection.delete(id);
    } else {
      newSelection.add(id);
    }
    setSelectedIds(newSelection);
  };

  const onCategoryChange = (value) => {
    setFilters({ category: value });
    setPage(1);
    setSelectedIds(new Set());
  };

  const handleTypeChange = (value) => {
    setFilters({ type: value, category: '' });
    setPage(1);
    setSelectedIds(new Set());
  };

  const handleBulkDelete = () => {
    if (selectedIds.size === 0) return;
    const type = filters.type === 'all' ? 'movie' : (filters.type === 'movies' ? 'movie' : 'series');
    bulkSoftDeleteVODs(type, Array.from(selectedIds)).then(() => {
      setSelectedIds(new Set());
      setSelectMode(false);
    });
  };

  const handleBulkRestore = () => {
    if (selectedIds.size === 0) return;
    const type = filters.type === 'all' ? 'movie' : (filters.type === 'movies' ? 'movie' : 'series');
    bulkRestoreVODs(type, Array.from(selectedIds)).then(() => {
      setSelectedIds(new Set());
      setSelectMode(false);
    });
  };

  const categoryOptions = getCategoryOptions(categories, filters);
  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <Box p="md" id="vods-container" pos="relative">
      <Stack spacing="md">
        <Group position="apart">
          <Title order={2}>Video on Demand</Title>
          <Button 
            variant={selectMode ? "filled" : "light"} 
            color="indigo" 
            leftIcon={<CheckSquare size={16} />}
            onClick={() => {
              setSelectMode(!selectMode);
              if (selectMode) setSelectedIds(new Set());
            }}
          >
            {selectMode ? 'Cancel Selection' : 'Select Mode'}
          </Button>
        </Group>

        {/* Filters */}
        <Group spacing="md" align="end" position="apart">
          <Group spacing="md" align="end">
            <SegmentedControl
              value={filters.type}
              onChange={handleTypeChange}
              data={[
                { label: 'All', value: 'all' },
                { label: 'Movies', value: 'movies' },
                { label: 'Series', value: 'series' },
              ]}
            />

            <TextInput
              placeholder="Search VODs..."
              icon={<Search size={16} />}
              value={filters.search}
              onChange={(e) => setFilters({ search: e.target.value })}
              miw={200}
            />

            <Select
              placeholder="Category"
              data={categoryOptions}
              value={filters.category}
              onChange={onCategoryChange}
              clearable
              miw={150}
            />

            <Select
              label="Page Size"
              value={String(pageSize)}
              onChange={handlePageSizeChange}
              data={['12', '24', '48', '96'].map((v) => ({
                value: v,
                label: v,
              }))}
              w={110}
            />
          </Group>
          <Group>
            <Switch 
              label="Show Hidden (Deleted)" 
              checked={filters.is_active === false}
              onChange={(e) => {
                setFilters({ is_active: !e.currentTarget.checked });
                setSelectedIds(new Set());
              }}
            />
          </Group>
        </Group>

        {/* Content */}
        {initialLoad ? (
          <Flex justify="center" py="xl">
            <Loader size="lg" />
          </Flex>
        ) : (
          <>
            <Grid gutter="md">
              <ErrorBoundary>
                <Suspense fallback={<Loader />}>
                  {getDisplayData().map((item) => (
                    <GridCol
                      span={12 / columns}
                      key={`${item.contentType}_${item.id}`}
                      miw={MIN_CARD_WIDTH}
                      maw={MAX_CARD_WIDTH}
                      m={'0 auto'}
                    >
                      <Box pos="relative">
                        {item.contentType === 'series' ? (
                          <SeriesCard series={item} onClick={handleSeriesClick} />
                        ) : (
                          <VODCard vod={item} onClick={handleVODCardClick} />
                        )}
                        {selectMode && (
                          <Box pos="absolute" top={10} right={10} style={{ zIndex: 10 }}>
                            <Checkbox 
                              size="md" 
                              checked={selectedIds.has(item.id)} 
                              onChange={() => toggleSelection(item.id)}
                            />
                          </Box>
                        )}
                      </Box>
                    </GridCol>
                  ))}
                </Suspense>
              </ErrorBoundary>
            </Grid>

            {/* Pagination */}
            {totalPages > 1 && (
              <Flex justify="center" mt="md" mb={selectMode ? 80 : 0}>
                <Pagination
                  page={currentPage}
                  onChange={setPage}
                  total={totalPages}
                />
              </Flex>
            )}
          </>
        )}
      </Stack>

      {/* Floating Action Bar for Selection Mode */}
      {selectMode && selectedIds.size > 0 && (
        <Paper
          shadow="xl"
          radius="md"
          p="md"
          withBorder
          pos="fixed"
          bottom={20}
          left="50%"
          style={{ transform: 'translateX(-50%)', zIndex: 1000, backgroundColor: 'var(--mantine-color-dark-7)' }}
        >
          <Group spacing="lg">
            <Text weight={500}>{selectedIds.size} selected</Text>
            {filters.is_active === false ? (
              <Button color="green" leftIcon={<RotateCcw size={16} />} onClick={handleBulkRestore}>
                Restore Selected
              </Button>
            ) : (
              <Button color="red" leftIcon={<Trash size={16} />} onClick={handleBulkDelete}>
                Delete Selected
              </Button>
            )}
          </Group>
        </Paper>
      )}

      {/* Series Episodes Modal */}
      <ErrorBoundary>
        <Suspense fallback={<LoadingOverlay />}>
          <SeriesModal
            series={selectedSeries}
            opened={seriesModalOpened}
            onClose={closeSeriesModal}
          />
        </Suspense>
      </ErrorBoundary>

      {/* VOD Details Modal */}
      <ErrorBoundary>
        <Suspense fallback={<LoadingOverlay />}>
          <VODModal
            vod={selectedVOD}
            opened={vodModalOpened}
            onClose={closeVODModal}
          />
        </Suspense>
      </ErrorBoundary>
    </Box>
  );
};

export default VODsPage;
