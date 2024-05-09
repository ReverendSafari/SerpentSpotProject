**
# Deployment Guide

 ## Running on localhost

 1. If you don't have one already install an IDE, like vscode onto your computer
 2. Download Git
	 (Windows) Download here https://git-scm.com/download/win and install it, you can keep the default settings during installation
	 (Mac) Install Git using Homebrew, simply open a terminal and run brew install git, if you don't have homebrew installed you can get it here https://brew.sh/
 3. If you don't have python yet install it from this link https://www.python.org/downloads/
     (For windows users make sure to check the box that says "Add Python to PATH")
4. Now that python and git are installed open up your terminal again and add these commands with your name and email to configure them in Git  `
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
`
5. Now that git is installed and configured we are going to "clone" the project, which just means making a copy of all the projects files locally. 
   Open your command prompt and type 
 `git clone https://github.com/ReverendSafari/SerpentSpotProject.git`
 and then lets navigate into the projects folder using this command
`cd SerpentSpotProject
`
(Windows)
 Now we need to create a virtual enviroment, a project typically contains a lot of "dependencies" or external libraries it depends on. It is good practice to create a segragated place to store these dependencies so your system isn't overloaded with them, this is what a virtualenv does.
 First install virtualenv by typing this command into your console `pip install virtualenv
`
Now create a virtual enviroment named 'venv' `virtualenv venv`
And finally activate the enviroment (Think of your virtualenv as a a special room on your computer, this command lets us walk into that room) `.\venv\Scripts\activate`
(Mac)
 Install virtualenv with this command `pip3 install virtualenv`
Create your venv `pip3 install virtualenv`
Activate your venv `source venv/bin/activate`
6. Now we need to install our requirements (all the libraries our website needs to run) with this command `pip install -r requirements.txt`
7. Now we need to fill our database with the correct tables and models (the structure of a database) so our app can add into it, and get data from it. We will do this with a series of two commands in the console
`python manage.py makemigrations
python manage.py migrate` 

8. Before we can run the server we need to get a googlemaps api key so you can use the snakemap, to do this simply follow the instructions here https://developers.google.com/maps/documentation/javascript, your api key is a secret key that lets you use the google maps service. Once you have it we need to add the key as a env variable. (Store it on the system) 
(Windows) The command is `set GOOGLE_MAPS_API_KEY='apikeyhere'`
(Mac)  The command is `export GOOGLE_MAPS_API_KEY='apikeyhere'`
10. Finally we can start the webserver and interact with out website with this command `python manage.py runserver`

Congratulations ! You are now running SerpentSpot locally on your computer!
You should simply be able to open a web browser and type in http://127.0.0.1:8000 as the url.


## Deploying on python anywhere
1. Follow the steps above to clone the repository, and create your google maps api key
2. Install github desktop https://desktop.github.com/ and log in
3. Create an account on https://www.pythonanywhere.com/
4. Click file in the top left hand corner and click "new repository" then chose a name and description and confirm by clicking "Create Repository"
5. Open you cloned repo in the ide of your choice and navigate to the settings.py file located in the SerpentSpotProject directory in the repo
6. Look through the file and find allowed_hosts, once you find it add this domain too the list 'yourusername.pythonanywhere.com' and save 
7. Copy all the files from your cloned repository into the directory of your new repository that you just created 
8. In github desktop under the files tab add a simple summary and description, and click commit, and in the top center of github desktop you will see a button that says "push" click it

10. Now your repository is created on github!

Now you are all set up to actually deploy the project!

Pythonanywhere is a great platform for beginners to deploy simple python based web apps so lets jump right in, for a more detailed guide or extra tips they have their own deployment guide here https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/

1. Go to github and find you repository, click the blue button that says "code" and click the SSH tab under where it says "clone" and copy the link
2. On your pythonanywhere dashboard in the left column click "new bash console" and it should take you to a new page with a big terminal window, here we will clone you repository.
3. With your github clone link type `git clone git@github.com:myusername/myproject.git` in the console 
4. Now create a new virtualenv in your console and name it after your project (repo) name `mkvirtualenv --python=/usr/bin/python3.10 mysite-virtualenv`
5. Now install django `pip install django`
6. Finally install your requirements `pip install -r requirements.txt
7. Now that everything is installed write down the name of your venv
8. Open a new python anywhere tab and navigate to web tab and click to create a new web app, select manual configuration and choose python version 3.10
9. Enter your virtualvenv name
10. Enter the path to your code's main directory, it should be /home/'pythonanywhereusername'/'githubreponame'
11. Now we need to modify the wsgi file, the pythonanywhere uses this file to run and configure you website for you, go to the code tab in your web app and scroll until you find wsgiconfigurationfile and click on it
12. Delete everything except the Django section and uncomment the django section add in your project's path and the nameOfApp.settings (See link above for more detail) 
13. Setting up the static files (JS, CSS, etc) is simpler with images to guide you so please follow the official documentation https://help.pythonanywhere.com/pages/DjangoStaticFiles

15. Now go back to your console and run `python manage.py makemigrations` and finally `python manage.py migrate` and just like that your website is online! 

You should be able to view your website at the link provided on your dashboard!

## SnakeMap - How it's made

The snakemap was the API component of our app, and probably the most complex from a backend perspective. The design utilizes three main components.

1. The Inaturalist API
The Inat API is the key to getting data for our map. It contains observation data for millions of species across the globe, to querry this API we only need one API endpoint -> https://api.inaturalist.org/v1/observations
We pass in the taxon id for snakes, latitude, longitude, a radius in KM around this point, d1 (The start date of observations we want to see), and geo = true which tells the api we want to get the geographical data (lat,long) back for each observation.
	
	The api then returns a big json dictionary that we trim down to just pull out the information we want (Common name, Scientific name, and lat/long) this then get's passed back to the frontend to be handed off to the map.

2. Google Maps JS library
  This library is the workhorse of the snakemap, it allows us to render a google map onto the page, drop pins to find coordinates, draw our radius circle, and drop our dynamic observation pins onto said map. All the code to make this happen is isolated to one JS file map.js. It renders the map, takes the form data above the map to get data from the backend (inat api) and displays the data as pins on the map. All the functions to perform each task described is well documented in the JS file I am referencing. The formal documentation for the maps library can be found here 
  https://developers.google.com/maps/documentation/javascript


3. Google Map API
Unlike standard JS libraries the maps library and map object are very data heavy so the use of the map actually requires an api key, this can be found in the documentation above. In my code I have a env variable set in my settings.py file so I can use it in my snakemap views.

**
