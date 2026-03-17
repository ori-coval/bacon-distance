import pandas as pd
from bacon_distance import database
from bacon_distance.database import Actor, ActorMovie, Movie
from sqlalchemy.orm import Session

NAMES_URL = "name.basics.tsv.gz"
PRINCIPALS_URL = "title.principals.tsv.gz"
BASICS_URL = "title.basics.tsv.gz"

session: Session = database.create_db()

principals = pd.read_csv(
    PRINCIPALS_URL,
    sep="\t",
    compression="gzip",
    usecols=["tconst", "nconst", "category"],
    nrows=10000000,
)
principals = principals[principals["category"].isin(["actor", "actress"])]

names = pd.read_csv(
    NAMES_URL,
    sep="\t",
    compression="gzip",
    usecols=["nconst", "primaryName"],
    nrows=10000000,
)

basics = pd.read_csv(
    BASICS_URL,
    sep="\t",
    compression="gzip",
    usecols=["tconst", "primaryTitle", "titleType"],
    nrows=10000000,
)
basics = basics[basics["titleType"] == "movie"]

cast = principals.merge(names, on="nconst", how="left")
cast = cast.merge(basics, on="tconst", how="left")
cast = cast[["tconst", "nconst", "primaryTitle", "primaryName"]]
cast = cast.dropna(subset=["primaryName", "primaryTitle"]).drop_duplicates()

actors = [
    Actor(nconst=row["nconst"], primaryName=row["primaryName"])
    for _, row in cast[["nconst", "primaryName"]].drop_duplicates().iterrows()
]
session.bulk_save_objects(actors)

movies = [
    Movie(tconst=row["tconst"], primaryTitle=row["primaryTitle"])
    for _, row in cast[["tconst", "primaryTitle"]].drop_duplicates().iterrows()
]
session.bulk_save_objects(movies)
session.commit()

rows = [
    {"actor_id": row["nconst"], "movie_id": row["tconst"]}
    for _, row in cast.drop_duplicates().iterrows()
]

session.bulk_insert_mappings(ActorMovie, rows)  # type: ignore

session.commit()
session.close()
