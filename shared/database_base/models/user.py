from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String

from OpalSuite.shared.database_base.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    first_name = Column(String(80), nullable=True)
    last_name = Column(String(80), nullable=True)

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f"<User {self.username}>"
