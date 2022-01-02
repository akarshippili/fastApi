from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import post, user, auth, vote
from fastapi import FastAPI, Depends
from . import models
from. database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Headers
options = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=options,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# try:
#     conn = psycopg2.connect(host='localhost', database='fastApi',
#                             user='postgres', password='akarsh', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("sucessfully connected")
# except Exception as err:
#     print(err)


# all_posts = [
#     {"title": "First post", "content": "This is my first post",
#         "published": True, "id": 1},
#     {"title": "Second post", "content": "This is my second post",
#         "published": False, "id": 2}
# ]


# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": "sucesses", "data": posts}

@app.get("/")
async def root():
    return {"message": "welcome to the root dude !!!!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
