import axios from 'axios';
import { GameMovie, Guess, GameState, GiveUpResponse, API_BASE_URL } from './types';

const client = axios.create({
  baseURL: API_BASE_URL,
});

export const api = {
  getCandidators: () => 
    client.get<string[]>('/candidators'),

  startGame: (candidatorName?: string) =>
    client.post<GameState>('/start_game', {}, {
      params: { candidator_name: candidatorName }
    }),

  findMovies: (searchTerm: string, limit: number = 10) =>
    client.get<GameMovie[]>(`/find_movies/${encodeURIComponent(searchTerm)}`, {
      params: { limit }
    }),

  makeGuess: (titleId: string) =>
    client.post<Guess>(`/make_guess/${titleId}`),

  giveUp: () =>
    client.post<GiveUpResponse>('/give_up'),
};
