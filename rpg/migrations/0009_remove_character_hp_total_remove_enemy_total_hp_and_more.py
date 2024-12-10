# Generated by Django 4.2.16 on 2024-12-10 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rpg", "0008_achievement_timestamp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="character",
            name="hp_total",
        ),
        migrations.RemoveField(
            model_name="enemy",
            name="total_hp",
        ),
        migrations.CreateModel(
            name="Battle",
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
                ("enemy_hp", models.IntegerField()),
                ("player_hp", models.IntegerField()),
                (
                    "char",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rpg.character"
                    ),
                ),
                (
                    "enemy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rpg.enemy"
                    ),
                ),
            ],
        ),
    ]
