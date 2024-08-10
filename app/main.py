from fastapi import FastAPI
from app.db import db_chooser, metadata
from app import model
from app.Router import auth, task


app = FastAPI()

# Initialize db
def init_db():
    # Initialize db
    engine = db_chooser.get_engine()
    model.Base.metadata.create_all(bind=engine)
    # model.Base.metadata.drop_all(bind=engine)

   
init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(task.router, prefix="/task", tags=["task"])


@app.get("/")
def home():
    return {"Home": "Update your awareness with us"}
