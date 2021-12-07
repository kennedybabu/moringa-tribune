from django.core.checks import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import datetime as dt

from news.forms import NewsLetterForm
from .models import Article, NewsLetterRecipients
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .email import send_welcome_email


def news_today(request):
    date = dt.date.today()   
    news = Article.todays_news()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name, email = email)
            recipient.save()
            send_welcome_email(name, email)
            
            HttpResponseRedirect('news_today')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date, "news": news, "letterForm":form})

def convert_dates(dates):
    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day = days[day_number]
    return day

def past_days_news(request, past_date):

    try:
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date": date, "news": news})


def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f'{search_term}'

        return render(request, 'all-news/search.html', {"message":message, "articles":searched_articles})

    else:
        message = "You haven't seacrhed for an item"
        return  render(request, 'all-news/search.html', {"message": message})


def article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'all-news/article.html', {"article":article})

# def news_today(request):
#     if request.method == 'POST':
#         form = NewsLetterForm(request.POST)
#         if form.is_valid():
#             print('valid')
#     else:
#         form = NewsLetterForm()
#     return render(request, 'all-news/today-news.html', {"date":date, })