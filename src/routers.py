from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status

from .dependencies import SessionDep
from .schemas import PartCreate, PartPartialUpdate, PartResponse, PartFilters, PartUpdate
from .service import create_part, delete_part, get_part, list_parts, update_part
from .exceptions import PartAlreadyExists, PartCreationError, PartDeletionError, PartNotFound, PartUpdateError


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
    
async def try_update_part(
        part_id: int,
        part: PartUpdate | PartPartialUpdate,
        session: SessionDep,
        partial: bool
    ):
    try:
        return await update_part(part_id, part, session, partial)
    except PartNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PartAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except PartUpdateError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{part_id}", response_model=PartResponse)
async def put_part_handler(part_id: int, part: PartUpdate, session: SessionDep):
    return try_update_part(part_id, part, session, partial=False)


@router.patch("/{part_id}", response_model=PartResponse)
async def patch_part_handler(part_id: int, part: PartPartialUpdate, session: SessionDep):
    return try_update_part(part_id, part, session, partial=True)
    

@router.delete("/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_part_handler(part_id: int, session: SessionDep):
    """ Deletes a part by ID. """
    try:
        await delete_part(part_id, session)
    except PartNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PartDeletionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
