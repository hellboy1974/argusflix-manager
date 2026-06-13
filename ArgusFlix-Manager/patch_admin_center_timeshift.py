import re

with open("frontend/src/pages/AdminCenter.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add states
state_orig = "  const [auditing, setAuditing] = useState(false);"
state_new = """  const [auditing, setAuditing] = useState(false);
  const [epgSources, setEpgSources] = useState([]);
  const [savingOffset, setSavingOffset] = useState({});"""
content = content.replace(state_orig, state_new)

# Add imports for NumberInput
import_orig = "import { Stack, Title, Group, Tabs, Text, Button, Table, Badge, ActionIcon, ScrollArea, Card, Switch, TextInput, Box } from '@mantine/core';"
import_new = "import { Stack, Title, Group, Tabs, Text, Button, Table, Badge, ActionIcon, ScrollArea, Card, Switch, TextInput, Box, NumberInput } from '@mantine/core';"
content = content.replace(import_orig, import_new)

# Add save icon
import_orig_icons = "import { Activity, ShieldAlert, LineChart, Clock, Scissors, Database, Trash, RefreshCw } from 'lucide-react';"
import_new_icons = "import { Activity, ShieldAlert, LineChart, Clock, Scissors, Database, Trash, RefreshCw, Save } from 'lucide-react';"
content = content.replace(import_orig_icons, import_new_icons)

# Fetch functions
fetch_orig = """  const fetchAuditResults = async () => {
    try {
      const data = await API.getProviderAudit();
      setAuditResults(data || []);
    } catch (e) {
      console.error(e);
    }
  };"""
fetch_new = """  const fetchAuditResults = async () => {
    try {
      const data = await API.getProviderAudit();
      setAuditResults(data || []);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchEpgSources = async () => {
    try {
      const response = await API.getEPGs();
      setEpgSources(response?.results || []);
    } catch (e) {
      console.error(e);
    }
  };

  const handleUpdateOffset = async (sourceId, newOffset) => {
    setSavingOffset(prev => ({ ...prev, [sourceId]: true }));
    try {
      await API.updateEPG({ id: sourceId, time_offset_minutes: newOffset });
      notifications.show({ title: 'Success', message: 'Timeshift offset updated', color: 'green' });
      fetchEpgSources();
    } catch (e) {
      console.error(e);
    } finally {
      setSavingOffset(prev => ({ ...prev, [sourceId]: false }));
    }
  };"""
content = content.replace(fetch_orig, fetch_new)

# Effect logic
effect_orig = """    } else if (activeTab === 'auditor') {
      fetchAuditResults();
    }
  }, [activeTab]);"""
effect_new = """    } else if (activeTab === 'auditor') {
      fetchAuditResults();
    } else if (activeTab === 'timeshift') {
      fetchEpgSources();
    }
  }, [activeTab]);"""
content = content.replace(effect_orig, effect_new)

# UI Panel
panel_orig = """        <Tabs.Panel value="timeshift" pt="md">
          <Text c="dimmed">Zeitreise-Editor Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>"""
panel_new = """        <Tabs.Panel value="timeshift" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Group justify="space-between" mb="md">
              <Box>
                <Text fw={500} size="lg">Zeitreise-Editor (EPG Timeshift)</Text>
                <Text c="dimmed" size="sm">Verschiebe das EPG global pro Provider in Minuten (z. B. -60 für eine Stunde zurück).</Text>
              </Box>
            </Group>
            
            <ScrollArea>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>EPG Source Name</Table.Th>
                    <Table.Th>Type</Table.Th>
                    <Table.Th style={{ width: 250 }}>Time Offset (Minuten)</Table.Th>
                    <Table.Th style={{ width: 100 }}>Aktion</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {epgSources.length === 0 ? (
                    <Table.Tr>
                      <Table.Td colSpan={4} ta="center">Keine EPG Sources gefunden</Table.Td>
                    </Table.Tr>
                  ) : (
                    epgSources.map((source) => (
                      <Table.Tr key={source.id}>
                        <Table.Td fw={500}>{source.name}</Table.Td>
                        <Table.Td>
                          <Badge color="blue" variant="light">{source.source_type}</Badge>
                        </Table.Td>
                        <Table.Td>
                          <NumberInput
                            defaultValue={source.time_offset_minutes || 0}
                            id={`offset-${source.id}`}
                            min={-1440}
                            max={1440}
                            step={30}
                          />
                        </Table.Td>
                        <Table.Td>
                          <Button 
                            size="xs" 
                            loading={savingOffset[source.id]}
                            onClick={() => {
                              const val = document.getElementById(`offset-${source.id}`).value;
                              handleUpdateOffset(source.id, parseInt(val, 10));
                            }}
                          >
                            Save
                          </Button>
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

print("Patched AdminCenter.jsx for Timeshift!")
