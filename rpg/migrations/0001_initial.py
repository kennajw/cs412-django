# Generated by Django 4.2.16 on 2024-11-22 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("img", models.ImageField(upload_to="")),
                ("level", models.IntegerField()),
                ("hp", models.IntegerField()),
                ("mp", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("type", models.TextField()),
                ("img", models.ImageField(upload_to="")),
                ("description", models.TextField()),
                ("price", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Inventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "char",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rpg.character"
                    ),
                ),
                (
                    "itm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rpg.item"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Achievement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "char",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rpg.character"
                    ),
                ),
            ],
        ),
    ]