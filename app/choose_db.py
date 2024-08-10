from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class ChooseDB:
    def __init__(self):
        self.db_url = "sqlite:///./project_management.db"

    def get_engine(self):
        return create_engine(self.db_url, connect_args={"check_same_thread": False})

    def get_session_local(self):
        engine = self.get_engine()
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Global instance
db_chooser = ChooseDB()
