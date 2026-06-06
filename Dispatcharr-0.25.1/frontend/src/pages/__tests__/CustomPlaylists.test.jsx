import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';
import { MantineProvider } from '@mantine/core';
import CustomPlaylistsPage from '../CustomPlaylists';
import API from '../../api';

// Mock dependencies
vi.mock('../../api', () => ({
  default: {
    getCustomPlaylists: vi.fn(),
    getChannelGroups: vi.fn(),
    getVODCategories: vi.fn(),
    getChannelsPage: vi.fn(),
    getMovies: vi.fn(),
    getSeries: vi.fn(),
    addVODCategory: vi.fn(),
    deleteVODCategory: vi.fn(),
    deleteChannelGroup: vi.fn(),
    updateCustomPlaylist: vi.fn(),
  },
}));

vi.mock('../../components/CategorySidebar', () => ({
  default: ({ categories, onSelect }) => (
    <div data-testid="category-sidebar">
      {categories.map((cat) => (
        <button key={cat.id} onClick={() => onSelect(cat.id)}>
          {cat.name}
        </button>
      ))}
    </div>
  ),
}));

vi.mock('../../components/modals/VODRegexRenameModal.jsx', () => ({
  default: () => <div data-testid="regex-modal">VODRegexRenameModal</div>,
}));

vi.mock('allotment', () => {
  const MockAllotment = ({ children }) => <div data-testid="allotment">{children}</div>;
  MockAllotment.Pane = ({ children }) => <div data-testid="allotment-pane">{children}</div>;
  return {
    Allotment: MockAllotment,
  };
});

const mockPlaylists = [
  {
    id: 1,
    name: 'My Playlist 1',
    token: 'token1',
    is_active: true,
    mapped_live_groups: [10],
    mapped_vod_categories: [20, 30],
  },
];

const mockChannelGroups = [
  { id: 10, name: 'Live Group A', channels_count: 5 },
];

const mockVodCategories = [
  { id: 20, name: 'Movie Cat A', category_type: 'movie', movie_count: 8 },
  { id: 30, name: 'Series Cat A', category_type: 'series', series_count: 12 },
];

describe('CustomPlaylistsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    API.getCustomPlaylists.mockResolvedValue(mockPlaylists);
    API.getChannelGroups.mockResolvedValue(mockChannelGroups);
    API.getVODCategories.mockResolvedValue(mockVodCategories);
  });

  const renderComponent = () =>
    render(
      <MantineProvider>
        <CustomPlaylistsPage />
      </MantineProvider>
    );

  it('renders Custom Playlists title and playlist list', async () => {
    renderComponent();

    expect(screen.getByText('Custom Playlists')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('My Playlist 1')).toBeInTheDocument();
    });
  });

  it('toggles credentials card visibility when button clicked', async () => {
    renderComponent();
    
    await waitFor(() => {
      expect(screen.getByText('Show Links')).toBeInTheDocument();
    });

    const toggleButton = screen.getByText('Show Links');
    fireEvent.click(toggleButton);

    await waitFor(() => {
      expect(screen.getByText('Hide Links')).toBeInTheDocument();
      expect(screen.getByText('M3U Link')).toBeInTheDocument();
      expect(screen.getByText('XMLTV EPG')).toBeInTheDocument();
    });
  });

  it('renders Manage Mappings button and opens mapping modal on click', async () => {
    renderComponent();
    
    await waitFor(() => {
      expect(screen.getByText('Manage Mappings')).toBeInTheDocument();
    });

    const manageButton = screen.getByText('Manage Mappings');
    fireEvent.click(manageButton);

    await waitFor(() => {
      expect(screen.getByText('Live TV Groups')).toBeInTheDocument();
      expect(screen.getByText('VOD Movie Categories')).toBeInTheDocument();
      expect(screen.getByText('VOD Series Categories')).toBeInTheDocument();
    });
  });
});
