# Pydantic Data Models -> describe how data is validated, parsed, and serialized in your API

from typing import Optional, Annotated
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

# Create a special type to match the Numeric(10, 2) in Postgress
DecimalType = Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

#------------Hub Schemas---------------------
class HubBase(BaseModel):
    # hub_id will be created by DB automatically as a primary key
    serial_number: str
    manufacturer: Optional[str] = None
    installed_on: Optional[date] = None

    #You only need this on schemas that FastAPI will fill using a SQLAlchemy ORM object.
    model_config = ConfigDict(from_attributes=True)


#------------Readingds Schema---------------------
class ReadingIn(BaseModel):
    serial_number: str
    timestamp: datetime
    temperature: DecimalType
    humidity: DecimalType
    soil_moisture: DecimalType


class ReadingOut(BaseModel):
    reading_id: int
    hub_serial_number: str
    timestamp: datetime
    temperature: DecimalType
    humidity: DecimalType
    soil_moisture: DecimalType

    model_config = ConfigDict(from_attributes=True)