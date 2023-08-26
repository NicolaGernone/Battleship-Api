# test_views.py
import pytest
from django.urls import reverse
from rest_framework import status

from tests.domain.factories import CoinFactory


@pytest.mark.django_db
def test_close_values_valid(api_client):
    coin = CoinFactory()
    url = (
        reverse("api:coin-close-values")
        + f'?symbol={coin.symbol}&date={coin.date.strftime("%Y-%m-%d")}'
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_close_values_missing_parameters(api_client):
    url = reverse("api:coin-close-values")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_close_values_coin_not_found(api_client):
    coin = CoinFactory()
    url = (
        reverse("api:coin-close-values")
        + f'?symbol=XLM&date={coin.date.strftime("%Y-%m-%d")}'
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test_views.py (continued)
@pytest.mark.django_db
def test_max_profit_valid(api_client):
    coin = CoinFactory()
    url = (
        reverse("api:coin-max-profit")
        + f'?symbol={coin.symbol}&start_date={coin.date.strftime("%Y-%m-%d")}&end_date={coin.date.strftime("%Y-%m-%d")}'
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_max_profit_missing_parameters(api_client):
    url = reverse("api:coin-max-profit")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test_views.py (continued)
@pytest.mark.django_db
def test_list_names_symbols_valid(api_client):
    url = reverse("api:coin-list-names-symbols")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_coin_valid(api_client):
    url = reverse('api:coin-list')
    data = {
        'name': 'Bitcoin',
        'symbol': 'BTC',
        'date': '2023-08-25T00:00:00Z',
        'high': '48000.00',
        'low': '42000.00',
        'open': '45000.00',
        'close': '46000.00',
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    
@pytest.mark.django_db
def test_list_all_coins(api_client):
    CoinFactory.create_batch(5)
    url = reverse('api:coin-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5

