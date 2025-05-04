import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc, select


from .models import Part
from .schemas import PartCreate, PartFilters
from .exceptions import PartAlreadyExists, PartCreationError, PartDeletionError, PartNotFound, PartUpdateError


logger = logging.getLogger(__name__)


async def list_parts(session: AsyncSession, filters: PartFilters) -> list[Part]:
    logger.info("Fetching all parts with filters: %s", filters)
    stmt = select(Part)

    # Filtering
    if filters.part_number:
        stmt = stmt.where(Part.part_number.ilike(f"%{filters.part_number}%"))
    if filters.description:
        stmt = stmt.where(Part.description.ilike(f"%{filters.description}%"))
    if filters.quantity is not None:
        stmt = stmt.where(Part.quantity == filters.quantity)

    # Ordering
    order_by = getattr(Part, filters.order_by)
    sort = asc if filters.sort == "asc" else desc
    stmt = stmt.order_by(sort(order_by))

    # Pagination
    stmt = stmt.limit(filters.limit).offset(filters.offset)
    
    # Execution
    result = await session.execute(stmt)
    parts = result.scalars().all()
    logger.info("Fetched %d parts", len(parts))
    return parts


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


async def update_part(part_id: int, part: PartCreate, session: AsyncSession, partial=False) -> Part:
    logger.info("Updating part with id: %s", part_id)
    existing_part = await get_part(part_id, session)
    
    for key, value in part.model_dump(exclude_unset=partial).items():
        setattr(existing_part, key, value)

    try:
        await session.commit()
        await session.refresh(existing_part)
    except IntegrityError as e:
        await session.rollback()
        logger.warning("Integrity error while updating part '%s': %s", part.part_number, str(e))
        raise PartAlreadyExists(f"Part with part_number '{part.part_number}' already exists")
    except Exception as e:
        await session.rollback()
        logger.exception("Unexpected error while updating part '%s': %s", part.part_number, str(e))
        raise PartUpdateError("An unexpected error occurred while updating the part")
    
    logger.info("Part updated successfully: id=%s part_number=%s",
                existing_part.id, existing_part.part_number)
    return existing_part



async def delete_part(part_id: int, session: AsyncSession) -> None:
    logger.info("Deleting part with id: %s", part_id)
    part = await get_part(part_id, session)
    
    try:
        await session.delete(part)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.exception("Unexpected error while deleting part '%s': %s", part.part_number, str(e))
        raise PartDeletionError("An unexpected error occurred while deleting the part")
    
    logger.info("Part deleted successfully: id=%s part_number=%s",
                part.id, part.part_number)

