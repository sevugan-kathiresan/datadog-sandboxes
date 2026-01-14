# SQL Alchemy model definitions need to match with our table definitions
from sqlalchemy import (Integer, String, Date, Numeric, DateTime, ForeignKey, func)
from sqlalchemy.orm import (relationship, DeclarativeBase, Mapped, mapped_column)
from datetime import datetime, date


class Base(DeclarativeBase):
    pass

class Hub(Base):
    __tablename__ = "hubs"
    hub_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    serial_number: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    manufacturer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    installed_on: Mapped[date | None] = mapped_column(Date, nullable=True)

    #relationship between the two ORM classes Hub and HubReading, this has no effect on creating the Database constraints
    readings: Mapped[list["HubReading"]] = relationship(back_populates="hub")

class HubReading(Base):
    __tablename__ = "hubreadings"
    reading_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hub_id: Mapped[int] = mapped_column(Integer, ForeignKey("hubs.hub_id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    temperature: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    humidity: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    soil_moisture: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    #relationship
    hub: Mapped["Hub"] = relationship(back_populates="readings")