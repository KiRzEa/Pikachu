import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const gameAPI = {
  createGame: async (level = 1) => {
    const response = await api.post('/game/new', null, { params: { level } });
    return response.data;
  },

  getGame: async (gameId) => {
    const response = await api.get(`/game/${gameId}`);
    return response.data;
  },

  makeMove: async (gameId, pos1, pos2) => {
    const response = await api.post(`/game/${gameId}/move`, {
      pos1,
      pos2,
    });
    return response.data;
  },

  getHint: async (gameId) => {
    const response = await api.post(`/game/${gameId}/hint`);
    return response.data;
  },

  shuffleBoard: async (gameId) => {
    const response = await api.post(`/game/${gameId}/shuffle`);
    return response.data;
  },

  updateTime: async (gameId, secondsElapsed) => {
    const response = await api.post(`/game/${gameId}/time`, null, {
      params: { seconds_elapsed: secondsElapsed },
    });
    return response.data;
  },
};

export default api;
