from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    avatar_url = Column(String)
    hashed_password = Column(String)
    role_id = Column(String, ForeignKey("roles.id"))
    created_date = Column(Integer)


class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    key = Column(String)
    name = Column(String)
    description = Column(String)
    created_date = Column(Integer)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, index=True)
    key = Column(String)
    name = Column(String)
    resource = Column(String)
    created_date = Column(Integer)


class RolePermission(Base):
    __table__ = "role_permission"

    id = Column(String, primary_key=True, index=True)
    role_id = Column(String, ForeignKey("roles.id"))
    permission = Column(String, ForeignKey("permissions.id"))


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
