import pytest
import requests


class BookingApi:
    """API-объект (POM) для сервиса Restful Booker."""

    def __init__(self, base_url="https://restful-booker.herokuapp.com"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_token(self, username="admin", password="password123"):
        response = requests.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password},
            headers=self.headers,
        )
        return response.json()["token"]

    def create_booking(self, booking):
        return requests.post(
            f"{self.base_url}/booking", json=booking, headers=self.headers
        )

    def get_booking(self, booking_id):
        return requests.get(
            f"{self.base_url}/booking/{booking_id}", headers=self.headers
        )

    def partial_update_booking(self, booking_id, data, token=None):
        headers = dict(self.headers)
        if token:
            headers["Cookie"] = f"token={token}"
        return requests.patch(
            f"{self.base_url}/booking/{booking_id}", json=data, headers=headers
        )



api = BookingApi()

BOOKING = {
    "firstname": "Nadya",
    "lastname": "Tester",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
    "additionalneeds": "Breakfast",
}


@pytest.fixture
def booking_id():
    """Создаёт бронь и возвращает её id."""
    response = api.create_booking(BOOKING)
    assert response.status_code == 200
    return response.json()["bookingid"]


def test_create_booking():
    """Создание брони."""
    response = api.create_booking(BOOKING)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["bookingid"], int)
    assert body["booking"] == BOOKING


def test_get_created_booking(booking_id):
    """Созданную бронь можно получить по id."""
    response = api.get_booking(booking_id)

    assert response.status_code == 200
    assert response.json() == BOOKING


def test_partial_update_booking(booking_id):
    """Частичное изменение брони (PATCH)."""
    token = api.get_token()
    changes = {"firstname": "Anna", "totalprice": 300}

    response = api.partial_update_booking(booking_id, changes, token)

    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "Anna"
    assert body["totalprice"] == 300
    # остальные поля не изменились
    assert body["lastname"] == BOOKING["lastname"]
    assert body["bookingdates"] == BOOKING["bookingdates"]


def test_partial_update_without_token(booking_id):
    """Негативный сценарий: изменение без токена запрещено."""
    response = api.partial_update_booking(booking_id, {"firstname": "Hacker"})

    assert response.status_code == 403
    # бронь осталась прежней
    assert api.get_booking(booking_id).json()["firstname"] == BOOKING["firstname"]


def test_get_nonexistent_booking():
    """Негативный сценарий: несуществующая бронь возвращает 404."""
    response = api.get_booking(999999999)

    assert response.status_code == 404
