# Generated by Django 4.2.16 on 2024-12-10 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rpg", "0005_enemy_total_hp"),
    ]

    operations = [
        migrations.AddField(
            model_name="character",
            name="hp_total",
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
