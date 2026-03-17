import pandas as pd
import json

NAMES_URL = "https://datasets.imdbws.com/name.basics.tsv.gz"
PRINCIPALS_URL = "https://datasets.imdbws.com/title.principals.tsv.gz"
BASICS_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"

principals = pd.read_csv(
    PRINCIPALS_URL,
    sep="\t",
    compression="gzip",
    usecols=["tconst", "nconst", "category"],
)
principals = principals[principals["category"].isin(["actor", "actress"])]

names = pd.read_csv(
    NAMES_URL, sep="\t", compression="gzip", usecols=["nconst", "primaryName"]
)

basics = pd.read_csv(
    BASICS_URL,
    sep="\t",
    compression="gzip",
    usecols=["tconst", "primaryTitle", "titleType"],
)
basics = basics[basics["titleType"] == "movie"]

cast = principals.merge(names, on="nconst", how="left")
cast = cast.merge(basics, on="tconst", how="left")
cast = cast[["tconst", "nconst", "primaryTitle", "primaryName"]]

actor_to_movies = cast.groupby("nconst")["tconst"].apply(list).to_dict()
movie_to_actors = cast.groupby("tconst")["nconst"].apply(list).to_dict()

actor_names = names.set_index("nconst")["primaryName"].to_dict()
movie_names = basics.set_index("tconst")["primaryTitle"].to_dict()

dataset = {
    "actor_to_movies": actor_to_movies,
    "movie_to_actors": movie_to_actors,
    "actors": actor_names,
    "movies": movie_names,
}

with open("actors_db.json", "w", encoding="utf-8") as actors_db:
    json.dump(dataset, actors_db, indent=2)
