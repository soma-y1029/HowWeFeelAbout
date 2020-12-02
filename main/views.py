from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import mainItem
from nlp.main import run_sentiment_analyzer


# Create your views here.


# when the server gets the request, return http response hello world
def home(request):
    return render(request, 'index.html', {})


# when there is a keyword passed in the form
def show_sentiment(request):
    # Update DB
    # all_items = mainItem.objects.all()
    # first_item = all_items[0]  # first data in the DB]
    # print(type(first_item))
    # print(f'{first_item=} {first_item.result=} {first_item.content=}')

    keyword = request.POST['keyword']  # this is the input keyword passed from templates
    print(f'{request.POST["keyword"]=}')

    first_item = mainItem()

    # run a method that gets us the sentimental result(0-100)
    res_dict = run_sentiment_analyzer(keyword)
    result_percent = res_dict['Positiveness']  # add your result here
    first_item.result = result_percent
    first_item.content = keyword
    first_item.positive_tweets = res_dict['Positive_tweets']
    first_item.negative_tweets = res_dict['Negative_tweets']

    # new_item = mainItem(content = keyword)
    first_item.save()

    print(type(first_item))
    print(f'{first_item=} {first_item.result=} {first_item.content=}')

    # Render Progress bar
    # result = 87
    return render(request, 'index.html', {'first_item': first_item})
    # return HttpResponseRedirect('/')
