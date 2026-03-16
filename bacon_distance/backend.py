from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from bacon_distance.bacon_distance import (
    ACTORS_DB_TYPE,
    actors_distance,
    get_actor_id,
    load_db,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

actors_db: ACTORS_DB_TYPE = load_db("actors_db.json")
kevin_id = get_actor_id(actors_db, "Kevin Bacon")


@app.get("/bacon-distance/{actor_name}")
def get_bacon_distance(actor_name: str):
    """return the bacon distance to the given actor"""
    actor_id = get_actor_id(actors_db, actor_name)
    if actor_id == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="actor name not found"
        )
    if kevin_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="kevin bacon not found",
        )
    return {"actors_distance": actors_distance(actors_db, kevin_id, actor_id)}
