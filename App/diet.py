from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
############################################
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
############################################

json_filename = "diet.json"

user_filename = "userfile.json"


with open(json_filename, "r") as read_file:
    data = json.load(read_file)

with open(user_filename, "r") as read_file:
    datauser = json.load(read_file)

app = FastAPI()

############################################
SECRET_KEY = "tugaststnix"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
############################################

class User(BaseModel):
    user_id: str
    name: str
    weight_kg: float
    height_cm: int
    age: int
    gender: str
    activity_level: str
    goal: str
    recommended_diet: dict

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class UserPass(BaseModel):
    username: str
    password: str



##########################################

#########################################

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    user_found = False
    for user_item in datauser['testuser']:
        if user_item['username']==username:
            user_found = True
            return user_item
    
    if not user_found:
        return None

def create_access_token(data: dict or None, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception
    

#########################################
@app.get('/diet')
async def read_all_diet(current_user: TokenData = Depends(get_current_user)):
    return data['diet']

@app.get('/diet/{user_id}')
async def read_diet(user_id: str, current_user: TokenData = Depends(get_current_user)):
    for user_data in data['diet']:
        if user_data['user_id'] == user_id:
            return user_data
    raise HTTPException(status_code=404, detail=f'User not found')

@app.post('/diet')
async def add_diet(user: User, current_user: TokenData = Depends(get_current_user)):
    user_dict = user.dict()
    user_found = False
    for user_data in data['diet']:
        if user_data['user_id'] == user_dict['user_id']:
            user_found = True
            return f"User with ID {user_dict['user_id']} already exists."
    if not user_found:
        data['diet'].append(user_dict)
        with open(json_filename, "w") as write_file:
            json.dump(data, write_file)
        return user_dict
    raise HTTPException(status_code=404, detail=f'User not found')

@app.put('/diet/{user_id}')
async def update_diet(user_id: str, user: User, current_user: TokenData = Depends(get_current_user)):
    user_dict = user.dict()
    user_found = False
    for diet_idx, user_data in enumerate(data['diet']):
        if user_data['user_id'] == user_id:
            user_found = True
            data['diet'][diet_idx] = user_dict
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            return "User updated"
    if not user_found:
        raise HTTPException(status_code=404, detail=f'User not found')

@app.delete('/diet/{user_id}')
async def delete_diet(user_id: str):
    user_found = False
    for diet_idx, user_data in enumerate(data['diet']):
        if user_data['user_id'] == user_id:
            user_found = True
            data['diet'].pop(diet_idx)
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            return "User deleted"
    if not user_found:
        raise HTTPException(status_code=404, detail=f'User not found')
    
#######################################################
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user or not verify_password(form_data.password, user['password']):        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
############################################################
@app.post("/register")
async def register_user(user: UserPass):
    # Check if the username is already taken
    for user_item in datauser['testuser']:
        if user_item['username'] == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before storing it
    hashed_password = pwd_context.hash(user.password)

    # Add the new user to the datauser dictionary
    datauser['testuser'].append({
        "username": user.username,
        "password": hashed_password
    })

    # Save the updated user data to the file
    with open(user_filename, "w") as write_file:
        json.dump(datauser, write_file)

    return {"message": "User registered successfully"}


@app.post("/signin", response_model=Token)
async def sign_in(user: UserPass):
    user_data = get_user(user.username)
    if user_data and verify_password(user.password, user_data['password']):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )