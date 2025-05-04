from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status

from .dependencies import SessionDep
from .schemas import PartCreate, PartResponse, PartFilters
from .service import create_part, get_part, list_parts
from .exceptions import PartAlreadyExists, PartCreationError, PartNotFound


router = APIRouter(prefix="/parts", tags=["parts"])


@router.get("", response_model=list[PartResponse])
async def list_parts_handler(
    session: SessionDep,
    filters: Annotated[PartFilters, Query()]
):
    """ List parts. """
    parts = await list_parts(session=session, filters=filters)
    return parts


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
