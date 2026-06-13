import re

with open("frontend/src/pages/AdminCenter.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
import_orig = "import { Stack, Title, Group, Tabs, Text, Button, Table, Badge, ActionIcon, ScrollArea, Card } from '@mantine/core';"
import_new = "import { Stack, Title, Group, Tabs, Text, Button, Table, Badge, ActionIcon, ScrollArea, Card, Switch, TextInput, Box } from '@mantine/core';"
content = content.replace(import_orig, import_new)

# Add VPN states
state_orig = "  const [loading, setLoading] = useState(false);"
state_new = """  const [loading, setLoading] = useState(false);
  const [vpnGuardEnabled, setVpnGuardEnabled] = useState(false);
  const [gluetunUrl, setGluetunUrl] = useState('http://gluetun:8000');
  const [vpnStatus, setVpnStatus] = useState('unknown');"""
content = content.replace(state_orig, state_new)

# Add VPN settings fetch
fetch_orig = """  const fetchConnections = async () => {
    setLoading(true);"""
fetch_new = """  const fetchVpnSettings = async () => {
    try {
      const settingsResponse = await API.getSettings();
      const settings = settingsResponse?.results || [];
      const vpnSetting = settings.find((s) => s.key === 'vpn_guard');
      if (vpnSetting && vpnSetting.value) {
        setVpnGuardEnabled(vpnSetting.value.enabled || false);
        setGluetunUrl(vpnSetting.value.gluetun_url || 'http://gluetun:8000');
      }
      
      const statusResponse = await API.getVpnStatus();
      setVpnStatus(statusResponse?.status || 'unknown');
    } catch (e) {
      console.error(e);
    }
  };

  const saveVpnSettings = async () => {
    try {
      const settingsResponse = await API.getSettings();
      const settings = settingsResponse?.results || [];
      const vpnSetting = settings.find((s) => s.key === 'vpn_guard');
      
      const newValue = { enabled: vpnGuardEnabled, gluetun_url: gluetunUrl };
      if (vpnSetting) {
        await API.updateSetting(vpnSetting.id, { value: newValue });
      } else {
        await API.createSetting({ key: 'vpn_guard', name: 'VPN Guard Config', value: newValue });
      }
      notifications.show({ title: 'Success', message: 'VPN Guard settings saved', color: 'green' });
    } catch (e) {
      console.error(e);
      notifications.show({ title: 'Error', message: 'Failed to save VPN Guard settings', color: 'red' });
    }
  };

  const fetchConnections = async () => {
    setLoading(true);"""
content = content.replace(fetch_orig, fetch_new)

# Update useEffect
effect_orig = """  useEffect(() => {
    if (activeTab === 'monitor') {
      fetchConnections();
    }
  }, [activeTab]);"""
effect_new = """  useEffect(() => {
    if (activeTab === 'monitor') {
      fetchConnections();
    } else if (activeTab === 'vpn') {
      fetchVpnSettings();
    }
  }, [activeTab]);"""
content = content.replace(effect_orig, effect_new)

# Update VPN Tab panel
panel_orig = """        <Tabs.Panel value="vpn" pt="md">
          <Text c="dimmed">VPN-Guard Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>"""
panel_new = """        <Tabs.Panel value="vpn" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Stack gap="md">
              <Group justify="space-between" align="center">
                <Box>
                  <Text fw={500} size="lg">VPN-Guard (Gluetun Kill-Switch)</Text>
                  <Text c="dimmed" size="sm">Stoppt Stream-Proxys sofort, falls der VPN-Tunnel abbricht.</Text>
                </Box>
                <Badge color={vpnStatus === 'up' ? 'green' : vpnStatus === 'down' ? 'red' : 'gray'} variant="light" size="lg">
                  VPN STATUS: {vpnStatus.toUpperCase()}
                </Badge>
              </Group>
              
              <Switch 
                label="VPN-Guard aktivieren" 
                checked={vpnGuardEnabled}
                onChange={(event) => setVpnGuardEnabled(event.currentTarget.checked)}
                size="md"
              />
              
              <TextInput 
                label="Gluetun Control API URL"
                description="The internal Docker URL to reach Gluetun's control API (port 8000)"
                value={gluetunUrl}
                onChange={(event) => setGluetunUrl(event.currentTarget.value)}
                placeholder="http://gluetun:8000"
              />
              
              <Group justify="flex-end" mt="md">
                <Button onClick={saveVpnSettings} leftSection={<ShieldAlert size={16} />}>
                  Save Settings
                </Button>
              </Group>
            </Stack>
          </Card>
        </Tabs.Panel>"""
content = content.replace(panel_orig, panel_new)

with open("frontend/src/pages/AdminCenter.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched AdminCenter.jsx!")
