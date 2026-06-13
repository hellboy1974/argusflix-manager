import re

# 1. Patch api.js
with open("frontend/src/api.js", "r", encoding="utf-8") as f:
    api_content = f.read()

api_addition = """
  static async getProviderAudit() {
    try {
      const response = await request(`${host}/api/core/admin/audit/`);
      return response;
    } catch (e) {
      errorNotification('Failed to fetch provider audit results', e);
      return [];
    }
  }

  static async triggerProviderAudit() {
    try {
      const response = await request(`${host}/api/core/admin/audit/`, {
        method: 'POST',
      });
      return response;
    } catch (e) {
      errorNotification('Failed to trigger provider audit', e);
      throw e;
    }
  }
"""

if "getProviderAudit" not in api_content:
    api_content = api_content.replace("  static async getVpnStatus() {", api_addition + "\n  static async getVpnStatus() {")
    with open("frontend/src/api.js", "w", encoding="utf-8") as f:
        f.write(api_content)


# 2. Patch AdminCenter.jsx
with open("frontend/src/pages/AdminCenter.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# State
state_orig = "  const [vpnStatus, setVpnStatus] = useState('unknown');"
state_new = """  const [vpnStatus, setVpnStatus] = useState('unknown');
  const [auditResults, setAuditResults] = useState([]);
  const [auditing, setAuditing] = useState(false);"""
content = content.replace(state_orig, state_new)

# Fetch
fetch_orig = """      const statusResponse = await API.getVpnStatus();
      setVpnStatus(statusResponse?.status || 'unknown');
    } catch (e) {"""
fetch_new = """      const statusResponse = await API.getVpnStatus();
      setVpnStatus(statusResponse?.status || 'unknown');
    } catch (e) {
      console.error(e);
    }
  };

  const fetchAuditResults = async () => {
    try {
      const data = await API.getProviderAudit();
      setAuditResults(data || []);
    } catch (e) {"""
content = content.replace(fetch_orig, fetch_new)

effect_orig = """    } else if (activeTab === 'vpn') {
      fetchVpnSettings();
    }
  }, [activeTab]);"""
effect_new = """    } else if (activeTab === 'vpn') {
      fetchVpnSettings();
    } else if (activeTab === 'auditor') {
      fetchAuditResults();
    }
  }, [activeTab]);

  const handleTriggerAudit = async () => {
    setAuditing(true);
    try {
      await API.triggerProviderAudit();
      notifications.show({ title: 'Audit Started', message: 'The benchmark is running in the background. Refresh in a moment.', color: 'blue' });
    } catch (e) {
      console.error(e);
    } finally {
      setAuditing(false);
    }
  };"""
content = content.replace(effect_orig, effect_new)


# Tab
panel_orig = """        <Tabs.Panel value="auditor" pt="md">
          <Text c="dimmed">Provider-Auditor Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>"""
panel_new = """        <Tabs.Panel value="auditor" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Group justify="space-between" mb="md">
              <Box>
                <Text fw={500} size="lg">Provider-Auditor</Text>
                <Text c="dimmed" size="sm">Führt Latenz- und Verfügbarkeits-Benchmarks für alle konfigurierten M3U/XC-Provider durch.</Text>
              </Box>
              <Button leftSection={<LineChart size={14} />} onClick={handleTriggerAudit} loading={auditing}>
                Run Benchmark Now
              </Button>
            </Group>
            
            <Group justify="flex-end" mb="xs">
              <Button variant="subtle" size="xs" onClick={fetchAuditResults} leftSection={<RefreshCw size={12} />}>
                Refresh Results
              </Button>
            </Group>
            
            <ScrollArea>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Provider Name</Table.Th>
                    <Table.Th>Type</Table.Th>
                    <Table.Th>Status</Table.Th>
                    <Table.Th>Latency (ms)</Table.Th>
                    <Table.Th>Last Checked</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {auditResults.length === 0 ? (
                    <Table.Tr>
                      <Table.Td colSpan={5} ta="center">No benchmark results yet</Table.Td>
                    </Table.Tr>
                  ) : (
                    auditResults.map((res) => (
                      <Table.Tr key={res.id}>
                        <Table.Td fw={500}>{res.name}</Table.Td>
                        <Table.Td>{res.type}</Table.Td>
                        <Table.Td>
                          <Badge color={res.status === 'OK' ? 'green' : 'red'}>{res.status}</Badge>
                        </Table.Td>
                        <Table.Td>
                          <Text c={res.latency_ms > 1500 ? 'red' : res.latency_ms > 800 ? 'yellow' : 'green'} fw={500}>
                            {res.latency_ms > 0 ? `${res.latency_ms} ms` : 'N/A'}
                          </Text>
                        </Table.Td>
                        <Table.Td>{res.last_checked ? new Date(res.last_checked * 1000).toLocaleString() : 'N/A'}</Table.Td>
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

print("Patched AdminCenter.jsx and api.js for Auditor!")
