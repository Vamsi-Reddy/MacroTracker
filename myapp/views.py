from django.shortcuts import render, redirect
from .models import Food, Consume
from django.contrib.auth.models import User
import sqlite3
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
cnt = 1


def index(request):
    global cnt
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        consume = Consume(cnt, food_consumed=consume)
        cnt += 1
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.all()

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    consumed_food.delete()
    return redirect('/')


def delete_food(request, id):
    food_item = Food.objects.get(id=id)
    food_item.delete()
    return redirect('/foodBase')


@csrf_exempt
def add_food(request):
    try:
        conn = sqlite3.connect('db.sqlite3')
        data = request.POST
        name = str(data['name'])
        carbs = int(data['carbs'])
        protein = int(data['protein'])
        fats = int(data['fats'])
        calories = int(data['calories'])
        conn.execute(
            f"INSERT INTO myapp_food(name,carbs,protein,fats,calories)  VALUES ('{name}',{carbs},{protein},{fats},{calories})")
    except:
        conn.execute(
            f"UPDATE myapp_food SET carbs = {carbs}, protein = {protein}, fats = {fats}, calories = {calories} WHERE name = '{name}'")
    conn.commit()
    return redirect('/foodBase')

    # name = data['name']
    # protien = data['protien']
    # fats = data['fats']
    # carbs = data['carbs']
    # calories = data['calories']
    # print(name, protien, fats, carbs, calories)
    # conn.execute(
    #     "INSERT INTO Students VALUES (1, 'Ashok', '2000-10-27', 'M.Tech')")
    # return render('myapp/foodBase')


def food_base(request):
    foods = Food.objects.all()
    return render(request, 'myapp/foodBase.html', {'foods': foods})
