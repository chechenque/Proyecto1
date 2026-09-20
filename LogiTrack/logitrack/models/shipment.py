from pydantic import BaseModel, ConfigDict, Field


class Shipment(BaseModel):
    """Modelo validado para representar un envío."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: int | None = None

    recipient: str = Field(
        min_length=1,
        max_length=100,
    )

    address: str = Field(
        min_length=1,
        max_length=250,
    )

    shipment_type: str = Field(
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        min_length=1,
        max_length=50,
    )