from collections import deque
from typing import Dict, List, Optional, TypedDict
from sqlalchemy.orm.session import Session
from bacon_distance.database import Actor, ActorMovie


class ACTORS_DB_TYPE(TypedDict):
    actor_to_movies: Dict[str, List[str]]
    movie_to_actors: Dict[str, List[str]]
    actors: Dict[str, str]
    movies: Dict[str, str]


def get_actor_id(actors_db: Session, name: str) -> Optional[str]:
    """get the id of an actor from his name"""
    actor = actors_db.query(Actor).filter(Actor.primaryName == name).first()
    if actor is not None:
        return actor.nconst
    return None


def get_actor_movies(actors_db: Session, actor_id: str) -> List[ActorMovie]:
    return actors_db.query(ActorMovie).filter(ActorMovie.actor_id == actor_id).all()


def get_movie_actors(actors_db: Session, movie_id: str) -> List[ActorMovie]:
    return actors_db.query(ActorMovie).filter(ActorMovie.movie_id == movie_id).all()


def actors_distance(actors_db: Session, source_id: str, target_id: str) -> int:
    """get the distance between the two actors"""
    if source_id == target_id:
        return 0

    visited = set([source_id])
    queue = deque([(source_id, 0)])

    while queue:
        actor, dist = queue.popleft()

        for movie in get_actor_movies(actors_db, actor):
            for co_actor in get_movie_actors(actors_db, movie.movie_id):
                if co_actor.actor_id == target_id:
                    return dist + 1
                if co_actor.actor_id not in visited:
                    visited.add(co_actor.actor_id)
                    queue.append((co_actor.actor_id, dist + 1))
    return -1
