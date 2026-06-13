import { getIconComponent } from './icons';
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
  Smartphone,
  Film,
  Tv,
  ListPlus,
  Activity,
  Map,
  Import,
  Server,
  Settings2,
  LayoutTemplate,
  RefreshCw,
} from 'lucide-react';

export const NAV_ITEMS = {
  admin_center: {
    id: 'admin_center',
    label: 'Admin Center',
    icon: Activity,
    path: '/admin-center',
    adminOnly: true,
  },

  channels: {
    id: 'channels',
    label: 'Channels',
    icon: ListOrdered,
    path: '/channels',
    adminOnly: false,
    hasBadge: true,
  },
  movies: {
    id: 'movies',
    label: 'Movies',
    icon: Film,
    path: '/movies',
    adminOnly: true,
  },
  series: {
    id: 'series',
    label: 'Series',
    icon: Tv,
    path: '/series',
    adminOnly: true,
  },
  custom_playlists: {
    id: 'custom_playlists',
    label: 'Custom Playlists',
    icon: ListPlus,
    path: '/custom-playlists',
    adminOnly: true,
  },
  updates: {
    id: 'updates',
    label: 'Updates',
    icon: RefreshCw,
    path: '/updates',
    adminOnly: true,
    hasBadge: true,
  },
  sources: {
    id: 'sources',
    label: 'Sources & EPG',
    icon: Play,
    adminOnly: true,
    paths: [
      { label: 'Verbindungen', icon: ListOrdered, path: '/sources' },
      { label: 'Content Import', icon: Import, path: '/content-import' },
      { label: 'EPG Mapping', icon: Map, path: '/epg-mapping' }
    ],
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
  admin: {
    id: 'admin',
    label: 'Admin Center',
    icon: Activity,
    adminOnly: true,
    paths: [
      { label: 'Dashboard Stats', icon: ChartLine, path: '/stats' },
      { label: 'Automations', icon: Settings2, path: '/automations' },
      { label: 'Argus TV Devices', icon: Smartphone, path: '/devices' },
      { label: 'Media Servers', icon: Server, path: '/media-servers' },
      { label: 'App Builder', icon: LayoutTemplate, path: '/app-builder' },
      { label: 'Metadata Providers', icon: Database, path: '/metadata-providers' }
    ]
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
      { label: 'Profiles', icon: User, path: '/profiles' },
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
  'channels',
  'admin_center',
  'updates',
  'guide',
  'movies',
  'series',
  'custom_playlists',
  'sources',
  'dvr',
  'admin',
  'plugins',
  'integrations',
  'system',
];

export const DEFAULT_USER_ORDER = [
  'channels',
  'guide',
  'settings',
];


export const getOrderedNavItems = (userOrder, isAdmin, channelIds = [], customProperties = {}) => {
  const defaultOrder = isAdmin ? DEFAULT_ADMIN_ORDER : DEFAULT_USER_ORDER;

  let order;
  if (userOrder && Array.isArray(userOrder) && userOrder.length > 0) {
    // Filter saved order to only include allowed items
    const filteredOrder = userOrder.filter((id) => defaultOrder.includes(id));

    // Find any new items that aren't in the saved order and append them
    const missingItems = defaultOrder.filter(
      (id) => !filteredOrder.includes(id)
    );

    order = [...filteredOrder, ...missingItems];
  } else {
    order = defaultOrder;
  }

  const customLabels = customProperties.navLabels || {};
  const customIcons = customProperties.navIcons || {};

  return order.map((id) => {
    const item = NAV_ITEMS[id];
    if (!item) return null;

    const label = customLabels[id] || item.label;
    const CustomIconComp = customIcons[id] ? getIconComponent(customIcons[id]) : null;
    const icon = CustomIconComp || item.icon;

    // Group item (has paths array)
    if (item.paths) {
      return {
        id: item.id,
        label: label,
        icon: icon,
        paths: item.paths,
        canHide: item.canHide,
      };
    }

    const navItem = {
      id: item.id,
      label: label,
      icon: icon,
      path: item.path,
      canHide: item.canHide,
    };

    // Add badge for channels
    if (id === 'channels') {
      navItem.badge = `(${Array.isArray(channelIds) ? channelIds.length : 0})`;
    }

    return navItem;
  }).filter(Boolean);
};
