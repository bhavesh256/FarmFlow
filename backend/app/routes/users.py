from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, request: Request):
    user = await user_service.create_user(request.app.state.db, data)

    if user is None:
        raise HTTPException(status_code=409, detail="User already exists")

    return user


@router.get("/", response_model=list[UserResponse])
async def list_users(request: Request):
    return await user_service.get_users(request.app.state.db)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str, request: Request):
    user = await user_service.get_user(request.app.state.db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def edit_user(user_id: str, data: UserUpdate, request: Request):
    user = await user_service.update_user(
        request.app.state.db,
        user_id,
        data.model_dump(exclude_unset=True),
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or no valid changes",
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: str, request: Request):
    deleted = await user_service.delete_user(
        request.app.state.db, user_id
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
