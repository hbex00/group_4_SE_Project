# group_4_SE_project

|Group Members|Git Handles|Emails|
|-------------|-----------|-----|
|Hugo Bexell|hbex00|behu23hw@student.ju.se|
|Axel Håkansson|Just-Another-Programer|haax23or@student.ju.se|
|William Klasson|Irodoot|klwi24jt@student.ju.se|
|Samuel Johansson|Itchingtree|josa24ym@student.ju.se|
|Noah Haraldsson|NoahHaraldsson1337|hano24if@student.ju.se|
|Bjarne Svensson|BjarneOS|svbj23mw@student.ju.se|

## Project Details
### Project Vision

We aim with this project to develope a recipe-sharing website.\
It aim to include features like user accounts,\
these accounts would then have capabilities of uploading private or public recipes,\
as well as uploading reviews to existing public recipes.

### The following details entail the languages and dependencies utilized in this project.

The Project's web-server uses the framework __flask__ and will connect to the database utilizing __SQL-alchemy__, and __SQL-lite__.\
The backend will be comprised of __python__.\
The frontend will be a mixture of __HTML__ and __CSS__. User interaction through __javascript__.

## Project planning

### Minimal Viable Product (MVP)

The functionality to upload a recipe to a database.\
The functionality to fetch a recipe from a database for viewing.

### Version 1.0

A stable product where multiple users can interact with the server and with other user's recipes.

### Roadmap

The main branch is our development branch where we introduce features and fixes.\
Specific stable versions/releases will be tagged on this main branch.\
We will use feature/issue branches that we merge into the development branch to address issues.

### Agreed on a workflow

Our plan is to have a working main branch and for us to have separate branches for test builds and trying new features.

We plan to use pull requests for the main branch in the future, once we have learned it. Also, all commits should have meaningful and informative comments. 

we have a kanbanbord here [kanban board][]

[Kanban board]: https://github.com/users/hbex00/projects/2

### Assets

ICONPACKS:
SVG file for user icon  
https://www.iconpacks.net/free-icon/user-3295.html

### Running instructions

1. Make a virtual environment inside project folder

        $ py -m venv .venv

2. Activate the virtual environment

        (windows): $ .venv\Scripts\activate
        (linux): $ source .venv/bin/activate

3. Install Flask-SQLAlchemy and all independencies with pip inside the venv

        $ pip install -r requirements.txt

4. Start the program

        $ py run.py

5. Connect to the loopback-address

        http://127.0.0.1:5000


## Declaration of Authorship
I, Hugo Bexell, declare that I am the sole author of the content I add to this repository.\
I, Axel Håkansson, declare that I am the sole author of the content I add to this repository.\
I, William Klasson, declare that I am the sole author of the content I add to this repository.\
I, Samuel Johansson, declare that I am the sole author of the content I add to this repository.\
I, Noah Haraldsson, declare that I am the sole author of the content I add to this repository.\
I, Bjarne Svensson, declare that I am the sole author of the content I add to this repository.
