#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from os import getenv
# from dotenv import load_dotenv

# This line brings all environment variables from .env into os.environ
# load_dotenv()


class State(BaseModel, Base):
    """ State class """

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "states"

        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""

        @property
        def cities(self):
            list_city = []
            allcities = models.storage.all(City).values()
            for city in allcities:
                if city.state_id == self.id:
                    list_city.append(city)
            return list_city
