# choices.py
from django.db import models


class Coins(models.TextChoices):
    AAVE = "AAVE", "Aave"
    BINANCE_COIN = "BNB", "Binance Coin"
    BITCOIN = "BTC", "Bitcoin"
    CARDANO = "ADA", "Cardano"
    CHAINLINK = "LINK", "Chainlink"
    COSMOS = "ATOM", "Cosmos"
    CRYPTOCOM_COIN = "CRO", "Crypto.com Coin"
    DOGECOIN = "DOGE", "Dogecoin"
    EOS = "EOS", "EOS"
    ETHEREUM = "ETH", "Ethereum"
    IOTA = "MIOTA", "IOTA"
    LITECOIN = "LTC", "Litecoin"
    MONERO = "XMR", "Monero"
    NEM = "XEM", "NEM"
    POLKADOT = "DOT", "Polkadot"
    SOLANA = "SOL", "Solana"
    STELLAR = "XLM", "Stellar"
    TETHER = "USDT", "Tether"
    TRON = "TRX", "TRON"
    USD_COIN = "USDC", "USD Coin"
    UNISWAP = "UNI", "Uniswap"
    WRAPPED_BITCOIN = "WBTC", "Wrapped Bitcoin"
    XRP = "XRP", "XRP"
