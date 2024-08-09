from fastapi import FastAPI
from app.db import db_chooser, metadata
from app import model
from app.Router import auth, task


app = FastAPI()

# Initialize db
def init_db():
    # Initialize auth.db
    auth_engine = db_chooser.get_engine('auth')
    model.Base.metadata.create_all(bind=auth_engine)
    #model.Base.metadata.drop_all(bind=engine)

    # Initialize task.db
    task_engine = db_chooser.get_engine('task')
    model.Base.metadata.create_all(bind=task_engine)

   
init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(task.router, prefix="/task", tags=["task"])


@app.get("/")
def home():
    return {"Home": "Update your awareness with us"}
