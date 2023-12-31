# Generated by Django 4.2.4 on 2023-08-25 08:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Coin",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "symbol",
                    models.CharField(
                        choices=[
                            ("AAVE", "Aave"),
                            ("BNB", "Binance Coin"),
                            ("BTC", "Bitcoin"),
                            ("ADA", "Cardano"),
                            ("LINK", "Chainlink"),
                            ("ATOM", "Cosmos"),
                            ("CRO", "Crypto.com Coin"),
                            ("DOGE", "Dogecoin"),
                            ("EOS", "EOS"),
                            ("ETH", "Ethereum"),
                            ("MIOTA", "IOTA"),
                            ("LTC", "Litecoin"),
                            ("XMR", "Monero"),
                            ("XEM", "NEM"),
                            ("DOT", "Polkadot"),
                            ("SOL", "Solana"),
                            ("XLM", "Stellar"),
                            ("USDT", "Tether"),
                            ("TRX", "TRON"),
                            ("USDC", "USD Coin"),
                            ("UNI", "Uniswap"),
                            ("WBTC", "Wrapped Bitcoin"),
                            ("XRP", "XRP"),
                        ],
                        default="AAVE",
                        max_length=5,
                    ),
                ),
                ("date", models.DateField()),
                (
                    "high",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                (
                    "low",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                (
                    "open",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
                (
                    "close",
                    models.DecimalField(decimal_places=8, default=0, max_digits=18),
                ),
            ],
        ),
    ]
