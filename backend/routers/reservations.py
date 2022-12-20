from fastapi import APIRouter, File

from schemas import reservation

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/xlsx-file/", response_model=reservation.ReservationOut)
async def create_reservation_xlsx_file(file: bytes = File(summary="The file which reservations data")):
    """The file which reservations data.

    Args:
        file: File with xlsx extension.
    
    Returns:
        Return list of reservations created based on input file.

    """
    return {"file_size": len(file)}
