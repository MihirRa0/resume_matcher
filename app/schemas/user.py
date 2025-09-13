from pydantic import BaseModel,EmailStr

#shared properties
class UserBase(BaseModel):
    email:EmailStr


# signup
class UserCreate(UserBase):
    password:str

# Properties to return to client (never include password)
class User(UserBase):
    id:int
    is_active :bool
    class Config:
        from_attributes = True