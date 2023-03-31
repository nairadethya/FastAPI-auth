from sqlalchemy import (
    LargeBinary,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint
)

from db_initializer import Base
import bcrypt 

class User(Base):
    __tablename__ = "Users"
    email = Column(String(225), nullable=False, unique=True)
    id = Column(Integer, nullable=False, primary_key=True)
    hashed_password = Column(LargeBinary, nullable=False)
    full_name = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self) -> str:
        return "<User {full_name}!r>".format(full_name=self.full_name)

    @staticmethod
    def hash_password(password) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool: 
        return{
            "access_token":jwt.encode(
                {"full_name": self.full_name, "email": self.email},
                "ApplicationSecretKey"
            )
        }