# Generated by Django 4.2.16 on 2024-12-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rpg", "0006_character_hp_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="character",
            name="enemies_defeated",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
