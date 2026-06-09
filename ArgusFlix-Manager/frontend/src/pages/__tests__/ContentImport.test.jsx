import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import ContentImportPage from '../ContentImport';

vi.mock('../../components/tables/M3UsTable', () => ({
  default: ({ filterType }) => (
    <div data-testid={`m3us-table-${filterType}`}>M3UsTable {filterType}</div>
  ),
}));
vi.mock('../../components/tables/StalkerPortalsTable', () => ({
  default: () => <div data-testid="stalker-portals-table">StalkerPortalsTable</div>,
}));
vi.mock('../../components/tables/EPGsTable', () => ({
  default: () => <div data-testid="epgs-table">EPGsTable</div>,
}));

describe('ContentImportPage', () => {
  it('renders page header and all four tabs', () => {
    render(
      <MantineProvider>
        <ContentImportPage />
      </MantineProvider>
    );
    
    // Check header text
    expect(screen.getByText('Content Import')).toBeInTheDocument();
    
    // Check tab list buttons
    expect(screen.getByText('Xtream Codes')).toBeInTheDocument();
    expect(screen.getByText('M3U Playlists')).toBeInTheDocument();
    expect(screen.getByText('Stalker Portals')).toBeInTheDocument();
    expect(screen.getByText('EPG-Guides')).toBeInTheDocument();
  });
});
