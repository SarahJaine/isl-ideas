# ISL Ideas

[ISL Ideas](https://ideas.isl.co) is an internal message board application for employees of iStrategyLabs.  ISL Ideas is a place to share thoughts about innovative products we should build, technologies we should explore, workplace policies we should change, or anything else that’s on your mind.  

Sign in using your isl.co email address and get ideating!

---

## Developing

### Requirements

* Python 3
* [foreman](http://ddollar.github.io/foreman/)

### Python and Django

First you need to configure your environment:

```
cp env.example .env
```

Edit *.env* and set the values you need to run the project locally. 

Next, create a Python 3 virtual environment and install the requirements:

```
mkvirtualenv --python=$(which python3) isl-ideas
pip install -r requirements.txt
```

Create the database specified in *.env*, run the initial model migration,
and create a super user:

```
createdb islideas
foreman run python manage.py migrate
foreman run python manage.py createsuperuser
```

### Front End Tools

Use [nvm](https://github.com/creationix/nvm) to install the correct version
of Node.js and install the front-end dependencies:

```
nvm install
npm install
```

Do an initial build of assets:

```
gulp build
```

## Running the Project

First load the virtualenv:

```
workon isl-ideas
```

Then use [foreman](http://ddollar.github.io/foreman/) (or [forego](https://github.com/ddollar/forego)) to run the development processes:

```
foreman start -f Procfile.dev
```

*Procfile.dev* defines the following processes:

* web: the Django development server
* static: the gulp watch process


`foreman start -f Procfile.dev` will start all of the processes at once. If you
want to run a specific process, you can specify it directly:

```
foreman start -f Procfile.dev web
```

### Procfile

When deployed to production or staging, the application and any other processes will be run as defined in the Procfile. You can run this file locally using [foreman](http://ddollar.github.io/foreman/) to launch the application the same way it will be run in production:

```
foreman start
```

You are **highly encouraged** to do this before finishing features to make sure the app runs as expected before it is deployed.

##Deployment

pushing to master autodeploys to staging application

