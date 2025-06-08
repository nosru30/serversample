from app.db_models import Base
from app.db import engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
