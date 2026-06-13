import React, { useEffect, useState } from 'react';
import { Box, Card, Grid, GridCol, Group, Text, Title, Loader, Center, Stack } from '@mantine/core';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import API from '../api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const DashboardVisuals = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.getDashboardVisuals();
        setData(response);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <Center p="xl"><Loader /></Center>;
  }

  if (!data || !data.content_counts) return null;

  const { content_counts, recent_streams, common_errors } = data;

  const pieData = [
    { name: 'Live TV', value: content_counts.live_tv || 0 },
    { name: 'Movies', value: content_counts.movies || 0 },
    { name: 'Series', value: content_counts.series || 0 },
  ].filter(d => d.value > 0);

  return (
    <Box mb="xl">
      <Grid gutter="md">
        <GridCol span={12} md={4}>
          <Card shadow="sm" p="lg" radius="md" withBorder h="100%" bg="#27272A">
            <Title order={4} mb="md">Content Types</Title>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </GridCol>

        <GridCol span={12} md={4}>
          <Card shadow="sm" p="lg" radius="md" withBorder h="100%" bg="#27272A">
            <Title order={4} mb="md">Most Common Errors</Title>
            {common_errors && common_errors.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={common_errors}>
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#aaa' }} />
                  <YAxis allowDecimals={false} tick={{ fill: '#aaa' }} />
                  <Tooltip cursor={{ fill: 'rgba(255, 255, 255, 0.1)' }} contentStyle={{ backgroundColor: '#333', border: 'none' }} />
                  <Bar dataKey="count" fill="#ff6b6b" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <Center h={200}>
                <Text c="dimmed">No error data available</Text>
              </Center>
            )}
          </Card>
        </GridCol>

        <GridCol span={12} md={4}>
          <Card shadow="sm" p="lg" radius="md" withBorder h="100%" bg="#27272A" style={{ overflowY: 'auto' }}>
            <Title order={4} mb="md">Recently Played</Title>
            {recent_streams && recent_streams.length > 0 ? (
              <Stack spacing="xs">
                {recent_streams.map((stream, idx) => (
                  <Box key={idx} p="xs" style={{ borderBottom: '1px solid #444' }}>
                    <Group position="apart">
                      <Text size="sm" weight={500} truncate>{stream.content_id}</Text>
                      <Text size="xs" c="dimmed">{stream.type}</Text>
                    </Group>
                    <Group position="apart" mt={4}>
                      <Text size="xs" c="dimmed">User: {stream.profile}</Text>
                      <Text size="xs" c="dimmed">
                        {stream.last_watched ? new Date(stream.last_watched).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
                      </Text>
                    </Group>
                  </Box>
                ))}
              </Stack>
            ) : (
              <Center h={200}>
                <Text c="dimmed">No recent activity</Text>
              </Center>
            )}
          </Card>
        </GridCol>
      </Grid>
    </Box>
  );
};

export default DashboardVisuals;
