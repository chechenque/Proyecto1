import httpx

from logitrack.services.address_api_client import AddressApiClient
from logitrack.services.postal_code_worker import PostalCodeWorker


def test_postal_code_worker_emits_result() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
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
    worker = PostalCodeWorker(
        "01000",
        api_client.get_location_by_postal_code,
    )

    results: list[dict] = []
    errors: list[str] = []

    worker.finished.connect(results.append)
    worker.error.connect(errors.append)

    worker.run()

    assert errors == []
    assert results == [
        {
            "city": "Álvaro Obregón",
            "state": "Ciudad de México",
        }
    ]

    api_client.close()

def test_postal_code_worker_emits_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={"message": "Postal code not found"},
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    api_client = AddressApiClient(client)
    worker = PostalCodeWorker(
        "99999",
        api_client.get_location_by_postal_code,
    )

    results: list[dict] = []
    errors: list[str] = []

    worker.finished.connect(results.append)
    worker.error.connect(errors.append)

    worker.run()

    assert results == []
    assert len(errors) == 1
    assert "404 Not Found" in errors[0]
    assert "https://api.zippopotam.us/MX/99999" in errors[0]

    api_client.close()