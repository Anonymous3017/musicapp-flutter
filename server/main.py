from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup")
def signup_user(user: UserCreate):
    # extract the data thats comming from the request
    print(user.name)
    print(user.email)
    print(user.password)
    # check if user already exists in db
    # add user to db
    return {"message": "User created successfully"}