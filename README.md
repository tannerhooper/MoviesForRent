# Rent-A-Movie! 
## https://rent-a-movie-231721.appspot.com
This is an app for people to share movies amongst themselves. 

## Organization Name and Structure
cp ~/pasta is the unofficial name given to the team working on this project. Officially we are known as group 10. 
Members include: 
+ Zach Hawkes
+ Nick Jugganaikloo
+ Tanner Hooper
+ George Done

All team members will work on all aspects of the application and the various scrum roles will rotate between each member every sprint

## Version Control Guidelines 
All changes and additions to the application will be tracked in this git repository. 
Any changes made to this branch should be made on a feature branch.

### Process of adding new feature to the application
1. Create a feature branch for developing the feature.
2. Once the feature has been coded out, create a pull request to merge the feature branch into the test branch.
3. Request a review from another member of the group on the pull request
4. Once this member has reviewed and approved it after performing their own test and review of the code. Request another review from another member of the group
5. Once the pull request has two approved reviews, the feature branch can be merged into the test branch
6. Once the feature is merged into test another pull request is created to merge the test branch into the master branch. 
7. The feature will be tested by a member of the group that did not originally code the feature in the test branch. 
8. Once testing has passed in the test branch the PR is merged into master and the feature is present in production level code. 

## Tool Stack
This app is written in Python 3 using the Django framework. 
Versions: 
+ Django = 2.1.7
+ Python3 = 3.7.2

Any code editor or IDE can be used to work on this application as no restriction is currently needed or forseen. 

## Setup Procedure
For now this will follow the same initial setup procedure as a normal Django app. This may change if different libraries are added to the app that need additional setup. 

## Build Instructions
1. Install Python 3.7.2
2. Install Django 2.2  
3. Pull most recent code from git repository
4. Configure local SQlite database
	* python manage.py makemigrations
	* python manage.py migrate
5. Start the django server
	* python manage.py runserver
6. When it is the project has been reached a major release version and has been deemed ready by the team the project will be configured to run on a google cloud server



## Unit and System Testing
1. Install requests module using "pip install requests"
2. Run tests by using "python manage.py test"

## Important Stuff
Google Cloud 
Backups are created daily between 10pm and 2 am
Postgres data base logins
	username password
	postgres bOCBdG0yzNjzIa2B
	django   Team10
Connection Name
	rent-a-movie-231721:us-central1:movies-beta
gs bucket name 
	movies-for-rent

## How to Redeploy
This The tutorial we followed to do the intial deploy https://cloud.google.com/python/django/flexible-environment  
Required command line tools can be installed by following the tutorial

All commands should be run in the same directory as manage.py

It is possible to run the server on your computer and connect to the data base in the cloud.(this is optional but very useful)  
Edit settings,py to so that DATABASES['default']['HOST'] = '127.0.0.1' instead of the cloud database.  
get the right version of the cloud sql proxy from the above link 
then use this command  
* ./cloud_sql_proxy -instances="rent-a-movie-231721:us-central1:movies-beta"=tcp:5432  
or for windows 
*	cloud_sql_proxy.exe -instances="[rent-a-movie-231721:us-central1:movies-beta]"=tcp:5432  
After enabling the proxy you may manipulate the data base using these commands and more
* python manage.py makemigrations  
* python manage.py migrate



It is recommended that you create a virtualenv like so (this is optional)
1. create one
	virtualenv env
2. then begin using it
	source env/bin/activate or for windows env\scripts\activate
3. then install modules
	pip install -r requirements.txt
4. your termianl shoud look like (env)location $ 
	Run all manage.py stuff from this terminal with (env) showing




To redepoly you must
navigate to the directory containing manage.py 

1.Update Static files  
* python manage.py collectstatic  
* gsutil rsync -R static/ gs://movies-for-rent/static  

2.Redeploy to app engine project  
* gcloud app deploy

Code will be redeployed to https://rent-a-movie-231721.appspot.com



