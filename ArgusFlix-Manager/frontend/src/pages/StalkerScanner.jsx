import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Title,
  Paper,
  TextInput,
  Button,
  Group,
  Stack,
  Text,
  Table,
  Badge,
  Select,
  Progress,
  ActionIcon,
  Modal,
  Textarea
} from '@mantine/core';
import { Play, Square, Check, Trash } from 'lucide-react';
import { api } from '../api';
import useWebSocketStore from '../store/websocket';

const StalkerScanner = () => {
  const [scans, setScans] = useState([]);
  const [results, setResults] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  
  const [isNewScanModalOpen, setIsNewScanModalOpen] = useState(false);
  const [portalUrl, setPortalUrl] = useState('');
  const [scanType, setScanType] = useState('random');
  const [macPrefix, setMacPrefix] = useState('00:1A:79');
  const [macCount, setMacCount] = useState(50);
  const [macRangeStart, setMacRangeStart] = useState('');
  const [macRangeEnd, setMacRangeEnd] = useState('');
  const [importedMacs, setImportedMacs] = useState('');
  const [rateLimit, setRateLimit] = useState(333); // default ~3/sec

  const wsMessage = useWebSocketStore((state) => state.lastMessage);

  useEffect(() => {
    fetchScans();
  }, []);

  useEffect(() => {
    if (wsMessage?.type === 'stalker_scan_progress') {
      const data = wsMessage.data;
      setScans((prevScans) =>
        prevScans.map((scan) =>
          scan.id === data.scan_id
            ? { ...scan, status: data.status, macs_to_test: data.macs_to_test, macs_tested: data.macs_tested, macs_found: data.macs_found }
            : scan
        )
      );
    }
  }, [wsMessage]);

  const fetchScans = async () => {
    try {
      const res = await api.get('/m3u/stalker-scan/');
      setScans(res.data);
    } catch (error) {
      console.error('Failed to fetch scans', error);
    }
  };

  const fetchResults = async (scanId) => {
    try {
      const res = await api.get(`/m3u/stalker-scan/${scanId}/results/`);
      setResults(res.data);
      setSelectedScan(scanId);
    } catch (error) {
      console.error('Failed to fetch results', error);
    }
  };

  const startScan = async () => {
    try {
      await api.post('/m3u/stalker-scan/', {
        portal_url: portalUrl,
        scan_type: scanType,
        mac_prefix: macPrefix,
        macs_to_test: macCount,
        mac_range_start: macRangeStart,
        mac_range_end: macRangeEnd,
        imported_macs: importedMacs,
        rate_limit: rateLimit
      });
      setIsNewScanModalOpen(false);
      fetchScans();
    } catch (error) {
      console.error('Failed to start scan', error);
    }
  };

  const cancelScan = async (id) => {
    try {
      await api.post(`/m3u/stalker-scan/${id}/cancel/`);
      fetchScans();
    } catch (error) {
      console.error('Failed to cancel scan', error);
    }
  };

  const approveResult = async (resultId) => {
    try {
      await api.post(`/m3u/stalker-scan-results/${resultId}/approve/`);
      fetchResults(selectedScan);
    } catch (error) {
      console.error('Failed to approve result', error);
    }
  };

  return (
    <Container size="xl" py="md">
      <Group justify="space-between" mb="lg">
        <Title order={2}>Stalker Portal Scanner</Title>
        <Button leftSection={<Play size={16} />} onClick={() => setIsNewScanModalOpen(true)}>
          Neuer Scan
        </Button>
      </Group>

      <Stack gap="lg">
        <Paper withBorder p="md" radius="md">
          <Title order={4} mb="md">Scan Historie</Title>
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Portal</Table.Th>
                <Table.Th>Typ</Table.Th>
                <Table.Th>Status</Table.Th>
                <Table.Th>Fortschritt</Table.Th>
                <Table.Th>Gefunden</Table.Th>
                <Table.Th>Aktionen</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {scans.map((scan) => (
                <Table.Tr key={scan.id}>
                  <Table.Td>{scan.portal_url}</Table.Td>
                  <Table.Td>{scan.scan_type}</Table.Td>
                  <Table.Td>
                    <Badge color={scan.status === 'running' ? 'blue' : scan.status === 'completed' ? 'green' : 'gray'}>
                      {scan.status}
                    </Badge>
                  </Table.Td>
                  <Table.Td style={{ width: '30%' }}>
                    <Text size="xs" mb={4}>{scan.macs_tested} / {scan.macs_to_test || '?'}</Text>
                    <Progress value={scan.macs_to_test ? (scan.macs_tested / scan.macs_to_test) * 100 : 0} />
                  </Table.Td>
                  <Table.Td>{scan.macs_found}</Table.Td>
                  <Table.Td>
                    <Group gap="xs">
                      {scan.status === 'running' && (
                        <ActionIcon color="red" onClick={() => cancelScan(scan.id)}>
                          <Square size={16} />
                        </ActionIcon>
                      )}
                      <Button size="xs" variant="light" onClick={() => fetchResults(scan.id)}>
                        Ergebnisse
                      </Button>
                    </Group>
                  </Table.Td>
                </Table.Tr>
              ))}
              {scans.length === 0 && (
                <Table.Tr>
                  <Table.Td colSpan={6} align="center">Keine Scans vorhanden</Table.Td>
                </Table.Tr>
              )}
            </Table.Tbody>
          </Table>
        </Paper>

        {selectedScan && (
          <Paper withBorder p="md" radius="md">
            <Title order={4} mb="md">Gefundene Accounts (Scan {selectedScan})</Title>
            <Table>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>MAC Adresse</Table.Th>
                  <Table.Th>Status</Table.Th>
                  <Table.Th>Profil</Table.Th>
                  <Table.Th>Aktion</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {results.map((r) => (
                  <Table.Tr key={r.id}>
                    <Table.Td><Text fw={500}>{r.mac_address}</Text></Table.Td>
                    <Table.Td>
                      <Badge color={r.status === 'approved' ? 'green' : 'yellow'}>{r.status}</Badge>
                    </Table.Td>
                    <Table.Td>
                      <Text size="xs" c="dimmed">
                        {r.raw_profile ? JSON.stringify(r.raw_profile).substring(0, 50) + '...' : '-'}
                      </Text>
                    </Table.Td>
                    <Table.Td>
                      {r.status === 'pending' && (
                        <Button size="xs" color="green" leftSection={<Check size={14} />} onClick={() => approveResult(r.id)}>
                          Als Account importieren
                        </Button>
                      )}
                    </Table.Td>
                  </Table.Tr>
                ))}
                {results.length === 0 && (
                  <Table.Tr>
                    <Table.Td colSpan={4} align="center">Noch keine validen MACs gefunden.</Table.Td>
                  </Table.Tr>
                )}
              </Table.Tbody>
            </Table>
          </Paper>
        )}
      </Stack>

      <Modal opened={isNewScanModalOpen} onClose={() => setIsNewScanModalOpen(false)} title="Neuer Stalker Portal Scan">
        <Stack>
          <TextInput
            label="Portal URL"
            placeholder="http://example.com/c/"
            value={portalUrl}
            onChange={(e) => setPortalUrl(e.currentTarget.value)}
            required
          />
          <Select
            label="Scan Typ"
            value={scanType}
            onChange={setScanType}
            data={[
              { value: 'random', label: 'Zufällig' },
              { value: 'sequential', label: 'Reihenfolge' },
              { value: 'import', label: 'Liste Importieren' }
            ]}
          />
          
          <TextInput
            label="Rate Limit (ms)"
            description="Pausenzeit zwischen Anfragen, um IP Bans zu vermeiden"
            type="number"
            value={rateLimit}
            onChange={(e) => setRateLimit(Number(e.currentTarget.value))}
          />

          {scanType === 'random' && (
            <>
              <TextInput
                label="MAC Präfix"
                description="Z.B. 00:1A:79 für MAG-Boxen"
                value={macPrefix}
                onChange={(e) => setMacPrefix(e.currentTarget.value)}
              />
              <TextInput
                label="Anzahl zu testen"
                type="number"
                value={macCount}
                onChange={(e) => setMacCount(Number(e.currentTarget.value))}
              />
            </>
          )}

          {scanType === 'sequential' && (
            <>
              <TextInput
                label="Start MAC"
                placeholder="00:1A:79:00:00:00"
                value={macRangeStart}
                onChange={(e) => setMacRangeStart(e.currentTarget.value)}
              />
              <TextInput
                label="End MAC"
                placeholder="00:1A:79:00:00:FF"
                value={macRangeEnd}
                onChange={(e) => setMacRangeEnd(e.currentTarget.value)}
              />
            </>
          )}

          {scanType === 'import' && (
            <Textarea
              label="MAC Adressen (eine pro Zeile)"
              minRows={5}
              value={importedMacs}
              onChange={(e) => setImportedMacs(e.currentTarget.value)}
            />
          )}

          <Button onClick={startScan} fullWidth mt="md">
            Scan Starten
          </Button>
        </Stack>
      </Modal>
    </Container>
  );
};

export default StalkerScanner;
