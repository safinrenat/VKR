# Generated by Django 3.2 on 2021-05-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_userdata_food_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='fun_weight',
            field=models.IntegerField(default=15, null=True, verbose_name='Удельный вес сферы "Развлечения", %'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='sport_weight',
            field=models.IntegerField(default=10, null=True, verbose_name='Удельный вес сферы "Спорт", %'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='transport_weight',
            field=models.IntegerField(default=20, null=True, verbose_name='Удельный вес сферы "Транспорт", %'),
        ),
    ]
