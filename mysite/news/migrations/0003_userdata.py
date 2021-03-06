# Generated by Django 3.2 on 2021-05-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_spheres_weight_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('family_number', models.IntegerField(null=True)),
                ('credit_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('apartment_costs', models.DecimalField(decimal_places=2, max_digits=10)),
                ('education_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_expenses', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('food_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('food_weight', models.IntegerField(null=True)),
                ('transport_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transport_weight', models.IntegerField(null=True)),
                ('fun_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fun_weight', models.IntegerField(null=True)),
                ('sport_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sport_weight', models.IntegerField(null=True)),
            ],
        ),
    ]
