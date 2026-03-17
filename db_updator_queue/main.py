import json
from typing import Dict, List, TypedDict
import pika, sys, os
from database import Actor, ActorMovie, Movie, get_db


class NEW_MOVIES_JSON_TYPE(TypedDict):
    PrimaryTitle: str
    Tconst: str
    Actors: Dict[str, str]


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    db_session = get_db()

    channel.queue_declare(
        queue="new_movies",
        durable=True,
        arguments={"x-queue-type": "quorum"},
    )

    def callback(ch, method, properties, body):
        data: NEW_MOVIES_JSON_TYPE = json.loads(body)
        if (
            db_session.query(Movie).filter(Movie.tconst == data["Tconst"]).first()
            is None
        ):
            db_session.add(
                Movie(tconst=data["Tconst"], primaryTitle=data["PrimaryTitle"])
            )
        else:
            ch.basic_publish(
                exchange="",
                routing_key="error_queue",
                body=json.dumps(
                    {"original": body.decode(), "error": "movie already exists in db"}
                ),
            )

        actors: List[Actor] = []
        for nconst, primaryName in data["Actors"].items():
            if db_session.query(Actor).filter(Actor.nconst == nconst).first() is None:
                actors.append(Actor(nconst=nconst, primaryName=primaryName))
        db_session.add_all(actors)

        actor_movie: List[ActorMovie] = []
        for nconst in data["Actors"].keys():
            if not db_session.get(ActorMovie, (nconst, data["Tconst"])):
                actor_movie.append(ActorMovie(actor_id=nconst, movie_id=data["Tconst"]))
        db_session.add_all(actor_movie)

        db_session.commit()

    channel.basic_consume(
        queue="new_movies",
        on_message_callback=callback,
        auto_ack=True,
    )

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
