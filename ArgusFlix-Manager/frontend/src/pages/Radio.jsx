import React, { useState, useEffect, useCallback } from 'react';
import { Radio as RadioIcon, List } from 'lucide-react';
import api from '../api';

const axios = {
  get: async (url, config) => ({ data: await api.get(url, config) }),
  post: async (url, data, config) => ({ data: await api.post(url, data, config) }),
  put: async (url, data, config) => ({ data: await api.put(url, data, config) }),
  patch: async (url, data, config) => ({ data: await api.patch(url, data, config) }),
  delete: async (url, config) => ({ data: await api.delete(url, config) }),
};
import { Stack, Group, Title, Text } from '@mantine/core';
import { Table, Button, Input, Form, Modal, Switch, Tabs, Select } from 'antd';

export default function RadioStations() {
  const [stations, setStations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loadingStations, setLoadingStations] = useState(true);
  const [loadingCategories, setLoadingCategories] = useState(true);
  
  const [isStationModalOpen, setIsStationModalOpen] = useState(false);
  const [editingStation, setEditingStation] = useState(null);
  const [stationForm] = Form.useForm();
  
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [categoryForm] = Form.useForm();

  const fetchStations = useCallback(async () => {
    setLoadingStations(true);
    try {
      const response = await axios.get('/api/radio/stations/');
      setStations(response.data);
    } catch (error) {
      console.error('Error fetching radio stations:', error);
    } finally {
      setLoadingStations(false);
    }
  }, []);

  const fetchCategories = useCallback(async () => {
    setLoadingCategories(true);
    try {
      const response = await axios.get('/api/radio/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    } finally {
      setLoadingCategories(false);
    }
  }, []);

  useEffect(() => {
    fetchStations();
    fetchCategories();
  }, [fetchStations, fetchCategories]);

  // --- Stations ---
  const handleAddStation = () => {
    setEditingStation(null);
    stationForm.resetFields();
    stationForm.setFieldsValue({ is_active: true, sort_order: 0 });
    setIsStationModalOpen(true);
  };

  const handleEditStation = (record) => {
    setEditingStation(record);
    stationForm.setFieldsValue(record);
    setIsStationModalOpen(true);
  };

  const handleDeleteStation = async (id) => {
    if (window.confirm('Are you sure you want to delete this radio station?')) {
      try {
        await axios.delete(`/api/radio/stations/${id}/`);
        fetchStations();
      } catch (error) {
        console.error('Error deleting station:', error);
      }
    }
  };

  const handleSaveStation = async (values) => {
    try {
      if (editingStation) {
        await axios.put(`/api/radio/stations/${editingStation.id}/`, values);
      } else {
        await axios.post('/api/radio/stations/', values);
      }
      setIsStationModalOpen(false);
      fetchStations();
    } catch (error) {
      console.error('Error saving station:', error);
    }
  };

  const stationColumns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Category/Genre', dataIndex: 'category_name', key: 'category_name', render: (val) => val || 'None' },
    { title: 'URL', dataIndex: 'stream_url', key: 'stream_url' },
    { title: 'Active', dataIndex: 'is_active', key: 'is_active', render: (val) => (val ? 'Yes' : 'No') },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button onClick={() => handleEditStation(record)} size="small">Edit</Button>
          <Button danger onClick={() => handleDeleteStation(record.id)} size="small">Delete</Button>
        </div>
      ),
    },
  ];

  // --- Categories ---
  const handleAddCategory = () => {
    setEditingCategory(null);
    categoryForm.resetFields();
    categoryForm.setFieldsValue({ sort_order: 0 });
    setIsCategoryModalOpen(true);
  };

  const handleEditCategory = (record) => {
    setEditingCategory(record);
    categoryForm.setFieldsValue(record);
    setIsCategoryModalOpen(true);
  };

  const handleDeleteCategory = async (id) => {
    if (window.confirm('Are you sure you want to delete this category? Stations will have their category cleared.')) {
      try {
        await axios.delete(`/api/radio/categories/${id}/`);
        fetchCategories();
        fetchStations(); // Refresh stations as category_name might be cleared
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    }
  };

  const handleSaveCategory = async (values) => {
    try {
      if (editingCategory) {
        await axios.put(`/api/radio/categories/${editingCategory.id}/`, values);
      } else {
        await axios.post('/api/radio/categories/', values);
      }
      setIsCategoryModalOpen(false);
      fetchCategories();
      fetchStations();
    } catch (error) {
      console.error('Error saving category:', error);
    }
  };

  const categoryColumns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Sort Order', dataIndex: 'sort_order', key: 'sort_order' },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button onClick={() => handleEditCategory(record)} size="small">Edit</Button>
          <Button danger onClick={() => handleDeleteCategory(record.id)} size="small">Delete</Button>
        </div>
      ),
    },
  ];

  const items = [
    {
      key: '1',
      label: 'Radio Stations',
      children: (
        <div>
          <div style={{ marginBottom: 16 }}>
            <Button type="primary" onClick={handleAddStation}>Add Station</Button>
          </div>
          <Table
            dataSource={stations}
            columns={stationColumns}
            rowKey="id"
            loading={loadingStations}
          />
        </div>
      ),
    },
    {
      key: '2',
      label: 'Categories (Genres)',
      children: (
        <div>
          <div style={{ marginBottom: 16 }}>
            <Button type="primary" onClick={handleAddCategory}>Add Category</Button>
          </div>
          <Table
            dataSource={categories}
            columns={categoryColumns}
            rowKey="id"
            loading={loadingCategories}
          />
        </div>
      ),
    },
  ];

  return (
    <div className="p-6">
      <Stack gap="xs" mb="lg">
        <Group gap="xs" align="center">
          <RadioIcon size={28} />
          <Title order={2} style={{ fontFamily: 'Outfit, Inter, sans-serif', fontWeight: 600 }}>
            Internet Radio
          </Title>
        </Group>
        <Text c="dimmed" size="sm">
          Manage your custom internet radio stations and genres
        </Text>
      </Stack>
      <div className="bg-white rounded-lg shadow mt-4 p-4">
        <Tabs defaultActiveKey="1" items={items} />
      </div>

      {/* Station Modal */}
      <Modal
        title={editingStation ? "Edit Radio Station" : "Add Radio Station"}
        open={isStationModalOpen}
        onOk={() => stationForm.submit()}
        onCancel={() => setIsStationModalOpen(false)}
      >
        <Form form={stationForm} layout="vertical" onFinish={handleSaveStation}>
          <Form.Item name="name" label="Station Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="stream_url" label="Stream URL" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="logo_url" label="Logo URL">
            <Input />
          </Form.Item>
          <Form.Item name="category" label="Category/Genre">
            <Select allowClear placeholder="Select a Category">
              {categories.map((cat) => (
                <Select.Option key={cat.id} value={cat.id}>{cat.name}</Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="sort_order" label="Sort Order">
            <Input type="number" />
          </Form.Item>
          <Form.Item name="is_active" label="Active" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>

      {/* Category Modal */}
      <Modal
        title={editingCategory ? "Edit Category" : "Add Category"}
        open={isCategoryModalOpen}
        onOk={() => categoryForm.submit()}
        onCancel={() => setIsCategoryModalOpen(false)}
      >
        <Form form={categoryForm} layout="vertical" onFinish={handleSaveCategory}>
          <Form.Item name="name" label="Category Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="sort_order" label="Sort Order">
            <Input type="number" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
