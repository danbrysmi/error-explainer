# Python Error Explainer
## Dan Bryan-Smith's 3rd Year Project

# To-Do:
    - Follow tutorial on https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
    to learn more about how to use Django
    - Gather Python traces to come up with more templates
    - Go over loop to see if there are any gaps where the program could crash
    - Provide example solutions for templates
    - Think about what the explanation 'panels' are going to look like
    - Website styling :)
    - Re-add the other \_\_\_Error ones that were removed

# Current Features:
    - Form that takes in text input
    - When submitted, takes the user to a results page with the error trace
    - Presents the user with the correct template
    - Delivers the parameters as specified in the template's <n> tags

## Running the Django Server
go to the outer myproject/ (so you are in the same directory as manage.py)
python manage.py runserver

## Stopping the Django server
Ctrl + Break
(there is no Break button on my laptop so I use a Virtual Keyboard - Ctrl + Pause does the same thing)

## Running Database Migrations - (need to do this whenever the database structure changes including removal and additions of whole models and individual fields)
python3 manage.py makemigrations
python3 manage.py migrate

### If you've messed up the database structure beyond all hope:
    - Backup any templates and error types that you want to use
    - python manage.py flush
    - then DELETE THE MIGRATIONS so it doesn't try to remember the last one
