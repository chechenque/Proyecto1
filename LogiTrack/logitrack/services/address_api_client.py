import httpx


class AddressApiClient:
    """Cliente HTTP para consultar información de códigos postales."""

    BASE_URL = "https://api.zippopotam.us/MX"

    def __init__(
        self,
        client: httpx.Client | None = None,
    ) -> None:
        self.client = client or httpx.Client(
            timeout=5.0,
        )

    def get_location_by_postal_code(
            self,
            postal_code: str,
    ) -> dict[str, str]:
        """Obtiene ciudad y estado a partir de un código postal."""

        self._validate_postal_code(postal_code)

        try:
            response = self.client.get(
                f"{self.BASE_URL}/{postal_code}"
            )
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise ConnectionError(
                "No fue posible conectarse al servicio de códigos postales."
            ) from exc

        data = response.json()
        place = data["places"][0]

        return {
            "city": place["place name"],
            "state": place["state"],
        }

    def close(self) -> None:
        """Cierra el cliente HTTP."""

        self.client.close()

    def _validate_postal_code(self, postal_code: str) -> None:
        """Valida el formato de un código postal mexicano."""

        if not postal_code.isdigit() or len(postal_code) != 5:
            raise ValueError(
                "El código postal debe contener 5 dígitos."
            )