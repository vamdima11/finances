import ast
from time import sleep

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Portfolio, Investment, Goal, History


# @login_required
def portfolio(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(user=request.user)

    if request.method == 'POST':
        goal_amount = request.POST.get('goal_amount')
        if goal_amount:
            goal_amount = float(goal_amount)
            if goal_amount < 0:
                messages.error(request, 'Invalid goal amount')
            else:
                portfolio.goal = goal_amount
                portfolio.save()
                History.objects.create(portfolio=portfolio, change=f"Goal changed to {goal_amount}")
        else:
            investment_id = request.POST.get('investment_id')
            investment_action = request.POST.get('investment_action')
            investment_quantity = request.POST.get('investment_quantity')
            if investment_id and investment_action and investment_quantity:
                investment = Investment.objects.get(pk=investment_id)
                if investment_action == 'add':
                    investment.quantity += int(investment_quantity)
                    History.objects.create(portfolio=portfolio,
                                           change=f"{investment.symbol} ({investment_quantity}) added")
                elif investment_action == 'remove':
                    if int(investment_quantity) > investment.quantity:
                        messages.error(request, 'Invalid quantity')
                    else:
                        investment.quantity -= int(investment_quantity)
                        History.objects.create(portfolio=portfolio,
                                               change=f"{investment.symbol} ({investment_quantity}) removed")
                investment.save()
                portfolio.save()
    investments = Investment.objects.filter(portfolio=portfolio)
    goals = Goal.objects.filter(portfolio=portfolio)
    highest_goal = goals.first()
    history = History.objects.filter(portfolio=portfolio)
    return render(request, 'portfolio.html',
                  {'portfolio': portfolio, 'investments': investments,
                   'goals': goals, 'history': history,
                   'highest_goal': highest_goal})


import random
import matplotlib.pyplot as plt
import io
import base64


@login_required
def add_investment(request):
    portfolio = Portfolio.objects.get(user=request.user)
    investment_amount = request.GET.get('investment_amount')
    if investment_amount:
        investment_amount = float(investment_amount)
        investment_quantity = (investment_amount / 2, investment_amount / 2)  # Пример 50/50 распределения
        approach = portfolio.approach
        print('investment: ', investment_amount)
        if approach:
            print('approach: ', approach)

            labels = []
            prices = []
            if portfolio.approach == 'Aggressive':
                # BTC, AAPL, BA, TSLA, GOOGL
                labels = ['BTC', 'AAPL', 'BA', 'TSLA', 'GOOGL']
                prices = [random.randint(1000, 10000), random.randint(100, 1000), random.randint(100, 1000),
                            random.randint(100, 1000), random.randint(100, 1000)]
            elif portfolio.approach == 'Conservative':
                # MSFT, NVDA, TSLA, AMZN
                labels = ['MSFT', 'NVDA', 'TSLA', 'AMZN']
                prices = [random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000),
                            random.randint(100, 1000)]
            else:
                # JPM, JNJ, BA
                labels = ['JPM', 'JNJ', 'BA']
                prices = [random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000)]

            # Генерация случайных процентных соотношений для акций
            percentages = [random.randint(1, int(100/len(labels))) for _ in range(len(labels))]

            # Изменение последнего процентного соотношения для достижения суммы 100
            total_percentage = sum(percentages)
            percentages[-1] += 100 - total_percentage

            # Расчет количества акций на основе процентных соотношений и цен акций
            quantities = []
            for i in range(len(labels)):
                print('investment_amount: ', investment_amount)
                print('percentages[i]: ', percentages[i])
                print('prices[i]: ', prices[i])
                quantity = round(investment_amount * (percentages[i] / 100) / prices[i], 2)
                quantities.append(quantity)

            print('quantities107: ', quantities)

            from io import BytesIO
            img = BytesIO()
            plt.figure(figsize=(6, 6))
            print('percentages: ', percentages)
            plt.pie(percentages, labels=labels, autopct='%1.1f%%')
            plt.axis('equal')

            plt.savefig(img, format='png')
            plt.savefig('./static/test.png', format='png')

            plt.close()
            img.seek(0)
            chart_base64 = base64.b64encode(img.getvalue()).decode('utf8')

            return render(request, 'add_investment.html',
                              {'portfolio': portfolio,
                               'approach': approach,
                               'investment_quantity': investment_quantity,
                               'chart_base64': chart_base64,
                               'stock_ticks': labels,
                               'stock_prices': prices,
                               'stock_amounts': quantities})
        else:
            messages.error(request, 'Invalid input')

    return render(request, 'add_investment.html', {'portfolio': portfolio})


@login_required
def accept_investment(request):
    portfolio = Portfolio.objects.get(user=request.user)
    print(request.POST)
    stock_ticks = request.POST.get('stock_ticks')
    stock_prices = request.POST.get('stock_prices')
    stock_amounts = request.POST.get('stock_amounts')

    stock_ticks = ast.literal_eval(stock_ticks)
    stock_prices = ast.literal_eval(stock_prices)
    stock_amounts = ast.literal_eval(stock_amounts)
    print(stock_ticks)

    if request.method == 'POST' and len(stock_ticks) > 0:
        for x in range(len(stock_ticks)):
            investment = Investment.objects.create(portfolio=portfolio, symbol=stock_ticks[x].upper(),
                                                   quantity=int(stock_amounts[x]),
                                                   purchase_price=float(stock_prices[x]),
                                                   current_market_value=float(stock_prices[x]))
            History.objects.create(portfolio=portfolio, change=f"{investment.symbol} ({investment.quantity}) added")

        return redirect('portfolio')
    else:
        messages.error(request, 'Invalid input')
    return redirect('portfolio')  # Если нажата кнопка "Отвергнуть"


@login_required
def edit_investment(request, investment_id):
    portfolio = Portfolio.objects.get(user=request.user)
    investment = Investment.objects.get(pk=investment_id)
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        quantity = request.POST.get('quantity')
        purchase_price = request.POST.get('purchase_price')
        if symbol and quantity and purchase_price:
            investment.symbol = symbol.upper()
            investment.quantity = int(quantity)
            investment.purchase_price = float(purchase_price)
            investment.current_market_value = float(purchase_price)
            investment.save()
            History.objects.create(portfolio=portfolio, change=f"{investment.symbol} ({investment.quantity}) edited")
            return redirect('portfolio')
        else:
            messages.error(request, 'Invalid input')
    return render(request, 'edit_investment.html', {'investment': investment})


@login_required
def delete_investment(request, investment_id):
    investment = Investment.objects.get(pk=investment_id)
    portfolio = investment.portfolio
    History.objects.create(portfolio=portfolio, change=f"{investment.symbol} ({investment.quantity}) deleted")
    investment.delete()
    return redirect('portfolio')


@login_required
def add_goal(request):
    portfolio = Portfolio.objects.get(user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            goal = Goal.objects.create(portfolio=portfolio, amount=float(amount))
            History.objects.create(portfolio=portfolio, change=f"Goal {goal.id} added")
            return redirect('portfolio')
        else:
            messages.error(request, 'Invalid input')
    return render(request, 'add_goal.html')


@login_required
def edit_goal(request, goal_id):
    portfolio = Portfolio.objects.get(user=request.user)
    goal = Goal.objects.get(pk=goal_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            goal.amount = float(amount)
            goal.save()
            portfolio.highest_goal = portfolio.goals.aggregate(Max('amount'))['amount__max']
            portfolio.save()
            History.objects.create(portfolio=portfolio, change=f"Goal {goal.id} edited")
            return redirect('portfolio')
        else:
            messages.error(request, 'Invalid input')
    return render(request, 'edit_goal.html', {'goal': goal})


@login_required
def delete_goal(request, goal_id):
    goal = Goal.objects.get(pk=goal_id)
    portfolio = goal.portfolio
    History.objects.create(portfolio=portfolio, change=f"Goal {goal.id} deleted")
    goal.delete()
    return redirect('portfolio')


@login_required
def approach(request):
    portfolio = Portfolio.objects.get(user=request.user)
    if request.method == 'POST':
        approach = request.POST.get('approach')
        if approach:
            Investment.objects.filter(portfolio=portfolio).delete()
            portfolio.approach = approach
            portfolio.save()
            History.objects.create(portfolio=portfolio, change=f"Approach changed to {approach}")
            return redirect('portfolio')
        else:
            messages.error(request, 'Invalid input')
    return render(request, 'approach.html', {'portfolio': portfolio})


@login_required
def calculator(request):
    portfolio = Portfolio.objects.get(user=request.user)
    goals = Goal.objects.filter(portfolio=portfolio)
    investments = Investment.objects.filter(portfolio=portfolio)
    context = {
        'portfolio': portfolio,
        'goals': goals,
        'investments': investments
    }
    if request.method == 'POST':
        goal_amount = request.POST.get('goal_amount')
        if goal_amount:
            goal_amount = float(goal_amount)
            if goal_amount < 0:
                messages.error(request, 'Invalid goal amount')
            else:
                context['goal_amount'] = goal_amount
                context['forecast_years'] = 10
                context['forecast_amount'] = 10000
    return render(request, 'calculator.html', context)


def index(request):
    return render(request, 'index.html')


from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('portfolio')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


import os
import joblib
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max
from .models import Investment, Portfolio


@login_required
def predict(request):
    portfolio = Portfolio.objects.get(user=request.user)
    investments = list(Investment.objects.filter(portfolio=portfolio))

    # Load models for each stock from predictor_model directory
    models = {}
    for investment in investments:
        ticker = investment.symbol
        model_file = f'predictor_model/{ticker}.pkl'
        if os.path.exists(model_file):
            models[ticker] = joblib.load(model_file)

    # Calculate total balance and investment count
    total_balance = Investment.objects.filter(portfolio=portfolio).aggregate(Sum('current_market_value'))[
                        'current_market_value__sum'] or 0
    total_balance = float(total_balance)

    investment_count = len(investments)

    # Get approach of the user
    approach = portfolio.approach

    # Add additional investments based on user's approach
    if portfolio.approach == 'Aggressive':
        bitcoin_price = 50000
        bitcoin_quantity = (float(total_balance) * 0.2) / bitcoin_price
        investments.append(Investment(symbol='BTC', quantity=bitcoin_quantity, purchase_price=bitcoin_price))
        total_balance += bitcoin_price * bitcoin_quantity

    elif portfolio.approach == 'Conservative':
        gold_price = 1700
        gold_quantity = (float(total_balance) * 0.1) / gold_price
        investments.append(Investment(symbol='GLD', quantity=gold_quantity, purchase_price=gold_price))
        total_balance += gold_price * gold_price

    # Calculate time required to reach the goal
    goals = Goal.objects.filter(portfolio=portfolio)
    goal = float(max(goal.amount for goal in goals))

    time_to_goal = (goal - total_balance) / (total_balance / len(models))

    context = {
        'total_balance': total_balance,
        'investment_count': investment_count,
        'approach': approach,
        'days_to_goal': round(time_to_goal),
    }
    return render(request, 'prediction.html', context)
