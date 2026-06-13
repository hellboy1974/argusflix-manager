import { create } from 'zustand';
import api from '../api';

const useCustomPlaylistsStore = create((set) => ({
  playlists: [],
  isLoading: false,
  error: null,
  fetchPlaylists: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/api/v1/output/playlists/');
      set({ playlists: response.data?.results || response.data || [], isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
}));

export default useCustomPlaylistsStore;
