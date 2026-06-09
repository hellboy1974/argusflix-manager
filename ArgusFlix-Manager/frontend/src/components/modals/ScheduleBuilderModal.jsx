import React, { useState, useEffect } from 'react';
import {
  Modal,
  Box,
  Select,
  NumberInput,
  Button,
  Group,
  Text,
} from '@mantine/core';

// Helper to convert simple UI choices to Cron strings
const buildCronExpression = (type, hours, minutes, dayOfWeek) => {
  if (type === 'interval') {
    return ''; // empty means interval-based (or we rely on interval_hours)
  } else if (type === 'daily') {
    return `${minutes} ${hours} * * *`;
  } else if (type === 'weekly') {
    return `${minutes} ${hours} * * ${dayOfWeek}`;
  }
  return '';
};

// Helper to parse Cron string into simple UI choices
const parseCronExpression = (cron, intervalHours) => {
  if (!cron) {
    return { type: 'interval', hours: 0, minutes: 0, dayOfWeek: '0', intervalHours: intervalHours || 0 };
  }
  const parts = cron.split(' ');
  if (parts.length === 5) {
    const [min, hour, dom, mon, dow] = parts;
    if (dom === '*' && mon === '*' && dow === '*') {
      return { type: 'daily', hours: parseInt(hour, 10), minutes: parseInt(min, 10), dayOfWeek: '0', intervalHours: 0 };
    } else if (dom === '*' && mon === '*' && dow !== '*') {
      return { type: 'weekly', hours: parseInt(hour, 10), minutes: parseInt(min, 10), dayOfWeek: dow, intervalHours: 0 };
    }
  }
  // Fallback to advanced or interval
  return { type: 'interval', hours: 0, minutes: 0, dayOfWeek: '0', intervalHours: intervalHours || 0 };
};

const ScheduleBuilderModal = ({ opened, onClose, onSave, title, initialCron, initialInterval }) => {
  const [type, setType] = useState('interval');
  const [intervalHours, setIntervalHours] = useState(0);
  const [timeHour, setTimeHour] = useState(0);
  const [timeMinute, setTimeMinute] = useState(0);
  const [dayOfWeek, setDayOfWeek] = useState('0');

  useEffect(() => {
    if (opened) {
      const parsed = parseCronExpression(initialCron, initialInterval);
      setType(parsed.type);
      setIntervalHours(parsed.intervalHours);
      setTimeHour(parsed.hours);
      setTimeMinute(parsed.minutes);
      setDayOfWeek(parsed.dayOfWeek);
    }
  }, [opened, initialCron, initialInterval]);

  const handleSave = () => {
    const cron = buildCronExpression(type, timeHour, timeMinute, dayOfWeek);
    const interval = type === 'interval' ? intervalHours : 0;
    onSave(cron, interval);
    onClose();
  };

  return (
    <Modal opened={opened} onClose={onClose} title={title || "Schedule Builder"} centered>
      <Box mb="md">
        <Select
          label="Schedule Type"
          value={type}
          onChange={setType}
          data={[
            { value: 'interval', label: 'Every X Hours (Interval)' },
            { value: 'daily', label: 'Daily' },
            { value: 'weekly', label: 'Weekly' }
          ]}
        />
      </Box>

      {type === 'interval' && (
        <Box mb="md">
          <NumberInput
            label="Interval (Hours)"
            description="Run every X hours. Set to 0 to disable."
            value={intervalHours}
            onChange={(val) => setIntervalHours(val === '' ? 0 : val)}
            min={0}
          />
        </Box>
      )}

      {(type === 'daily' || type === 'weekly') && (
        <Group grow mb="md">
          <NumberInput
            label="Hour (0-23)"
            value={timeHour}
            onChange={(val) => setTimeHour(val === '' ? 0 : val)}
            min={0}
            max={23}
          />
          <NumberInput
            label="Minute (0-59)"
            value={timeMinute}
            onChange={(val) => setTimeMinute(val === '' ? 0 : val)}
            min={0}
            max={59}
          />
        </Group>
      )}

      {type === 'weekly' && (
        <Box mb="md">
          <Select
            label="Day of the week"
            value={dayOfWeek}
            onChange={setDayOfWeek}
            data={[
              { value: '0', label: 'Sunday' },
              { value: '1', label: 'Monday' },
              { value: '2', label: 'Tuesday' },
              { value: '3', label: 'Wednesday' },
              { value: '4', label: 'Thursday' },
              { value: '5', label: 'Friday' },
              { value: '6', label: 'Saturday' },
            ]}
          />
        </Box>
      )}

      <Group position="right" mt="xl">
        <Button variant="default" onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave}>Save Schedule</Button>
      </Group>
    </Modal>
  );
};

export default ScheduleBuilderModal;
