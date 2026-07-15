from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Fleet(Base):
    __tablename__ = "fleet"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    drivers = relationship("Driver", back_populates="fleet")


class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE")

    fleet_id = Column(Integer, ForeignKey("fleet.id"), nullable=True)

    fleet = relationship("Fleet", back_populates="drivers")

    cars = relationship("Car", secondary="booking", back_populates="drivers")

    bookings = relationship("Booking", back_populates="driver")


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(20), nullable=False)
    status = Column(String(20), default="AVAILABLE")

    drivers = relationship("Driver", secondary="booking", back_populates="cars")

    bookings = relationship("Booking", back_populates="car")


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)

    driver_id = Column(Integer, ForeignKey("driver.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)

    driver = relationship("Driver", back_populates="bookings")
    car = relationship("Car", back_populates="bookings")
