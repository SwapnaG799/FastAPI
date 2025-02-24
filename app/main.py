
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


print(settings.database_username)

#models.Base.metadata.create_all(bind=engine, checkfirst=True)


app = FastAPI() #create instance




# class Post(BaseModel):
#     title: str
#     content: str
#     published:bool = True
    #rating: Optional[int] = None
    
# while True :
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user = 'postgres',password = 'Admin',cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print("connecting database failed")
#         print("Error:",error)
#         time.sleep(5)

    
# my_posts= [{"title":"title of the post 1","content":"content of post1","id":1},{"title":"favouritefood",'content':"I like pizza",'id':2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#          if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return{'message':"welcome to api"}


