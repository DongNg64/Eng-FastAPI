from fastapi import Depends
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.orm import Session


from .database import Base, get_db


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(100), unique=True)
    # phone = Column(String(11))
    # avatar_url = Column(String(255))
    hashed_password = Column(String(255))
    type = Column(String(50))
    role_id = Column(String(50), ForeignKey("roles.id"))

    role = relationship("Role")

    @property
    def role_name(self, db: Session = Depends(get_db)):
        return self.role.key


class Role(Base):
    __tablename__ = "roles"

    id = Column(String(50), primary_key=True, index=True)
    key = Column(String(255))
    name = Column(String(255))
    description = Column(String(255))


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String(50), primary_key=True, index=True)
    key = Column(String(255))
    name = Column(String(255))
    resource = Column(String(500))

    role_permissions = relationship("RolePermission", back_populates="permissions")


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(String(50), primary_key=True, index=True)
    role_id = Column(String(50), ForeignKey("roles.id"))
    permission_id = Column(String(50), ForeignKey("permissions.id"))

    # @property
    # def permissions(self):
    permissions = relationship("Permission", back_populates="role_permissions")
        


    # permissions = relationship("Permission", back_populates="items")


class Redis(Base):
    __tablename__ = "redis"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(String(50))
    permissions = Column(Text)


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
