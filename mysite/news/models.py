from django.db import models
import pandas as pd
from pulp import *
from django.db import connection

# Create your models here.
class Spheres(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сфера жизни'
        verbose_name_plural = 'Сферы жизни'

class Spheres_weight(models.Model):
    sphere_id = models.ForeignKey(Spheres, on_delete=models.PROTECT)
    weight = models.IntegerField(null=True)

    def __str__(self):
        return self.sphere_id

    class Meta:
        verbose_name = 'Вес сферы'
        verbose_name_plural = 'Веса сфер'

class Quality(models.Model):
    level = models.CharField(max_length=300)

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = 'Качество жизни'
        verbose_name_plural = 'Качество жизни'

class Mealtime(models.Model):
    type = models.CharField(max_length=300)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'

class Transport(models.Model):
    name = models.CharField(max_length=300)
    sphere_id = models.ForeignKey(Spheres, on_delete=models.PROTECT)
    quality_level = models.ForeignKey(Quality, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'

class Sport(models.Model):
    name = models.CharField(max_length=300)
    sphere_id = models.ForeignKey(Spheres, on_delete=models.PROTECT)
    quality_level = models.ForeignKey(Quality, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спорт'
        verbose_name_plural = 'Спорт'

class Fun(models.Model):
    name = models.CharField(max_length=300)
    sphere_id = models.ForeignKey(Spheres, on_delete=models.PROTECT)
    quality_level = models.ForeignKey(Quality, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Развлечение'
        verbose_name_plural = 'Развлечения'

class Food(models.Model):
    name = models.CharField(max_length=300)
    sphere_id = models.ForeignKey(Spheres, on_delete=models.PROTECT)
    mealtime_type = models.ForeignKey(Mealtime, on_delete=models.PROTECT)
    quality_level = models.ForeignKey(Quality, on_delete=models.PROTECT)
    calorific = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Питание'
        verbose_name_plural = 'Питание'

class UserData(models.Model):
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ежемесячный доход, руб.')
    family_number = models.IntegerField(null=True, verbose_name='Количество членов семьи')
    credit_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Кредитный платеж, руб.')
    apartment_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Расходы на оплату жилья, руб.')
    education_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Плата за обучение, руб.')
    other_expenses = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Прочие расходы, руб.')
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Месячный бюджет, руб.', null=True)
    food_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет питание, руб.', null=True)
    food_weight = models.IntegerField(null=True, verbose_name='Удельный вес сферы "Питание", %', default= Spheres_weight.objects.get(id = 1).weight)
    #food_weight = models.IntegerField(null=True, verbose_name='Удельный вес сферы "Питание", %', default = '55')
    #food_set = models.ArrayField(max_digits=10, decimal_places=2, verbose_name='Прочие расходы, руб.')

    transport_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет транспорт, руб.',null=True)
    transport_weight = models.IntegerField(null=True, verbose_name='Удельный вес сферы "Транспорт", %', default= Spheres_weight.objects.get(id = 2).weight)
    fun_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет развлечения, руб.', null=True)
    fun_weight = models.IntegerField(null=True, verbose_name='Удельный вес сферы "Развлечения", %', default= Spheres_weight.objects.get(id = 3).weight)
    sport_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет спорт, руб.', null=True)
    sport_weight = models.IntegerField(null=True, verbose_name='Удельный вес сферы "Спорт", %', default= Spheres_weight.objects.get(id = 4).weight)

    def food_selection(self):
        db_query = str(Food.objects.all().query)
        df = pd.read_sql_query(db_query, connection)
        prob = LpProblem("Food_Choice_Problem", LpMaximize)
        food_items = list(df['id'])
        costs = dict(zip(food_items, df['cost']))
        calories = dict(zip(food_items, df['calorific']))
        food_integer = LpVariable.dict('', food_items, lowBound=0, upBound=1, cat='Integer')
        prob += lpSum([calories[i] * food_integer[i] for i in food_items]), "Total calories of the diet"
        prob += lpSum([costs[f] * food_integer[f] for f in food_items]) >= 1.00, "CostMinimum"
        prob += lpSum([costs[f] * food_integer[f] for f in food_items]) <= int(UserData.objects.last().food_budget / 30), "CostMaximum"
        prob.writeLP("Food_Choice_Problem.lp")
        prob.solve()
        food_optimal = []
        for v in prob.variables():
            if v.varValue > 0:
                food_optimal.append(v.name[1:])
        return food_optimal

    def transport_selection(self):
        if (UserData.objects.last().transport_budget / 4) >= 360:
            db_query_tr = str(Transport.objects.all().query)
            df = pd.read_sql_query(db_query_tr, connection)
            prob = LpProblem("Transport_Choice_Problem", LpMaximize)
            transport_items = list(df['id'])
            costs = dict(zip(transport_items, df['cost']))
            transport_integer = LpVariable.dict('', transport_items, lowBound=0, upBound=12, cat='Integer')
            prob += lpSum([costs[i] * transport_integer[i] for i in transport_integer]), "Total cost"
            prob += lpSum([costs[f] * transport_integer[f] for f in transport_integer]) >= 1, "CostMinimum"
            prob += lpSum([costs[f] * transport_integer[f] for f in transport_integer]) <= int(UserData.objects.last().transport_budget / 4), "CostMaximum"
            prob += lpSum([transport_integer[f] for f in transport_integer]) == 12, "Need transport"
            prob.writeLP("Transport_Choice_Problem.lp")
            prob.solve()
            transport_optimal = {}
            for v in prob.variables():
                if v.varValue > 0:
                    transport_optimal[(v.name[1:])] = v.varValue
        else:
            by_bus = int((UserData.objects.last().transport_budget / 4) / 35)
            transport_optimal = {'1': by_bus}
        return transport_optimal

    def fun_selection(self):
        if (UserData.objects.last().fun_budget / 4) >= 150:
            db_query_fun = str(Fun.objects.filter(id__lte = 8).query)
            df = pd.read_sql_query(db_query_fun, connection)
            prob = LpProblem("Fun_Choice_Problem", LpMaximize)
            fun_items = list(df['id'])
            costs = dict(zip(fun_items, df['cost']))
            fun_integer = LpVariable.dict('', fun_items, lowBound=0, upBound=12, cat='Integer')
            prob += lpSum([costs[i] * fun_integer[i] for i in fun_integer]), "Total cost"
            prob += lpSum([costs[f] * fun_integer[f] for f in fun_integer]) >= 1, "CostMinimum"
            prob += lpSum([costs[f] * fun_integer[f] for f in fun_integer]) <= int(UserData.objects.last().fun_budget / 4), "CostMaximum"
            prob += lpSum([fun_integer[f] for f in fun_integer]) <= 7, "Max fun"
            prob.writeLP("Fun_Choice_Problem.lp")
            prob.solve()
            fun_optimal = {}
            for v in prob.variables():
                if v.varValue > 0:
                    fun_optimal[(v.name[1:])] = v.varValue
        else:
            fun_optimal = {'9': 1, '10': 1}
        return fun_optimal

    def sport_selection(self):
        if (UserData.objects.last().sport_budget / 4) >= 100:
            db_query_sport = str(Sport.objects.filter(id__gte = 3).query)
            df = pd.read_sql_query(db_query_sport, connection)
            prob = LpProblem("Sport_Choice_Problem", LpMaximize)
            sport_items = list(df['id'])
            costs = dict(zip(sport_items, df['cost']))
            sport_integer = LpVariable.dict('', sport_items, lowBound=0, upBound=12, cat='Integer')
            prob += lpSum([costs[i] * sport_integer[i] for i in sport_integer]), "Total cost"
            prob += lpSum([costs[f] * sport_integer[f] for f in sport_integer]) >= 1, "CostMinimum"
            prob += lpSum([costs[f] * sport_integer[f] for f in sport_integer]) <= int(UserData.objects.last().sport_budget / 4), "CostMaximum"
            prob += lpSum([sport_integer[f] for f in sport_integer]) <= 7, "Max sport"
            prob.writeLP("Sport_Choice_Problem.lp")
            prob.solve()
            sport_optimal = {}
            for v in prob.variables():
                if v.varValue > 0:
                    sport_optimal[(v.name[1:])] = v.varValue
        else:
            sport_optimal = {'1': 1, '2': 1}
        return sport_optimal


    class Meta:
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователя'
