import os
import sys

# Add the project root to PYTHONPATH
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from shared.database_base.database import SessionLocal
from shared.database_base.models.user import User
from auth_service.utils.password_hasher import hash_password

def create_superuser(username, email, password):
    db = SessionLocal()
    try:
        hashed_password = hash_password(password)
        superuser = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            roles="super_user" # Set role to super_user
        )
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        print(f"Superuser '{username}' created successfully with ID: {superuser.id}")
    except Exception as e:
        db.rollback()
        print(f"Error creating superuser: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Replace with your desired superuser credentials
    create_superuser("admin", "stephensrinivasan@gmail.com", "admin")