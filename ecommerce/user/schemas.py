from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    name: constr(min_length=2, max_length=50, to_lower=True)
    email: EmailStr
    password: str
    
    class Config:
         schema_extra = {
            "example": {
                "name": "John Cina",
                "email": "johncina@gmail.com",
                "password": "password"
            }
        }
    
class OutUser(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "test",
                "email": "test@gmail.com"
            }
        }
        