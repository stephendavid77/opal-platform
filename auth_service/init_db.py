from auth_service.db.database import Base, engine
from auth_service.db.models import (  # Import models to ensure they are registered with Base
    RefreshToken,
    User,
)


def init_db():
    print("Initializing the auth_service database...")
    Base.metadata.create_all(bind=engine)
    print("auth_service database initialized successfully.")


if __name__ == "__main__":
    init_db()
