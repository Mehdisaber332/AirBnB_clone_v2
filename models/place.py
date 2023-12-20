#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Table  # noqa

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """

    if getenv("HBNB_TYPE_STORAGE") == "db":

        __tablename__ = "places"

        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        amenities = relationship("Amenity", backref="place_amenities",
                                 secondary='place_amenity', viewonly=False)
        reviews = relationship(
            "Review", backref="places", cascade="all, delete")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def reviews(self):
        """
        Returns the list of Review instances with place_id equals to the
        current Place.id => It will be the FileStorage relationship between
        Place and Review
        """
        from models import storage
        reviews = []
        for review in storage.all("Review").values():
            if review.place_id == self.id:
                reviews.append(review)
        return reviews

    @property
    def amenities(self):
        """
        returns the list of Amenity instances based on the attribute
        amenity_ids that contains all Amenity.id linked to the Place
        """
        from models import storage
        amenities = []
        for amenity in storage.all("Amenity").values():
            if amenity.place_id == self.id:
                amenities.append(amenity)
        return amenities

    @amenities.setter
    def amenities(self, obj=None):
        """ Adding an Amenity.id to the attribute amenity_ids """
        if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
            self.amenity_ids.append(obj.id)
