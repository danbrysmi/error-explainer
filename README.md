# Python Error Explainer
## Dan Bryan-Smith's 3rd Year Project

### To-Do:
    - Look into cpython to gather more error traces
    - Add traces based on the common errors from Digital People Doc
    - Add more tests
    - Provide example solutions for templates
    - Improve explanation panels
    - Improve website styling
    - Add trace highlighting from hovering over panels

### Current Features:
    - Form that takes in text input for their error trace
    - When submitted, takes the user to a results page with help
    - Presents the user with the correct template, along with the parameters and tags
    - Each tag is associated to a help panel (bootstrap card)
    - Panels give help text and link to more resources (currently w3schools)

### Running the server
`cd myproject/` (so you are in the same directory as manage.py)<br>
`python manage.py runserver`

### Stopping the server
`Ctrl + Break`<br>
(there is no Break button on my laptop so I use a Virtual Keyboard - Ctrl + Pause does the same thing)

### Database Migrations 
(need to do this whenever the database structure changes including removal and additions of whole models and individual fields)
`python3 manage.py makemigrations`<br>
`python3 manage.py migrate`

### If you've messed up the database beyond all hope:
`python manage.py flush`<br>

    - Backup any templates and error types that you want to use
    - then DELETE THE MIGRATIONS so it doesn't try to remember the last one
    - you also have to create a new admin account


