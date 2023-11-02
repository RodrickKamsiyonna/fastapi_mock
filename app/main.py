from typing import Optional,List
from fastapi import FastAPI, Response,status,HTTPException
import psycopg
from psycopg.rows import dict_row
import time
from  .import schemas,config

from fastapi.middleware.cors import CORSMiddleware




app  =  FastAPI()
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings =  config.Settings()
print(settings.db_password)
while True:
     try: 
         conn = psycopg.connect(f'host={settings.db_host} dbname={settings.db_name} user={settings.db_username} password={settings.db_password}',
                                row_factory= dict_row
                                )
         cursor =  conn.cursor()
         print("DataBase Connection was Sucessfull!")
         break;
     except Exception as error: 
        print("Connection failed")
        print("Error", error)
        time.sleep(2)

my_posts =   [{"title:": "title of posts", "content":"A post", "id":1},
              {"title:": "Pizza is the way forward", "content":"I like pizza", "id":2}
              ]
@app.get("/")
def read_root():
    return {"message": "Welcome to my Program this is good"}

@app.get("/posts",response_model= List[schemas.Post])
def get_posts(limit: int = 5 ):
    cursor.execute("""SELECT * FROM posts LIMIT %s""",(str(limit),))
    posts = cursor.fetchall()
    cursor.row_factory
    return  posts

"""
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message":"Sucessfully created post"}
"""
@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model= schemas.Post)
def create_posts(post: schemas.PostCreate):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published)) 
    new_post =  cursor.fetchone()
    conn.commit()
    return new_post 

@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""",(str(id),))
    post = cursor.fetchone()
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"""Post with an id of {id} not found""")
    return  post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
     cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""",(str(id),))
     post =  cursor.fetchone()
     conn.commit()
     if not post: 
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"""Post with an id of {id} not found""")
     return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model= schemas.Post)
def change_post(id:int, post:schemas.PostCreate):
     cursor.execute("""UPDATE posts SET title = (%s), content =  %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published, str(id)))
     post =  cursor.fetchone()
     conn.commit()
     if not post: 
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"""Post with an id of {id} not found""")
     return  post


