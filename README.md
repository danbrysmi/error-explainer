# Python Error Explainer
## Dan Bryan-Smith's 3rd Year Project

### To-Do:
    - Look into cpython to gather more error traces and create examples if applicable
    - Add traces based on the common errors from Digital People Doc
    - Add more tests
    - Improve explanation panels
    - Improve website styling

### Current Features:
    - Form that takes in text input for their error trace
    - When submitted, takes the user to a results page with help
    - Presents the user with the correct template, along with the parameters and tags
    - Each tag is associated to a help panel (bootstrap card)
    - Panels give help text and link to more resources (currently w3schools)
    - Selected tags provide python example solutions
    - Different parts of the traceback are highlighted based on type (header, frame summary, exception etc)
    - Some CSS transitions have been added

### Report Progress (Draft /#1)
    - Abstract (Done!)
    - Introduction (In Progress...)
    - Background (In Progress...)
    - Design (Not done yet.)
    - Development (Not done yet.)
    - Feedback & Improvements (Not done yet.)
    - Conclusion (Not done yet.)

### Running the server
`cd myproject/` (so you are in the same directory as manage.py)<br>
`python manage.py runserver`

### Stopping the server
`Ctrl + Break`<br>
(there is no Break button on my laptop so I use a Virtual Keyboard - Ctrl + Pause does the same thing)

### CSS not working?
It might be because Chrome is keeping your old stuff cached. Fix it by refreshing with `Ctrl + F5`

### Running Tests
`python manage.py test results`

### Finding Error Messages in CPython
Example: `PyErr_SetString(PyExc_IndexError, "index out of range");`
So you can search the [repo](https://github.com/python/cpython) for `PyErr_SetString`

Here is some [Useful Info](https://github.com/python/cpython/blob/main/Doc/extending/extending.rst) about Exceptions found on the cpython repo.

### Database Migrations
(need to do this whenever the database structure changes including removal and additions of whole models and individual fields)
`python3 manage.py makemigrations`<br>
`python3 manage.py migrate`

#### If you've messed up the database beyond all hope:
`python manage.py flush`<br>

    - Backup any templates and error types that you want to use
    - then DELETE THE MIGRATIONS so it doesn't try to remember the last one
    - you also have to create a new admin account
