from collections import deque
import json
from typing import Dict, List, Optional, TypedDict


class ACTORS_DB_TYPE(TypedDict):
    actor_to_movies: Dict[str, List[str]]
    movie_to_actors: Dict[str, List[str]]
    actors: Dict[str, str]
    movies: Dict[str, str]


def main():
    """method to get actor names from the user and print the distance of the actor to kevin bacon"""
    actors_db: ACTORS_DB_TYPE = load_db("actors_db.json")
    kevin_id = get_actor_id(actors_db, "Kevin Bacon")
    assert kevin_id

    while True:
        name = input("Enter actor name: ")
        actor_id = get_actor_id(actors_db, name)
        if actor_id is None:
            print("actor not found")
            continue
        print(actors_distance(actors_db, kevin_id, actor_id))


def load_db(file_path: str) -> ACTORS_DB_TYPE:
    """loads the db from the given file"""
    with open(file_path) as actors_db_file:
        return json.load(actors_db_file)


def get_actor_id(actors_db: ACTORS_DB_TYPE, name: str) -> Optional[str]:
    """get the id of an actor from his name"""
    for key, value in actors_db["actors"].items():
        if value == name:
            return key
    return None


def actors_distance(actors_db: ACTORS_DB_TYPE, source_id: str, target_id: str) -> int:
    """get the distance between the two actors"""
    if source_id == target_id:
        return 0

    actor_to_movies: Dict[str, List[str]] = actors_db["actor_to_movies"]
    movie_to_actors: Dict[str, List[str]] = actors_db["movie_to_actors"]

    visited = set([source_id])
    queue = deque([(source_id, 0)])

    while queue:
        actor, dist = queue.popleft()
        for movie in actor_to_movies[actor]:
            for co_actor in movie_to_actors[movie]:
                if co_actor == target_id:
                    return dist + 1
                if co_actor not in visited:
                    visited.add(co_actor)
                    queue.append((co_actor, dist + 1))
    return -1


if __name__ == "__main__":
    main()
