# Moviedle Frontend

NOTE: The entire frontend was vibe-coded

A modern React frontend for the Moviedle guessing game.

## Project Structure

```
src/
├── components/          # React components
│   ├── AttributeCell.tsx    # Color-coded attribute display
│   ├── MovieRow.tsx         # Movie display row (reusable for guesses & search)
│   ├── SearchBar.tsx        # Interactive search with dropdown
│   ├── GuessList.tsx        # Scrollable guesses list
│   └── Game.tsx             # Main game orchestrator
├── types.ts            # TypeScript interfaces & configuration
├── api.ts              # API client (axios)
├── App.tsx             # App root
└── main.tsx            # Entry point
```

## Key Features

### Component Design
- **Extensible**: New movie attributes automatically appear in display rows via `MOVIE_DISPLAY_FIELDS`
- **Reusable MovieRow**: Single component for both search results and guess display
- **Color-coded feedback**: Visual indicators for each guess relation type

### Search
- Debounced API calls (300ms) for responsive search
- Dropdown with movie suggestions
- Click to guess

### Game Flow
- Select candidator and start game
- Search and guess movies
- Real-time guess feedback with attribute comparisons
- Win/lose states with candidate reveal

## Setup & Development

```bash
cd web/frontend
npm install
npm run dev
```

Visit `http://localhost:3000` (proxies to backend at `http://localhost:8000`)

## Build

```bash
npm run build
```

## Architecture Notes

### State Management
- Uses React hooks (`useState`, `useEffect`) for local state
- Frontend maintains: guesses, tries, game state
- Backend maintains: candidate movie (private)

### API Contract
- `/candidators` - Get available candidators
- `/start_game?candidator_name=X` - Start new game
- `/find_movies/{searchTerm}` - Search with debounce
- `/make_guess/{titleid}` - Submit guess
- `/give_up` - Reveal candidate and end game

### Styling
- CSS Modules for component isolation
- Responsive design (desktop, tablet, mobile)
- Accessible colors and focus states

## Extensibility

To add new movie attributes:
1. Add to `GameMovie` interface in backend (`game_movie.py`)
2. Add to `MOVIE_DISPLAY_FIELDS` in `types.ts`
3. Add comparison logic to `Guess.evaluate_guess()` in backend
4. Done! The UI automatically displays the new field
