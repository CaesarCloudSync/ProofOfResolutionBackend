"""Resolutions router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.dependencies import get_resolution_service
from models.resolutions.requests.ResolutionCreate import ResolutionCreate
from models.resolutions.responses.CreateResolutionResponse import CreateResolutionResponse
from models.resolutions.responses.GetAllResolutionsResponse import GetAllResolutionsResponse
from models.resolutions.responses.GetResolutionResponse import GetResolutionResponse
from models.resolutions.responses.ImmutableResponse import ImmutableResponse
from services.ResolutionService import ResolutionService

router = APIRouter(prefix="/resolutions", tags=["Resolutions"])


@router.post("/", response_model=CreateResolutionResponse, status_code=status.HTTP_201_CREATED)
def create_resolution(
    resolution: ResolutionCreate,
    service: ResolutionService = Depends(get_resolution_service),
) -> CreateResolutionResponse:
    """Mine a block and permanently lock a new year's resolution onto the chain."""
    return service.create_resolution(resolution)


@router.get("/", response_model=GetAllResolutionsResponse)
def get_all_resolutions(
    service: ResolutionService = Depends(get_resolution_service),
) -> GetAllResolutionsResponse:
    """Return every resolution stored on the chain."""
    resolutions = service.get_all_resolutions()
    return GetAllResolutionsResponse(
        message=f"Found {len(resolutions)} resolution(s) locked on the blockchain.",
        resolutions=resolutions,
        total=len(resolutions),
    )


@router.get("/{goal_id}", response_model=GetResolutionResponse)
def get_resolution(
    goal_id: str,
    service: ResolutionService = Depends(get_resolution_service),
) -> GetResolutionResponse:
    """Fetch a single resolution by its ID."""
    resolution = service.get_resolution(goal_id)
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resolution '{goal_id}' not found.",
        )
    return GetResolutionResponse(message="Resolution retrieved.", resolution=resolution)


@router.put("/{goal_id}", response_model=ImmutableResponse)
def update_resolution(goal_id: str) -> ImmutableResponse:
    """Nicely tell the user that the blockchain gods forbid mutations."""
    return ImmutableResponse(
        message="✋ Nice try! You thought you could change your resolution... but the blockchain gods said NO.",
        tip="Resolutions are forever. Consider adding a new one instead of running from the old one 😄",
        goal_id=goal_id,
    )


@router.delete("/{goal_id}", response_model=ImmutableResponse)
def delete_resolution(goal_id: str) -> ImmutableResponse:
    """Nicely tell the user that the blockchain gods forbid deletions."""
    return ImmutableResponse(
        message="🔒 Nice try! The blockchain never forgets – and neither do we.",
        tip="You can't outrun your resolutions. The chain remembers all 💪",
        goal_id=goal_id,
    )