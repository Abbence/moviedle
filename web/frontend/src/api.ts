import axios from 'axios';
import { GameMovie, Guess, GameState, GiveUpResponse, GTMGameState, GTMGuessResult, API_BASE_URL } from './types';

const client = axios.create({
  baseURL: API_BASE_URL,
});

export const api = {
  getCandidators: () => 
    client.get<string[]>('/candidators'),

  // Moviedle endpoints
  moviedle: {
    startGame: (candidatorName?: string) =>
      client.post<GameState>('/moviedle/start_game', {}, {
        params: { candidator_name: candidatorName }
      }),

    findMovies: (searchTerm: string, limit: number = 10) =>
      client.get<GameMovie[]>(`/moviedle/find_movies/${encodeURIComponent(searchTerm)}`, {
        params: { limit }
      }),

    makeGuess: (titleId: string) =>
      client.post<Guess>(`/moviedle/make_guess/${titleId}`),

    giveUp: () =>
      client.post<GiveUpResponse>('/moviedle/give_up'),
  },

  // Guess the Movie endpoints
  gtm: {
    getCandidators: () =>
      client.get<string[]>('/guess_the_movie/candidators'),

    startGame: (slotCount: number = 5, candidatorName?: string) =>
      client.post<GTMGameState>('/guess_the_movie/start_game', {}, {
        params: { slot_count: slotCount, candidator_name: candidatorName }
      }),

    getState: () =>
      client.get<GTMGameState>('/guess_the_movie/state'),

    makeGuess: (slot: number, titleId: string) =>
      client.post<GTMGuessResult>(`/guess_the_movie/guess/${slot}/${titleId}`),

    findMovies: (searchTerm: string, limit: number = 10) =>
      client.get<GameMovie[]>(`/moviedle/find_movies/${encodeURIComponent(searchTerm)}`, {
        params: { limit }
      }),
  },
};
