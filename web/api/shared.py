from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session

from model.database.mappings import MoviesFinal
from model.game_movie import GameMovie
from model.candidation_types import CherryPickedCandidator, ICandidationType, Pop500K_HasHungarianTitleCandidator, TopNVoteCountCandidator


CANDIDATORS: dict[str, ICandidationType] = {
    "top10": TopNVoteCountCandidator(10),
    "top30": TopNVoteCountCandidator(30),
    "pop500": Pop500K_HasHungarianTitleCandidator(),
    "Autós": CherryPickedCandidator([
      "tt2369135", # Need for speed
      "tt0095016", # Die hard
      "tt0183869", # Taxi 2
      "tt0317219", # Cars
      "tt0232500", # The Fast and the Furious
      "tt16311594", # F1: The Movie
      "tt1950186", # Ford v Ferrari
      "tt0463985", # Tokyo Drift
      "tt8289930", # Formula 1: Drive to survive
      "tt1628033", # Top Gear
      "tt3890160", # Baby Driver
      "tt1979320", # Rush
      "tt0412080", # The world's fastest Indian
    ]),
    "Chick-flick": CherryPickedCandidator([
      "tt1041829", # The proposal
      "tt1093908", # Confessions of a shopaholic
      "tt0337563", # 13 going on 30
      "tt0458352", # The Devil Wears Prada
      "tt0247638", # The Princess Diaries
      "tt0251127", # How to Lose a Guy in 10 Days
      "tt0250494", # Legally Blonde
      "tt1478338", # Bridesmaids
      "tt0112697", # Clueless
      "tt0322330", # Freaky Friday
      "tt0475293", # High School Musical
      "tt2325989", # Teen Beach Movie
      "tt1055366", # Camp Rock
      "tt2171665", # Violetta
      "tt5189554", # Soy Luna
      "tt0147800", # 10 Things I Hate About You
      "tt0343660", # 50 First Dates
      "tt1981677", # Pitch Perfect
      "tt1405406", # The Vampire Diaries
      "tt0852713", # The House Bunny
      "tt6432466", # Moxie
    ]),
    "Akciófilmek": CherryPickedCandidator([
      "tt1489889", # Central Intelligence
      "tt0465494", # Hitman
      "tt1959563", # The Hitman's Bodyguard
      "tt2239822", # Valerian and the City of a Thousand Planets
      "tt1670345", # Now You See Me
      "tt2463208", # The Adam Project
      "tt0107290", # Jurassic Park
      "tt1464335", # Uncharted
      "tt1365519", # Tomb Raider
      "tt0160127", # Charlie's Angels
      "tt0119654", # Men in Black
      "tt1618434", # Murder Mystery
      "tt0087538", # The Karate Kid
      "tt0087332", # Ghostbusters
      "tt0112442", # Bad Boys
      "tt1386697", # Suicide Squad
      "tt0903624", # The Hobbit: An Unexpected Journey
      "tt14948432", # Red One
      "tt1318514", # Rise of the Planet of the Apes
      "tt0437086", # Alita: Battle Angel
      "tt0083658", # Blade Runner
      "tt0266697", # Kill Bill: Vol. 1
      "tt0320691", # Underworld
      "tt0117060", # Mission: Impossible
      "tt2015381", # Guardians of the Galaxy
      "tt0078748", # Alien
    ]),
    "Utópia": CherryPickedCandidator([
      "tt0120804", # Resident Evil
      "tt1392170", # The Hunger Games
      "tt1790864", # The Maze Runner
      "tt1840309", # Divergent
      "tt1520211", # The Walking Dead

    ]),
    "Szuperhős film": CherryPickedCandidator([
      "tt1270797", # Venom
      "tt0448115", # Shazam!
      "tt1431045", # Deadpool
      "tt0371746", # Iron Man
      "tt0800080", # The Incredible Hulk
      "tt0800369", # Thor
      "tt0848228", # The Avengers
      # BATMAN ??
      "tt0103923", # Captain America
      "tt3480822", # Black Widow
      "tt0145487", # Spider-Man
      "tt9140554", # Loki
      "tt1825683", # Black Panther
      "tt3498820", # Captain America: Civil War
      "tt2975590", # Batman v Superman: Dawn of Justice
      "tt1477834", # Aquaman
      "tt1211837", # Doctor Strange
      "tt0478970", # Ant-Man
      "tt4154664", # Captain Marvel
      "tt10857164", # Ms. Marvel ((series))
    ]),
    "Magyar": CherryPickedCandidator([
      "tt4964310", # Kincsem
      "tt0175383", # Barátok közt
      "tt0446224", # Jóban rosszban
      "tt5871080", # A viszkis
      "tt0131636", # Vuk
      "tt0133307", # A kockásfülű nyúl
      "tt0065067", # A tanú
      "tt0112545", # Vacak - a hetedik testvér
      "tt0136650", # A Mézga család különös kalandjai
      "tt0179955", # Macskafogó
      "tt0167595", # Frakk, a macskák réme
      "tt14466284", # Futni mentem
      "tt27811640", # Véletlenül írtam egy könyvet
      "tt29344974", # Hogyan tudnék élni nélküled?
      "tt0487841", # Mazsola és Tádé
      "tt0166931", # Pom-Pom meséi
    ]),
    "Animációs": CherryPickedCandidator([
      "tt0114709", # Toy Story
      "tt0892769", # How to Train Your Dragon
      "tt0441773", # Kung Fu Panda
      "tt0266543", # Finding Nemo
      "tt1482459", # The Lorax
      "tt0110357", # The Lion King
      # Elements?
      "tt2096673", # Inside Out
      "tt1323594", # Despicable Me
      "tt2293640", # Minions
      "tt3040964", # The Jungle Book
      "tt2948356", # Zootopia
      "tt0138749", # The Road to El Dorado
      "tt6718170", # The Super Mario Bros. Movie
      "tt0126029", # Shrek
      "tt0448694", # Csizmás, a kandúr
      "tt0472181", # The Smurfs
      "tt0910970", # WALL·E
      "tt0952640", # Alvin and the Chipmunks
      "tt0268380", # Ice Age
      "tt0848537", # Epic
      "tt1446192", # Rise of the Guardians
      "tt3874544", # The Boss Baby
      "tt2380307", # Coco
      "tt0206512", # SpongeBob SquarePants
      "tt14205554", # KPop Demon Hunters
      "tt0382932", # Ratatouille
      "tt2709768", # The Secret Life of Pets
      "tt0094469", # Garfield and Friends
      "tt0317705", # The Incredibles
      "tt2709692", # The Grinch (2018)
      "tt0119282", # Hercules
      "tt11655566", # Lilo & Stitch
      "tt0032910", # Pinocchio
      "tt1001526", # Megamind
      "tt1490017", # The Lego Movie
      "tt3014284", # The Lego Ninjago Movie
      "tt2245084", # Big Hero 6
      "tt2953050", # Encanto
      "tt0121164", # Corpse Bride
      "tt0131613", # Teenage Mutant Ninja Turtles (1987)
      "tt2580046", # Miraculous: Tales of Ladybug & Cat Noir
      "tt0844471", # Cloudy with a Chance of Meatballs
      "tt1049413", # Up
      "tt1142977", # Frankenweenie
      "tt0837562", # Hotel Transylvania
      "tt1217213", # Secret of the Wings
      "tt0366548", # Happy Feet
      "tt1860353", # Turbo
      "tt1911658", # Penguins of Madagascar
    ]),
    "Hercegnő (GPT xd)": CherryPickedCandidator(["tt0042332","tt0029583","tt0053285","tt3521164","tt2294629","tt1217209","tt0780521","tt0103639","tt0398286","tt0097757","tt0120762","tt0114148","tt0101414","tt0247638","tt5109280","tt1587310","tt0043274"]),
    "debug_starwars": CherryPickedCandidator("tt0076759"), # Star Wars: Episode IV - A New Hope
}

def get_candidator_names() -> list[str]:
    return list(CANDIDATORS.keys())

def get_candidator(name: str) -> ICandidationType | None:
    return CANDIDATORS.get(name)

def get_default_candidator_name() -> str:
    return next(iter(CANDIDATORS.keys()))


def find_movies(db: Session, title_search_text: str, limit: int = 10) -> list[GameMovie]:
    search_term = f"%{title_search_text.lower()}%"
    
    stmt = select(MoviesFinal).where(
        or_(
            MoviesFinal.primarytitle.ilike(search_term),
            MoviesFinal.originaltitle.ilike(search_term),
            MoviesFinal.hungariantitle.ilike(search_term)
        )
    ).order_by(
        MoviesFinal.imdbVoteCount.desc().nulls_last()
    ).limit(limit)
    
    results = db.execute(stmt).scalars().all()
    return [GameMovie.from_moviesfinal(movie) for movie in results]


def get_movie_by_id(db: Session, title_id: str) -> GameMovie | None:
    stmt = select(MoviesFinal).where(MoviesFinal.titleid == title_id).limit(1)
    result = db.execute(stmt).scalar_one_or_none()
    
    if result:
        return GameMovie.from_moviesfinal(result)
    return None
