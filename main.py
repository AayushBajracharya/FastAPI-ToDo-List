from datetime import datetime
from fastapi import FastAPI, APIRouter, HTTPException
from config import collection
from database.schemas import all_tasks
from database.models import Todo
from bson.objectid import ObjectId
app = FastAPI()
router = APIRouter()

@router.get("/")
async def get_all_todos():
    data = collection.find({"is_deleted":False})
    return all_tasks(data)

@router.get("/{task_id}")
async def get_task_by_id(task_id: str):
    try:
        id = ObjectId(task_id)
        task = collection.find_one({"_id": id, "is_deleted": False})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task["_id"] = str(task["_id"]) 
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

@router.post("/")
async def create_task(new_task: Todo):
    try:
        resp = collection.insert_one(dict(new_task))
        return {
            "status_code": 200, "id":str(resp.inserted_id)
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured{e}")
    
@router.put("/")
async def update_task(task_id:str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id":id, "is_deleted":False})
        if not existing_doc:
            return HTTPException(status_code=404, detail=f"Task does not exists")
        updated_task.updated_at = datetime.timestamp(datetime.now())
        resp = collection.update_one({"_id":id}, {"$set":dict(updated_task)})
        return {"status":200, "message": "Task Updated Successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")

@router.delete("/{task_id}")
async def delete_task(task_id:str):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id":id, "is_deleted":False})
        if not existing_doc:
            return HTTPException(status_code=404, detail=f"Task does not exists")
        resp = collection.update_one({"_id":id}, {"$set":{"is_deleted":True}})
        return {"status":200, "message": "Task Deleted Successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")


app.include_router(router)