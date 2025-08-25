from OpalSuite.shared.database_base.database import Base, engine
from OpalSuite.shared.database_base.models.user import (  # noqa: F401; Import User model to ensure it's registered with Base
    User,
)


def init_db():
    print("Initializing the shared OpalSuite database...")
    Base.metadata.create_all(bind=engine)
    print("Shared OpalSuite database initialized successfully.")


if __name__ == "__main__":
    init_db()
