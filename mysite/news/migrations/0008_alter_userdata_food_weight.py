# Generated by Django 3.2 on 2021-05-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20210529_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='food_weight',
            field=models.IntegerField(default='55', null=True, verbose_name='Удельный вес сферы "Питание", %'),
        ),
    ]