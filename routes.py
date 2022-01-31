from fastapi import APIRouter,HTTPException
import models,schemas
from config import conn,db,coll
from bson import ObjectId
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security=HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user=APIRouter()

def get_password_hash(password):
    return pwd_context.hash(password)

@user.get("/")
def find_all_users():
    db_user=schemas.serializeList(coll.find())
    if db_user==[]:
        raise HTTPException(status_code=404,detail="No user found!!")
    return db_user

@user.get("/{id}")
def find_user_by_id(id):
    db_user=schemas.serializeList(coll.find({"_id":ObjectId(id)}))
    if db_user==[]:
        raise HTTPException(status_code=404,detail="User not found!!")
    return db_user

@user.post("/")
def create_user(user:models.UserCreate):
    hash_pwd=get_password_hash(user.password)
    user.password=hash_pwd
    newUser=coll.insert_one(dict(user))
    return schemas.serializeDict(coll.find_one({"_id":newUser.inserted_id}))

@user.put("/{id}")
def update_user(id,user:models.UserUpdate):
    db_user = schemas.serializeList(coll.find({"_id": ObjectId(id)}))
    if db_user==[]:
        raise HTTPException(status_code=404,detail="User not found!!")
    if user.name!=None:
        coll.find_one_and_update({"_id":ObjectId(id)},
                                        {
                                            "$set": {"name":user.name}
                                        })
    if user.email!=None:
        coll.find_one_and_update({"_id":ObjectId(id)},
                                        {
                                            "$set": {"email":user.email}
                                        })
    # coll.find_one_and_update({"_id":ObjectId(id)},
    #                                     {
    #                                         "$set":dict(user)
    #                                     })
    return schemas.serializeDict(coll.find_one({"_id":ObjectId(id)}))

@user.delete("/{id}")
def delete_user(id:str):
    # if id != ObjectId:
    #     raise HTTPException(status_code=422,detail="Invalid Object Id!!")
    db_user=schemas.serializeList(coll.find({"_id":ObjectId(id)}))
    if db_user ==[]:
        raise HTTPException(status_code=404,detail="User not found!!")
    schemas.serializeDict(coll.find_one_and_delete({"_id":ObjectId(id)}))
    return "Successfully Deleted!!"
