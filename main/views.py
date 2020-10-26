from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import mainItem
from nlp.main import run_sentimet_analyzer
# Create your views here.


#when the server gets the request, return http response hello world
def myView(request):
    first_item = mainItem.objects.all()[0]  #first data in the DB
    return render(request, 'index.html', 
        {'first_item': first_item})
    # return HttpResponse('hi')

#when there is a keyword passed in the form
def passKeyword(request):
    #Update DB
    first_item = mainItem.objects.all()[0]   #first data in the DB]
    keyword = request.POST['keyword']        #this is the input keyword passed from templates
    
    #run a method that gets us the sentimental result(0-100)
    result_percent = 55 #run_sentimet_analyzer(keyword)                     #add your result here
    first_item.result = result_percent
    first_item.content = keyword
    # new_item = mainItem(content = keyword)
    first_item.save()

    #Render Progress bar
    #result = 87
    
    return HttpResponseRedirect('/main/')