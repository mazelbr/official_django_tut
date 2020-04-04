# Official Tutorial - Quickstart
## Getting startd
```shell
django-admin startproject mysite
--------------------------------
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```
This is the structure of your overall project. Most important is the manage.py file which provides a lot of the functionality. You can test the setup by running the server
``````
python manage.py runserver
``````
Inside your priject you now can create apps with 
``` 
python manage.py runapp appname 
-------------------------------
appname/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
The difference between project and apps is that project actually do somethin e.g. payment blogging etc. A project on the otherhand is a collection of configurations and apps for a website. Note that apps do not require the project and can easily exhchanged

## Views
Inside your app you can create views by defining methods in the view.py file. Those methods have to take at least a request attribute as first attribute but can also handle additional parameter e.g. from the url. Django expects views to return a HTTPRepsonse.
```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

## Routing and URLS
Note that you already have a global urls.py ín your project directory but you can define anotherone inside of each app. The global urls.py file handles all the incoming requests but we can embed our app urls.py file there so our local routes can be handeled as well
```python
# appname/urls.py
from django.urls import path
urlpatterns = [
    path('', views.method_name, name ="somename")
    ,
]

#projectname/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('appname/', include('appname.urls')),
    path('admin/', admin.site.urls),
]
```
Here quite a few things are going on lets start wirh the path
* the path takes a string that refers to the url `'index/'` would represent www.example.com/index. The second argument tells django which view/method the request should be routed. The third argument is the name. Names should be unique within each app and can be used to adress a certain route. Why this is a nice feature will be eyplained later
* Inside the global url.py file we are now including something.
Include tells django that is should redirect all requests that start with 'appname/' to our url.py file of our app directory
* And as a preview you can see that we enabled the admin tool

## The Database Setup
You can connect your app to a database by setting the database parameter inside the `project/settings.py`  
By default Django uses a SQLite database which needs no further specifications and work fine for developent

In case you are using the standard contrib apps the server already told you that you have open migrations. You can install the necesarry databases for admin and sessions with 
```
python manage.py migrate
```
In most cases we need additional databases for our own specific data. Those can easily be written in python. Lets consider Questions and Choices as an example
```python
# polls/models.py¶

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
Each class inheriates from the model.Model class which gives them access to the predefined field_types. Inside the Method we can specify first contraints for our data. We also have to define the relations between our databases here see ForeinKey.   
Note that ForeinKey methods always require a on_delete statement

### Include the app in our project
To register our app for our project we have to extend the INSTALLED_APPS list in the `project/settings.py` file. We have to tell Django the way to our app config file in a dotstyle path.
```
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    ...
]
```

### Implement the database
We now have to implement the database we defined in the models file. First of all we have to create migration files that define statements to actually create the database with 
```
python manage.py makemigrations appname
```
We can inspect the SQL statement for our migrations by calling 
```
python manage.py sqlmigrate polls 0001_initial
```
We can check if the defined models are syntactically correct with
```
python manage.py check
```
To create the databse we once again call 
```
p<thon manage.py migrate>
```

## The built in Shell
Django provides a built in shell that can be started with
```
python manage.py shell
```
In this interactive interpreter we can access all the models views and routes of our project. In addition we can use the interpreter to create data for our databases^

## The Admin Tool
For many Apps you will sooner or later need an admin tool thats why djngo provides a built-in tool out of the box. You can use it when in your INSTALLED_APPS the tool is not commented out and your routes has a corresponding route. (usually /admin)   
Before you can log in you have to create a superuser with
```
python manage.py createsuperuser
```
Now log in with the chosen name and password. The Admin tool allows you to create additonal admins, user, usergroups, rights etc. Furthermore is already has implemented a databse wrapper for all of your models. Through them you can create update and delete data without the terminal

## Write views that actuall do Somethin
as mentioned you can pass parameters through the urls e.g. with `path('polls/<int:question_id'>/, views.details, name='details')`

Inside your views you can access the models by importing them 
```
from .models import Question

def detail(request, question_id):
    q = Question.objects.get(id = question_id)
    return HTTPResponse()
```
You could now create HTTP-code here but it is easier to use templates. 
In your settings.py TEMPLATE list you probably have `APP_DIR =True` which tells django to search for a `appname/template` directory for each app. Even though it might seem redundant it is convention to create another `appname` directory inside this folder where you now can define html templates e.g. `details.html` . You can access varaibles with {{}} and use python tags with {%%}
```
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
## The render() shortcut
Since loading templates and filling it with data is a common task django provides a render() shortcut. `render(request, 'route', context_dict)` has the request as first attribute, specifies the route afterwards and finally privides a dict with all the variables that should be avaialbe in the views

## The 404 Shortcut
If you are trying to access access pages that are not available e.g. because we type in a wrong id for a database element we want django to render a 404 error page we could do this manualy with
```
rom django.http import Http404
from django.shortcuts import render
from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```
or use the shourtcut 
```python 
    from django.shortcuts import get_object_or_404, render
    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
            return render(request, 'polls/detail.htm', {'question': question})
```
Additional shortcuts are avauable for get_list_or_404() togeather with filter() instead of get() but note that it also redirect to 404 when the list is empty

## Do not use hardcoded URLS
Here the naming of the routes get clearer. It is bad style and agaist loose coupling to hardcode links and urls. A better way is to refer to the name of a route and use the url tag
```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

**Namespacing:** For only one app it's probably no big deal to find unique names but for a growing project with many apps this could quickly mess up. But you can define an app_name inside the `appname/urls.py` that can be used by the global urls.py file.
```python
# appname/urls.py
rom . import views

app_name = 'polls'
urlpatterns = [...,]

# polls/templates/polls/index.html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

