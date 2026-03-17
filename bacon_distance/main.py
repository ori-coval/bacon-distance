from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session

from bacon_distance.bacon_distance import actors_distance, get_actor_id
from bacon_distance.database import get_db

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{actor_name}")
def get_id(actor_name: str, actors_db: Session = Depends(get_db)):
    """return the bacon distance to the given actor"""
    return {"id": get_actor_id(actors_db, actor_name)}


@app.get("/bacon-distance/{actor_name}")
def get_bacon_distance(actor_name: str, actors_db: Session = Depends(get_db)):
    """return the bacon distance to the given actor"""
    kevin_id = get_actor_id(actors_db, "Kevin Bacon")
    if kevin_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="kevin bacon not found",
        )
    actor_id = get_actor_id(actors_db, actor_name)
    if actor_id == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="actor name not found"
        )

    return {"actors_distance": actors_distance(actors_db, kevin_id, actor_id)}
