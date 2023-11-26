# TwitterClone

A fullstack microblogs application allowing a user to create posts, follow other users and view their posts.

## Deployed version of the application
The deployed version of the application can be found at http://hossainaniad.pythonanywhere.com/ .

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`

## Warning
Issues with django-bootstrap-pagination 1.7.1 with python 3.9 and django 4.2.6
Need to update line 13 of bootstrap_pagination.templatetags.bootstrap_pagination to "from django.utils.translation import gettext_lazy as _"
