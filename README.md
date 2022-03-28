# Python Error Explainer
## Dan Bryan-Smith's 3rd Year Project

### To-Do:
    - Migrate worked examples to models.py
    - Migrate tips to models.py
    - Link top 10 common errors to traces templates
    - Change spacing of all elements to design mockup
    - Change carousel navigation to buttons at the bottom
    - Add escape characters in parser
    - Add tests for new parsing abilities

### Current Features:
    - Form that takes in text input for their error trace
    - When submitted, takes the user to a results page with help
    - Different parts of the traceback are highlighted in each section based on type 
    - (header, frame summary, frame summary line,  exception, carat)
    - Line number labelling from FSL's linked FSUM info

### Results Carousel:
    - 1) Presents the user with their trace giving an overview with info on the error type
    - 2)* Presents a breakdown of the users code that brought up the error
    - 3) Presents an explanation of the error template if there is one
    - 4)* Presents a worked example to relate to the error template with description
    - 5)* Presents help panels of related concepts for additional resources based on tags
    - (* are optional)
    
### Parsing Abilities:
    - Strings
    - Ints and floats
    - Functions and methods
    - Attributes
    - Control statements
    - Operators
    - Unfinished strings/brackets.
    - Anything else is parssed as an expression
    - Function and Methods call the parser recursively for their parameters
    - Syntax (commas and colons)
    - Brackets and Square Brackets (tuples, lists and indexing)
    - Carats ('^') on their own for SyntaxError are not parsed as python.
    
### Report Progress (Draft /#1)
    - Abstract (Done!)
    - Introduction (Done!)
    - Background (In Progress...)
    - Design (In Progress...)
    - Development (Not done yet.)
    - Feedback & Improvements (Not done yet.)
    - Conclusion (Not done yet.)

### Markdown Explanations:
Markdown Cheatsheet: https://duckduckgo.com/?q=markdown+cheatsheet&t=ffab&ia=answer&iax=answer 

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
