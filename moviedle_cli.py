from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from model.candidation_types import TopNVoteCountCandidator
from model.moviedle_game import MoviedleGame

if __name__ == "__main__":
  import config
  engine = create_engine(config.DATABASE_URL, echo=config.DATABASE_VERBOSE_LOGGING)

  with Session(engine) as session:
    game = MoviedleGame(TopNVoteCountCandidator(10), session)

    while not game.isGameOver:
      try:
        user_input = input("Enter your guessed movie titleid (or Ctrl+D to quit): ").strip()
      except EOFError:
        print("Exiting the game.")
        break

      try:
        guess = game.make_guess(user_input)
        print("Guess relations:")
        for attr, relation in guess.guess_relations_dict.items():
          print(f"\t{attr}: {relation.value}")
      except Exception as e:
        print(f"Error: {e}")

    if game.isGameWon:
      print("Congratulations! You've guessed the correct movie!")
      print("Last guessed movie:", game.guesses[-1].movie.primarytitle, "(", game.guesses[-1].movie.titleid, ")")
      print("Candidate movie:", game.candidateMovie.primarytitle, "(", game.candidateMovie.titleid, ")")