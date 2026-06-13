import re

# 1. Patch api.js
with open("frontend/src/api.js", "r", encoding="utf-8") as f:
    api_content = f.read()

api_addition = """
  static async scanProxyZombies() {
    try {
      const response = await request(`${host}/api/core/admin/doctor/scan/`);
      return response;
    } catch (e) {
      errorNotification('Failed to scan for proxy zombies', e);
      return { zombies: [], count: 0 };
    }
  }

  static async cleanProxyZombies() {
    try {
      const response = await request(`${host}/api/core/admin/doctor/clean/`, {
        method: 'POST',
      });
      return response;
    } catch (e) {
      errorNotification('Failed to clean proxy zombies', e);
      throw e;
    }
  }
"""

if "scanProxyZombies" not in api_content:
    api_content = api_content.replace("  static async clearSystemCache() {", api_addition + "\n  static async clearSystemCache() {")
    with open("frontend/src/api.js", "w", encoding="utf-8") as f:
        f.write(api_content)


# 2. Patch AdminCenter.jsx
with open("frontend/src/pages/AdminCenter.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# State
state_orig = "  const [clearingCache, setClearingCache] = useState(false);"
state_new = """  const [clearingCache, setClearingCache] = useState(false);
  const [zombies, setZombies] = useState([]);
  const [scanningZombies, setScanningZombies] = useState(false);
  const [cleaningZombies, setCleaningZombies] = useState(false);"""
content = content.replace(state_orig, state_new)

# Add Doctor Icon
import_orig_icons = "import { Activity, ShieldAlert, LineChart, Clock, Scissors, Database, Trash, RefreshCw, Save } from 'lucide-react';"
import_new_icons = "import { Activity, ShieldAlert, LineChart, Clock, Scissors, Database, Trash, RefreshCw, Save, AlertTriangle } from 'lucide-react';"
content = content.replace(import_orig_icons, import_new_icons)

# Fetch functions
fetch_orig = """  const handleClearCache = async () => {"""
fetch_new = """  const handleScanZombies = async () => {
    setScanningZombies(true);
    try {
      const data = await API.scanProxyZombies();
      setZombies(data?.zombies || []);
    } catch (e) {
      console.error(e);
    } finally {
      setScanningZombies(false);
    }
  };

  const handleCleanZombies = async () => {
    setCleaningZombies(true);
    try {
      const resp = await API.cleanProxyZombies();
      if (resp?.success) {
        notifications.show({ title: 'Success', message: `${resp.cleaned_count} Zombie-Prozesse wurden beendet.`, color: 'green' });
        handleScanZombies();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setCleaningZombies(false);
    }
  };

  const handleClearCache = async () => {"""
content = content.replace(fetch_orig, fetch_new)

effect_orig = """    } else if (activeTab === 'timeshift') {
      fetchEpgSources();
    }
  }, [activeTab]);"""
effect_new = """    } else if (activeTab === 'timeshift') {
      fetchEpgSources();
    } else if (activeTab === 'doctor') {
      handleScanZombies();
    }
  }, [activeTab]);"""
content = content.replace(effect_orig, effect_new)


# Tab
panel_orig = """        <Tabs.Panel value="doctor" pt="md">
          <Text c="dimmed">Proxy-Doctor Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>"""
panel_new = """        <Tabs.Panel value="doctor" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Group justify="space-between" mb="md">
              <Box>
                <Text fw={500} size="lg">Proxy-Doctor</Text>
                <Text c="dimmed" size="sm">Sucht nach hängengebliebenen Worker-Prozessen (Zombies) und bereinigt diese.</Text>
              </Box>
              <Group>
                <Button variant="default" leftSection={<RefreshCw size={14} />} onClick={handleScanZombies} loading={scanningZombies}>
                  Scan
                </Button>
                <Button color="red" leftSection={<Scissors size={14} />} onClick={handleCleanZombies} loading={cleaningZombies} disabled={zombies.length === 0}>
                  Clean Zombies
                </Button>
              </Group>
            </Group>
            
            <ScrollArea>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Client ID</Table.Th>
                    <Table.Th>User ID</Table.Th>
                    <Table.Th>Media</Table.Th>
                    <Table.Th>Start Time</Table.Th>
                    <Table.Th>Last Read</Table.Th>
                    <Table.Th>Warning</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {zombies.length === 0 ? (
                    <Table.Tr>
                      <Table.Td colSpan={6} ta="center">Keine Zombie-Prozesse gefunden! Alles läuft sauber.</Table.Td>
                    </Table.Tr>
                  ) : (
                    zombies.map((conn) => (
                      <Table.Tr key={conn.client_id}>
                        <Table.Td>{conn.client_id?.substring(0, 8)}...</Table.Td>
                        <Table.Td>{conn.user_id}</Table.Td>
                        <Table.Td>{conn.media_id || 'Live'}</Table.Td>
                        <Table.Td>{conn.start_time ? new Date(conn.start_time * 1000).toLocaleTimeString() : 'N/A'}</Table.Td>
                        <Table.Td>{conn.last_read ? new Date(conn.last_read * 1000).toLocaleTimeString() : 'N/A'}</Table.Td>
                        <Table.Td>
                          <Badge color="red" variant="light" leftSection={<AlertTriangle size={10} />}>
                            Dead Worker
                          </Badge>
                        </Table.Td>
                      </Table.Tr>
                    ))
                  )}
                </Table.Tbody>
              </Table>
            </ScrollArea>
          </Card>
        </Tabs.Panel>"""
content = content.replace(panel_orig, panel_new)

with open("frontend/src/pages/AdminCenter.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched AdminCenter.jsx and api.js for Proxy Doctor!")
