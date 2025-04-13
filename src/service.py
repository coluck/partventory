import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from .models import Part
from .schemas import PartCreate
from .exceptions import PartAlreadyExists, PartCreationError, PartNotFound


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)



async def create_part(part: PartCreate, session: AsyncSession) -> Part:
    logger.info("Creating new part: %s", part.part_number)
    new_part = Part(**part.model_dump())
    session.add(new_part)

    try:
        await session.commit()
        await session.refresh(new_part)
    except IntegrityError as e:
        await session.rollback()
        logger.warning("Integrity error while creating part '%s': %s", part.part_number, str(e))
        raise PartAlreadyExists(f"Part with part_number '{part.part_number}' already exists")
    except Exception as e:
        await session.rollback()
        logger.exception("Unexpected error while creating part '%s': %s", part.part_number, str(e))
        raise PartCreationError("An unexpected error occurred while creating the part")
    
    logger.info("Part created successfully: id=%s part_number=%s",
                new_part.id, new_part.part_number)
    return new_part


async def get_part(part_id: int, session: AsyncSession) -> Part:
    logger.info("Fetching part with id: %s", part_id)
    part = await session.get(Part, part_id)
    if not part:
        logger.warning("Part with id '%s' not found", part_id)
        raise PartNotFound(f"Part with id '{part_id}' not found")
    
    return part
