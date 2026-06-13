import { create } from 'zustand';
import api from '../api';

const useMediaServersStore = create((set) => ({
  servers: [],
  isLoading: false,
  error: null,
  fetchServers: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/api/v1/mediaservers/');
      set({ servers: response.data?.results || response.data || [], isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
}));

export default useMediaServersStore;
