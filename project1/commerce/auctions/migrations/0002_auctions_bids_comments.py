# Generated by Django 5.0.7 on 2024-07-19 10:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auctions",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=256)),
                ("image", models.URLField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("ER", "Electronics"),
                            ("FS", "Fashion"),
                            ("HM", "Home"),
                            ("EL", "Everything Else"),
                        ],
                        default="EL",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bids",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bid", models.DecimalField(decimal_places=2, max_digits=12)),
                ("enter_time", models.DateField(auto_now_add=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auctions.auctions",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bids",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(max_length=256)),
                ("enter_time", models.DateTimeField(auto_now_add=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item",
                        to="auctions.auctions",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
