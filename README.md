# Python Error Explainer
## Dan Bryan-Smith's 3rd Year Project

## Django help
outer myprojectt/ - root directory, container for project, can rename
inner myproject/ - python package, package name to import stuff from elsewhere e.g. myproject.urls - if renaming you'll need to change all of the import references/ (done using Include(...))

## Running Django Server
python manage.py runserver
(Remember Virtual Keyboard - Ctrl + Pause will stop the server running)

## Running Database Migrations - (need to do this whenever the database structure changes including removal and additions of whole models and individual fields)
python3 manage.py makemigrations
python3 manage.py migrate

## To-Do:
Follow tutorial on https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page to learn more about how to use Django!
