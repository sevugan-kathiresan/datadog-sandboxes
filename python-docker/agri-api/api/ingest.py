from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
import logging

#local imports from my code
from ..db import get_db
from ..schemas import ReadingIn, ReadingOut
from ..models import Hub, HubReading

#Instanticate the logger
logger = logging.getLogger(__name__) #__name__ corresponds to the respective module name likea place holder



# function that acts as a simulator for fecting hub details from the external service
async def fetch_hub_details(serial_number: str):
    return {
        "manufacturer": "Temp Manufacturer",
        "installed_on": datetime.now()
    }



# function to verify if the Hub exists if not create it
async def get_or_create_hub(serial_number: str, db: AsyncSession):
    #verify if the hub exists
    result = await db.execute(select(Hub).where(Hub.serial_number == serial_number))
    hub = result.scalar_one_or_none()

    if hub:
        return hub
    
    # if not we need to create the hub
    hub_details = await fetch_hub_details(serial_number)
    new_hub = Hub(
        serial_number=serial_number,
        manufacturer = hub_details.get("manufacturer"),
        installed_on = hub_details.get("installed_on")
    )

    db.add(new_hub)

    try:
        await db.commit()
        await db.refresh(new_hub) # If there was no error and the commit was successful then we are refreshing the committted data which also fetches back the generated primary key from DB
    except IntegrityError:
        await db.rollback()
        result = await db.execute(select(Hub).where(Hub.serial_number == serial_number))
        existing =  result.scalar_one_or_none()

        if existing == None:
            raise

        return existing

    except SQLAlchemyError:
        await db.rollback()
        raise
    
    return new_hub





#Instantiate the router
router = APIRouter()

@router.post("/ingest", response_model=ReadingOut)
async def ingest_reading(payload: ReadingIn, db: AsyncSession = Depends(get_db)):
    # Step 1 - Get or create the HUB for this Serial number
    try:
        hub = await get_or_create_hub(payload.serial_number)
    
    except IntegrityError as e:
        error_message = str(e.orig) if e.orif  else str(e)
        logger.error("IntegrityError while creating hub: %s", error_message)

        raise HTTPException(status_code=400, detail="Hub already exists or violates a database constraint") from e
    
    except SQLAlchemyError as e:
        error_message = str(e)
        logger.error("SQL Alchemy error happened: %s", error_message)

        raise HTTPException(status_code=500, detail="Internal Server Error Happened while processing the Hub") from e


        
