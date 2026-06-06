import { describe, it, expect } from 'vitest';
import {
  NAV_ITEMS,
  DEFAULT_ADMIN_ORDER,
  DEFAULT_USER_ORDER,
  getOrderedNavItems,
} from '../navigation';

describe('navigation config', () => {
  describe('NAV_ITEMS', () => {
    it('has all expected nav items', () => {
      expect(NAV_ITEMS.media).toBeDefined();
      expect(NAV_ITEMS.content_import).toBeDefined();
      expect(NAV_ITEMS.guide).toBeDefined();
      expect(NAV_ITEMS.dvr).toBeDefined();
      expect(NAV_ITEMS.stats).toBeDefined();
      expect(NAV_ITEMS.plugins).toBeDefined();
      expect(NAV_ITEMS.stalker).toBeDefined();
      expect(NAV_ITEMS.integrations).toBeDefined();
      expect(NAV_ITEMS.system).toBeDefined();
      expect(NAV_ITEMS.settings).toBeDefined();
    });

    it('has correct adminOnly subpaths', () => {
      const mediaPaths = NAV_ITEMS.media.paths;
      const liveTv = mediaPaths.find(p => p.path === '/channels');
      const movies = mediaPaths.find(p => p.path === '/movies');
      const series = mediaPaths.find(p => p.path === '/series');
      const playlists = mediaPaths.find(p => p.path === '/playlists');

      expect(liveTv.adminOnly).toBe(false);
      expect(movies.adminOnly).toBe(true);
      expect(series.adminOnly).toBe(true);
      expect(playlists.adminOnly).toBe(true);
    });
  });

  describe('DEFAULT_ADMIN_ORDER', () => {
    it('includes all nav items', () => {
      const adminItems = Object.keys(NAV_ITEMS).filter(
        (id) => id !== 'settings'
      );
      expect(DEFAULT_ADMIN_ORDER).toHaveLength(adminItems.length);
      adminItems.forEach((id) => {
        expect(DEFAULT_ADMIN_ORDER).toContain(id);
      });
    });
  });

  describe('DEFAULT_USER_ORDER', () => {
    it('includes media, guide, and settings', () => {
      expect(DEFAULT_USER_ORDER).toContain('media');
      expect(DEFAULT_USER_ORDER).toContain('guide');
      expect(DEFAULT_USER_ORDER).toContain('settings');
    });
  });

  describe('getOrderedNavItems', () => {
    it('returns default order when no saved order exists for admin', () => {
      const result = getOrderedNavItems(null, true);

      expect(result.map((item) => item.id)).toEqual(DEFAULT_ADMIN_ORDER);
    });

    it('returns default order when no saved order exists for non-admin', () => {
      const result = getOrderedNavItems(null, false);

      expect(result.map((item) => item.id)).toEqual(DEFAULT_USER_ORDER);
    });

    it('uses custom order when provided', () => {
      const customOrder = [
        'integrations',
        'media',
        'content_import',
        'guide',
        'dvr',
        'stats',
        'plugins',
        'stalker',
        'system',
      ];
      const result = getOrderedNavItems(customOrder, true);

      expect(result.map((item) => item.id)).toEqual(customOrder);
    });

    it('appends missing items to end of saved order', () => {
      const savedOrder = ['media', 'content_import'];
      const result = getOrderedNavItems(savedOrder, true);

      expect(result[0].id).toBe('media');
      expect(result[1].id).toBe('content_import');

      expect(result).toHaveLength(DEFAULT_ADMIN_ORDER.length);

      const resultIds = result.map((item) => item.id);
      expect(resultIds).toContain('guide');
      expect(resultIds).toContain('stalker');
      expect(resultIds).toContain('integrations');
    });

    it('filters out admin-only sub-paths for non-admin users', () => {
      const result = getOrderedNavItems(null, false);
      const mediaItem = result.find(item => item.id === 'media');

      expect(mediaItem).toBeDefined();
      expect(mediaItem.paths).toHaveLength(1);
      expect(mediaItem.paths[0].path).toBe('/channels');
    });

    it('adds channel badge to Live TV sub-path with correct count', () => {
      const channels = ['1', '2', '3'];
      const result = getOrderedNavItems(null, true, channels);

      const mediaItem = result.find((item) => item.id === 'media');
      const liveTvPath = mediaItem.paths.find(p => p.path === '/channels');
      expect(liveTvPath.badge).toBe('(3)');
    });

    it('returns items with correct structure', () => {
      const result = getOrderedNavItems(null, true);

      result.forEach((item) => {
        expect(item).toHaveProperty('id');
        expect(item).toHaveProperty('label');
        expect(item).toHaveProperty('icon');
        expect(item.path !== undefined || Array.isArray(item.paths)).toBe(true);
      });
    });
  });
});
