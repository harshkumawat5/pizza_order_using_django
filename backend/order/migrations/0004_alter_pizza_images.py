# Generated by Django 4.2.1 on 2023-06-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_cart_instamojo_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pizza",
            name="images",
            field=models.ImageField(upload_to="uploads/images"),
        ),
    ]
