from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import db, model, schemas
from app.dependencies import get_current_user, get_current_active_user, get_current_active_admin, get_current_active_guest, verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency for admin role
def admin_required(user: schemas.User = Depends(get_current_active_admin)):
    return user

# Dependency for user role
def user_required(user: schemas.User = Depends(get_current_active_user)):
    return user

# Dependency for guest role
def guest_required(user: schemas.User = Depends(get_current_active_guest)):
    return user

@router.post("/tasks/{user_id}", response_model=schemas.Task)
def create_task(user_id: int, task: schemas.TaskBase, db: Session = Depends(db.get_db()), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    print(f"Token payload: {payload}")  # Debugging line
    
    if "admin" not in payload.get("roles", []):
        raise HTTPException(status_code=403, detail="Permission denied")

    db_task = model.Task(
        title=task.title,
        description=task.description,
        owner_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db()), user: schemas.User = Depends(guest_required)):
    return db.query(model.Task).offset(skip).limit(limit).all()

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskBase, db: Session = Depends(db.get_db()), user: schemas.User = Depends(user_required)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(db.get_db()), user: schemas.User = Depends(admin_required)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return db_task
