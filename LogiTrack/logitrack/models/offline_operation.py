from pydantic import BaseModel, ConfigDict, Field


class OfflineOperation(BaseModel):
    """Representa una operación pendiente de sincronización."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    id: int | None = None
    operation: str = Field(
        min_length=1,
        max_length=50,
    )
    payload: str = Field(
        min_length=1,
    )
    status: str = Field(
        min_length=1,
        max_length=30,
    )