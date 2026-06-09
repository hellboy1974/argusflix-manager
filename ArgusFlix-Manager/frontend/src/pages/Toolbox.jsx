import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Loader, Text, Center } from '@mantine/core';
import useAuthStore from '../store/auth.jsx';
import { usePluginStore } from '../store/plugins.jsx';

const host = import.meta.env.DEV
  ? `http://${window.location.hostname}:5656`
  : '';

export default function Toolbox() {
  const { pluginKey } = useParams();
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const getToken = useAuthStore((s) => s.getToken);
  const plugins = usePluginStore((s) => s.plugins);
  const fetchPlugins = usePluginStore((s) => s.fetchPlugins);

  useEffect(() => {
    async function retrieveToken() {
      try {
        const t = await getToken();
        setToken(t);
      } catch (e) {
        console.error('Failed to get token for toolbox iframe', e);
      }
    }
    retrieveToken();
    setLoading(true); // Reset loading when changing plugins
  }, [getToken, pluginKey]);

  useEffect(() => {
    if (plugins.length === 0) {
      fetchPlugins();
    }
  }, [plugins, fetchPlugins]);

  const plugin = plugins.find((p) => p.key === pluginKey);

  if (!plugin) {
    return (
      <Center style={{ height: 'calc(100vh - 60px)' }}>
        <Loader size="md" />
        <Text ml="md">Loading plugin information...</Text>
      </Center>
    );
  }

  if (!plugin.enabled) {
    return (
      <Center style={{ height: 'calc(100vh - 60px)' }}>
        <Text c="red" fw={500}>
          Plugin '{plugin.name}' is currently disabled.
        </Text>
      </Center>
    );
  }

  const iframeSrc = `${host}/api/plugins/plugins/${pluginKey}/ui/?token=${encodeURIComponent(
    token || ''
  )}`;

  return (
    <Box
      style={{
        height: 'calc(100vh - 40px)',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        width: '100%',
        overflow: 'hidden',
      }}
    >
      {loading && (
        <Center
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 10,
            backgroundColor: '#18181b',
          }}
        >
          <Loader size="md" />
          <Text ml="md">Loading {plugin.name} UI...</Text>
        </Center>
      )}
      {token && (
        <iframe
          src={iframeSrc}
          title={plugin.name}
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            background: 'transparent',
            borderRadius: '8px',
          }}
          onLoad={() => setLoading(false)}
        />
      )}
    </Box>
  );
}
