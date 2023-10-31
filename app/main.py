from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params  import Body
from pydantic  import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
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

class Post(BaseModel):
    title: str
    content: str
    published:bool = True 
while True:
     try: 
         conn = psycopg.connect('host=localhost dbname=fastapi user=postgres  password=Kamsi&mark',
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

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    cursor.row_factory
    return  {"data": posts}

"""
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message":"Sucessfully created post"}
"""
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published)) 
    new_post =  cursor.fetchone()
    conn.commit()
    return{"data" :new_post} 

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""",(str(id),))
    post = cursor.fetchone()
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"""Post with an id of {id} not found""")
    return  

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
     cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""",(str(id),))
     post =  cursor.fetchone()
     conn.commit()
     if not post: 
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"""Post with an id of {id} not found""")
     return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def change_post(id:int, post:Post):
     cursor.execute("""UPDATE posts SET title = (%s), content =  %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published, str(id)))
     post =  cursor.fetchone()
     conn.commit()
     if not post: 
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"""Post with an id of {id} not found""")
     return  post


