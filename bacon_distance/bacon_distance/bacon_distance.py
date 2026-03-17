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
    current_level_actors = {source_id}
    distance = 0

    while current_level_actors:
        distance += 1
        movies = (
            actors_db.query(ActorMovie.movie_id)
            .filter(ActorMovie.actor_id.in_(current_level_actors))
            .distinct()
            .all()
        )
        movie_ids = [movie.movie_id for movie in movies]
        co_actors = (
            actors_db.query(ActorMovie.actor_id)
            .filter(ActorMovie.movie_id.in_(movie_ids))
            .distinct()
            .all()
        )
        next_level_actors = {co_actor.actor_id for co_actor in co_actors}

        if target_id in next_level_actors:
            return distance
        next_level_actors -= visited
        visited |= next_level_actors

        current_level_actors = next_level_actors

    return -1
