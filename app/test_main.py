import pytest
from unittest import mock
from unittest.mock import MagicMock
from datetime import date

from app.main import outdated_products


@pytest.fixture()
def products_list() -> list:
    return [
        {
            "name": "salmon",
            "expiration_date": date(2024, 10, 30),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": date(2024, 10, 31),
            "price": 120
        }
    ]


@pytest.mark.parametrize(
    "today_date, expected_result",
    [
        pytest.param(
            date(2024, 10, 31),
            ["salmon"],
            id="should return only `salmon`, "
               "which has expired for current date"
        ),
        pytest.param(
            date(2024, 10, 29),
            [],
            id="should return `[]`, "
               "because `salmon` and `chicken` not expired for current date"
        ),
        pytest.param(
            date(2024, 11, 1),
            ["salmon", "chicken"],
            id="should return [`salmon`, `chicken`], "
               "because they are expired for current date"
        )
    ]
)
@mock.patch("app.main.datetime")
def test_returns_from_outdated_products_func(
        mocked_today: MagicMock,
        products_list: list[dict],
        today_date: str,
        expected_result: list
) -> None:
    mocked_today.date.today.return_value = today_date
    assert outdated_products(products_list) == expected_result
