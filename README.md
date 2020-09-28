## Deployment
A live demo of this project can be viewed [here](https://tgc07-project04.herokuapp.com/).
All the source code for this project is available [here](https://github.com/andrewsui/tgc07-project04) on GitHub.

Code for the project was committed to GitHub in the following manner:
- Individual files were added to the next commit staging area by executing the `git add <filename>` command in a command-line interface.
- All changes in the working directory were added to the next commit staging area by executing the `git add .` command in a command-line interface.
- Staged content was committed as new commit snapshot by executing the `git commit -m “<message>"` command in a command-line interface.
- Local branch commits were pushed to the remote repository master branch by executing the `git push -u origin master` command in a command-line interface.
- Subsequent local branch commits were pushed to the remote repository master branch by executing the `git push` command in a command-line interface.

Deployment to Heroku was performed in a debian based linux environment bash terminal in the following manner:
- Install Heroku on local machine: `sudo snap install heroku --classic`
- Log into Heroku: `heroku login -i`
- Create a new heroku app: `heroku create <app-name>`
- Verify that the correct remotes have been added: `git remote -v`
- If changing PC, add heroku repo by executing:
`heroku git:remote -a <heroku app name>`
- Setup a python virtual environment in the root folder of the project: `python3 -m venv venv`
- Activate the python virtual environment whilst being in the root folder of the project: `source venv/bin/activate`
- Install libpq-dev python3-dev packages **before** installing psycopg2 python pip package:
`sudo apt install libpq-dev python3-dev`
- Install the dependencies: `pip install dj-database-url Django django-allauth django-crispy-forms django-mathfilters djangorestframework gunicorn psycopg2 python-dotenv stripe whitenoise`
- Create requirements.txt file to record dependencies for deployment and reinstallation on other machines `pip freeze > requirements.txt`

Using a file manager:
- Create a file named `Procfile` without speech-marks or file extension and save `web gunicorn <Django app name without .py>.wsgi:application` on the first line of `Procfile` (in my case, the content of the Procfile was `web: gunicorn app_main.wsgi:application`)

Using a web browser:
- Log into [Heroku](https://id.heroku.com/login) and set environment variables for `SECRET_KEY = <your own key>`, `DEBUG_MODE = "False"`, `DATABASE_URL = <Heroku PostgreSQL database URL>`, `STRIPE_PUBLISHABLE_KEY = <Stripe publishable key>`, `STRIPE_SECRET_KEY = <Stripe secret key>`, `STRIPE_WEBHOOK_SIGNING_SECRET = <Stripe webhook endpoint signing secret>`, `EMAIL_HOST_PASSWORD = <email host password>`, `EMAIL_HOST_USER = <email address>`

Back in the bash terminal:
- Commit all new changes to GitHub: `git add .` then `git commit -m “<message>"` then `git push`
- Finally, push to Heroku: `git push heroku master`

## Run locally on your own machine on debian based linux OS
- Clone the [repository](https://github.com/andrewsui/tgc07-project04)
- Setup a python virtual environment in the root folder of the project: `python3 -m venv venv`
- Activate the python virtual environment whilst in the root folder of the project: `source venv/bin/activate`
- Install libpq-dev python3-dev packages **before** installing psycopg2 python pip package:
`sudo apt install libpq-dev python3-dev`
- Install the dependencies: `pip install -r requirements.txt`
- Setup and run a public URL for testing using a service such as [ngrok](https://ngrok.com/) and your chosen <port_number>. Note down this public URL for use in step below referenced as <ngrok_URL>. This is required for Stripe webhook redirects.
- In root folder of project, create a `.env` file and set the following environment variables: `export = SECRET_KEY = <your own key>`, `export = DEBUG_MODE = "True"`, `export = DEBUG_URL = "<ngrok_URL>"`, `export = STRIPE_PUBLISHABLE_KEY = <Stripe publishable key>`, `export = STRIPE_SECRET_KEY = <Stripe secret key>`, `export = STRIPE_WEBHOOK_DEBUG = <Stripe webhook endpoint signing secret>`
- Make database migrations `python manage.py makemigrations`
- Migrate `python manage.py migrate`
- Run the web app `python manage.py runserver <port_number>`
- Use a web browser to navigate to `<ngrok_URL>:<port_number>`
