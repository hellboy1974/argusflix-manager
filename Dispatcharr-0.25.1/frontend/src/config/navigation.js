import {
  ListOrdered,
  Play,
  Database,
  LayoutGrid,
  Settings as LucideSettings,
  ChartLine,
  Video,
  PlugZap,
  Package,
  Download,
  User,
  FileImage,
  Webhook,
  Logs,
  Blocks,
  MonitorCog,
  Terminal,
  Film,
  Tv,
  ListPlus,
} from 'lucide-react';

export const NAV_ITEMS = {
  media: {
    id: 'media',
    label: 'Playlists & Content',
    icon: Tv,
    paths: [
      { label: 'Live TV', icon: ListOrdered, path: '/channels', adminOnly: false },
      { label: 'Movies', icon: Film, path: '/movies', adminOnly: true },
      { label: 'Series', icon: Tv, path: '/series', adminOnly: true },
      { label: 'Playlists', icon: ListPlus, path: '/playlists', adminOnly: true },
    ]
  },
  content_import: {
    id: 'content_import',
    label: 'Content Import',
    icon: Play,
    path: '/content-import',
    adminOnly: true,
  },
  guide: {
    id: 'guide',
    label: 'TV Guide',
    icon: LayoutGrid,
    path: '/guide',
    adminOnly: false,
  },
  dvr: {
    id: 'dvr',
    label: 'DVR',
    icon: Database,
    path: '/dvr',
    adminOnly: true,
  },
  stats: {
    id: 'stats',
    label: 'Stats',
    icon: ChartLine,
    path: '/stats',
    adminOnly: true,
  },
  plugins: {
    id: 'plugins',
    label: 'Plugins',
    icon: PlugZap,
    adminOnly: true,
    paths: [
      { label: 'My Plugins', icon: Package, path: '/plugins' },
      { label: 'Find Plugins', icon: Download, path: '/plugins/browse' },
    ],
  },
  stalker: {
    id: 'stalker',
    label: 'Stalker Toolbox',
    icon: Terminal,
    path: '/stalker-toolbox',
    adminOnly: true,
  },
  integrations: {
    id: 'integrations',
    label: 'Integrations',
    icon: Blocks,
    adminOnly: true,
    paths: [
      { label: 'Connections', icon: Webhook, path: '/connect' },
      { label: 'Logs', icon: Logs, path: '/connect/logs' },
    ],
  },
  system: {
    id: 'system',
    label: 'System',
    icon: MonitorCog,
    adminOnly: true,
    canHide: false,
    paths: [
      { label: 'Users', icon: User, path: '/users' },
      { label: 'Logo Manager', icon: FileImage, path: '/logos' },
      { label: 'Settings', icon: LucideSettings, path: '/settings' },
    ],
  },
  settings: {
    id: 'settings',
    label: 'Settings',
    icon: LucideSettings,
    path: '/settings',
    adminOnly: false,
    canHide: false,
  },
};

export const DEFAULT_ADMIN_ORDER = [
  'media',
  'content_import',
  'guide',
  'dvr',
  'stats',
  'plugins',
  'stalker',
  'integrations',
  'system',
];

export const DEFAULT_USER_ORDER = [
  'media',
  'guide',
  'settings',
];

export const getOrderedNavItems = (userOrder, isAdmin, channelIds = [], uiPlugins = []) => {
  const defaultOrder = isAdmin ? DEFAULT_ADMIN_ORDER : DEFAULT_USER_ORDER;

  let order;
  if (userOrder && Array.isArray(userOrder) && userOrder.length > 0) {
    // Filter saved order to only include allowed items or plugins
    const filteredOrder = userOrder.filter((id) => defaultOrder.includes(id) || id.startsWith('plugin-'));

    // Find any new items that aren't in the saved order and append them
    const missingItems = defaultOrder.filter(
      (id) => !filteredOrder.includes(id)
    );

    // Find any new plugins that aren't in the saved order and append them
    const missingPlugins = uiPlugins
      .map((p) => p.id)
      .filter((id) => !filteredOrder.includes(id));

    order = [...filteredOrder, ...missingItems, ...missingPlugins];
  } else {
    // Insert uiPlugins into defaultOrder before integrations, system, or settings
    const insertIndex = defaultOrder.findIndex(
      (id) => id === 'integrations' || id === 'system' || id === 'settings'
    );
    const orderList = [...defaultOrder];
    const pluginIds = uiPlugins.map((p) => p.id);
    if (insertIndex !== -1) {
      orderList.splice(insertIndex, 0, ...pluginIds);
      order = orderList;
    } else {
      order = [...orderList, ...pluginIds];
    }
  }

  // Combine NAV_ITEMS with dynamic UI plugins map
  const pluginItemsMap = {};
  uiPlugins.forEach((p) => {
    pluginItemsMap[p.id] = p;
  });

  return order.map((id) => {
    const item = NAV_ITEMS[id] || pluginItemsMap[id];
    if (!item) return null;

    // Group item (has paths array)
    if (item.paths) {
      // Filter sub-paths based on adminOnly & isAdmin
      const filteredPaths = item.paths
        .map((p) => {
          const childItem = { ...p };
          if (p.path === '/channels') {
            childItem.badge = `(${Array.isArray(channelIds) ? channelIds.length : 0})`;
          }
          return childItem;
        })
        .filter((p) => !p.adminOnly || isAdmin);

      if (filteredPaths.length === 0) return null;

      return {
        id: item.id,
        label: item.label,
        icon: item.icon,
        paths: filteredPaths,
        canHide: item.canHide,
      };
    }

    const navItem = {
      id: item.id,
      label: item.label,
      icon: item.icon,
      path: item.path,
      canHide: item.canHide,
    };

    return navItem;
  }).filter(Boolean);
};
