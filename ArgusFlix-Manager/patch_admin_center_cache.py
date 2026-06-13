import re

# 1. Patch api.js
with open("frontend/src/api.js", "r", encoding="utf-8") as f:
    api_content = f.read()

api_addition = """
  static async clearSystemCache() {
    try {
      const response = await request(`${host}/api/core/admin/cache/clear/`, {
        method: 'POST',
      });
      return response;
    } catch (e) {
      errorNotification('Failed to clear system cache', e);
      throw e;
    }
  }
"""

if "clearSystemCache" not in api_content:
    api_content = api_content.replace("  static async triggerProviderAudit() {", api_addition + "\n  static async triggerProviderAudit() {")
    with open("frontend/src/api.js", "w", encoding="utf-8") as f:
        f.write(api_content)


# 2. Patch AdminCenter.jsx
with open("frontend/src/pages/AdminCenter.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add states
state_orig = "  const [savingOffset, setSavingOffset] = useState({});"
state_new = """  const [savingOffset, setSavingOffset] = useState({});
  const [clearingCache, setClearingCache] = useState(false);"""
content = content.replace(state_orig, state_new)

# Add cache handler
handler_orig = """  const handleTriggerAudit = async () => {"""
handler_new = """  const handleClearCache = async () => {
    setClearingCache(true);
    try {
      const resp = await API.clearSystemCache();
      if (resp?.success) {
        notifications.show({ title: 'Cache Cleared', message: 'Der System-Cache wurde erfolgreich geleert.', color: 'green' });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setClearingCache(false);
    }
  };

  const handleTriggerAudit = async () => {"""
content = content.replace(handler_orig, handler_new)

# Tab
panel_orig = """        <Tabs.Panel value="cache" pt="md">
          <Text c="dimmed">Cache-Buster Modul befindet sich in Entwicklung.</Text>
        </Tabs.Panel>"""
panel_new = """        <Tabs.Panel value="cache" pt="md">
          <Card shadow="sm" p="md" radius="md" withBorder>
            <Stack gap="md">
              <Group justify="space-between" align="center">
                <Box>
                  <Text fw={500} size="lg">Cache-Buster</Text>
                  <Text c="dimmed" size="sm">Löscht serverseitigen Image- und API-Cache auf Knopfdruck.</Text>
                </Box>
                <Database size={32} opacity={0.3} />
              </Group>
              
              <Text size="sm">
                Wenn Kanallogos nicht richtig aktualisiert werden oder du veraltete EPG-Daten siehst, kann das Leeren des Caches Abhilfe schaffen.
              </Text>
              
              <Group justify="center" mt="xl" mb="xl">
                <Button 
                  size="lg" 
                  color="red" 
                  leftSection={<Trash size={20} />} 
                  onClick={handleClearCache} 
                  loading={clearingCache}
                  loaderProps={{ type: 'bars' }}
                >
                  SYSTEM-CACHE LEEREN
                </Button>
              </Group>
            </Stack>
          </Card>
        </Tabs.Panel>"""
content = content.replace(panel_orig, panel_new)

with open("frontend/src/pages/AdminCenter.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched AdminCenter.jsx and api.js for Cache Buster!")
