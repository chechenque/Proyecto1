import httpx

from logitrack.services.address_api_client import AddressApiClient


def test_get_location_by_postal_code() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "post code": "01000",
                "country": "Mexico",
                "places": [
                    {
                        "place name": "Álvaro Obregón",
                        "state": "Ciudad de México",
                    }
                ],
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    api_client = AddressApiClient(client)

    result = api_client.get_location_by_postal_code("01000")

    assert result["city"] == "Álvaro Obregón"
    assert result["state"] == "Ciudad de México"

    api_client.close()

def test_get_location_by_postal_code_raises_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={"message": "Postal code not found"},
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    api_client = AddressApiClient(client)

    try:
        api_client.get_location_by_postal_code("99999")
    except httpx.HTTPStatusError as exc:
        assert exc.response.status_code == 404
    else:
        raise AssertionError(
            "Se esperaba una excepción HTTPStatusError"
        )
    finally:
        api_client.close()

def test_get_location_by_postal_code_rejects_invalid_format() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(
            "La API no debería ser llamada."
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    api_client = AddressApiClient(client)

    try:
        api_client.get_location_by_postal_code("1234")
    except ValueError as exc:
        assert str(exc) == (
            "El código postal debe contener 5 dígitos."
        )
    else:
        raise AssertionError(
            "Se esperaba una excepción ValueError"
        )
    finally:
        api_client.close()

def test_get_location_by_postal_code_raises_connection_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(
            "No internet connection",
            request=request,
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    api_client = AddressApiClient(client)

    try:
        api_client.get_location_by_postal_code("01000")
    except ConnectionError as exc:
        assert (
            str(exc)
            == "No fue posible conectarse al servicio de códigos postales."
        )
    else:
        raise AssertionError("Se esperaba ConnectionError")