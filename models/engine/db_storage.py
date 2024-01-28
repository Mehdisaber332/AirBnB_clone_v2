#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv


class DBStorage:
    """ DBStorage to map tables in MySQLdb"""
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage objects """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of all instances """
        if not self.__session:
            self.reload()

        instances = {}
        if cls:
            for obj in self.__session.query(cls):
                instances[f"{obj.__class__.__name__}.{obj.id}"] = obj
        else:
            cls_names = [State, City, User, Place, Review, Amenity]
            for cls in cls_names:
                for obj in self.__session.query(cls):
                    instances[f"{obj.__class__.__name__}.{obj.id}"] = obj

        return instances

    def new(self, obj):
        """ add the object to the current database session  """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """
        create all tables in the database and create the current
        database session
        """

        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
        self.__session.close()

    def close(self):
        """close session"""
        self.__session.close
