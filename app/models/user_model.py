from sqlalchemy import Column, Integer, String, LargeBinary
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Integer, default=0)
    profile_image = Column(LargeBinary, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
