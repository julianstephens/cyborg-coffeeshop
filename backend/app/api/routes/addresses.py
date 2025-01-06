import uuid
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Security, status

from app.api.deps import (
    SessionDep,
    get_current_user,
)
from app.models import (
    Address,
    AddressCreate,
    AddressPublic,
    AddressUpdate,
    Message,
    User,
)

router = APIRouter()


@router.get(
    "/{id}",
    dependencies=[Security(User, scopes=["address"])],
    response_model=AddressPublic,
)
def read_address(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get address by ID.
    """
    address = session.get(Address, id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


@router.post("", response_model=AddressPublic)
def create_address(
    *,
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["address:write"])],
    address_in: AddressCreate,
) -> Any:
    """
    Create new address.
    """
    address = Address.model_validate(
        address_in, update={"customer_id": current_user.id}
    )
    session.add(address)
    session.commit()
    session.refresh(address)
    return address


@router.put("/{id}", response_model=AddressPublic)
def update_address(
    *,
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["address:write"])],
    id: uuid.UUID,
    address_in: AddressUpdate,
) -> Any:
    """
    Update an address.
    """
    address = session.get(Address, id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    if not current_user.is_superuser and (address.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    update_dict = address_in.model_dump(exclude_unset=True)
    address.sqlmodel_update(update_dict)
    session.add(address)
    session.commit()
    session.refresh(address)
    return address


@router.delete("/{id}")
def delete_address(
    session: SessionDep,
    current_user: Annotated[User, Security(get_current_user, scopes=["address:write"])],
    id: uuid.UUID,
) -> Message:
    """
    Delete an address.
    """
    address = session.get(Address, id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    if not current_user.is_superuser and (address.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    session.delete(address)
    session.commit()
    return Message(message="Address deleted successfully")
