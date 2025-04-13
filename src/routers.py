import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .schemas import PartCreate, PartResponse
from .service import create_part, get_part
from .exceptions import PartAlreadyExists, PartCreationError, PartNotFound

logger = logging.getLogger(__name__)


SessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/parts", tags=["parts"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PartResponse)
async def create_part_handler(part: PartCreate, session: SessionDep):
    """ Creates a new part in the database. """
    try:
        return await create_part(part, session)
    except PartAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except PartCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{part_id}", response_model=PartResponse)
async def get_part_handler(part_id: int, session: SessionDep):
    """ Gets a part by ID. """
    try:
        return await get_part(part_id, session)
    except PartNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
