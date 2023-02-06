# General Assembly Project Four - Festi: a Python Django API and React App

# Deployment
Please find the full deployment of the app [here](https://festi-front-end.netlify.app/).

# Description
This was my final project built on the Immersive Software Engineering course with General Assembly. Festi is a full-stack application designed to help users search for new music festivals for the summer months. This is the first project I have built using Django as the backend framework for api routing and using PostGreSQL to create the database of festivals. The app leverages React as a frontend framework and implements Material UI and CSS for styling. 

# Code Installation

Clone the backend repo using the SSH Key contained within the Code button above, then follow the steps below in a local Terminal window:

```sh
git clone <COPIED_SSH_KEY>
cd <Newly cloned git repo>
```
Now you have navigated into the cloned git repo you can run the following commands:

```sh
pipenv install
```
```sh
pipenv shell
```
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
```sh
python manage.py runserver
```

Now you have the backend installed correctly we can move onto the frontend:

Navigate to frontend repo [here](https://github.com/wyndhams/ga-project-4-frontend) then clone the repo on your local machine as above. Once you have changed your current directory to the newly cloned repo, use the following commands in your terminal window:

```sh
npm install
```
```sh
npm start
```