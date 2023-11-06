from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

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

json_filename = "diet.json"

with open(json_filename, "r") as read_file:
    data = json.load(read_file)

app = FastAPI()

@app.get('/diet')
async def read_all_diet():
    return data['diet']

@app.get('/diet/{user_id}')
async def read_diet(user_id: str):
    for user_data in data['diet']:
        if user_data['user_id'] == user_id:
            return user_data
    raise HTTPException(status_code=404, detail=f'User not found')

@app.post('/diet')
async def add_diet(user: User):
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
async def update_diet(user_id: str, user: User):
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