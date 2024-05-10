# SerpentSpotProject
 Capstone Software Engineering Project, Creating a django based platform to foster community, education, and indentification in the world of reptiles

 
# Features List - Safari:
## SnakeMap
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/7d389cab-0ea5-4f03-8352-c8a66505fdca)

The snakemap is the most backend heavy piece of the web app, it allows the user to select a location on a google maps JS map, with a radius and time range and see all snake observations meeting that criteria displayed on the map.

The backend is comprised of two components, a fetch_observations method that calls the Inaturalist API to recieve a JSON object containing all observations meeting the criteria provided by the front end and formats it to be given to the map.

The main view map_view that renders the template, and calls and passes the fetch_observations if it is given a POST request. Given a post request instead of rendering the template it returns a JSONresponse to the frontend with the formatted observations

The front end logic is handled by the map.js, this file has functions to intialize the map, drop a pin when a double click occurs and pass that lat/long data to the form above the map, render a radius provided in the form with a red circle on the map, send a post request to the backend to recieve observations, and plot the observations on the map with pins containing the observation's data

## FAQ
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/77eec2e4-eace-46ae-afe8-970bf60fc985)

The FAQ is a very simple component, it has a data model to hold a question/answer and a slug for the url of that question. There are two views, one to render the home page with all the questions, and another view render a template with the answer to the question that was clicked (utilizing slugs for the urls). This app is used to answer common questions that may come up specifically about the web app and features in it.

## Identification
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/6ba25ad2-8e78-44a7-a6f6-7388c98e805c)

The identification app is meant to be a dyanmic library of various snake species, their ranges, and many other common metrics to identify them.

The data is stored in two distinct models, a state model that has it's title and abbreviation, as well as a SnakeSpecies model that holds the ID information like Common Name, venemous status, and image path to our static directory which contains photos of all the snakes, as well as a many to many relationship with the state model.

The users can navigate the page with two main methods, a search bar that will try to find species matching the given string, as well as a method to filter just by state. The user also has the choice to sort by ascending and descending alphabetical order.

There is JS in the template that intializies the state dropdown, deals with sorting, live searching, as well as filtering down to a single species if the search value is autofilled (Like when jumping to the ID app from an observation or favorite snake on the profile, it will automatically display that chosen species)

The singular view renders the pages template, with the given "context" (snake and state data) if the page is freshly loaded it will simply display all the snakes found in the US until a specific state is submitted in the form.

## Forum
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/dd1f50da-afe0-476b-945b-65e19cc9f7b4)
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/af676640-3164-401c-8dce-d35aad40d10d)
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/cbfd9638-181f-49c4-953e-5921242e8eb3)



This may be the most CODE dense component of the web app, it is a user forum that allows people discuss the hobby and interact with other members of the herping community.

It is broken up into three main templates
* One to display all the boards on the forum as well as the most recent threads, and replies
* A template that renders a chosen board (Displays all the threads on that board)
* Finally a template that renders a chosen thread (The thread itself and all the replies under it, as well as a reply form to add replies to the thread)

Data
* A board model with title and description
* A thread model with a reference to the board it's on, creation time, user who created it etc
* A post model (Similar to thread but acts as a reply to a given thread, so it has a reference to it's parent thread)
* A post image model (This store's and handles photos being attached to a thread or a reply)

Views
* Home - Renders the boards template and passes recent posts/threads to template
* Board threads - Recieves a board id and returns the board threads templates with all the threads corresponding to that board
* Thread posts - Renders the thread template with all the replies and initializes the form for replies
* New threads - Handles the new thread form and creates a new thread (Storing info in DB)
* Reply thread - Same as new thread but handles a new reply to a thread (Storing new info in BD)
* User Profile - Allows link to each user profile attached to a thread or reply
* Delete thread/post - Both of these views handle the deletion of a thread and post handling the DB aspect and confirms that the user who created it is the only trying to delete
* Edit post/thread - Handles post requests to edit either a post or thread, and refreshes the page to update the information after it's changed in the DB


## Education
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/af0106fe-1f7e-4f7c-a480-dc48cbfc910a)

This is another simple and static component of the web app, it is simply an html template using bootstrap cards and drawers to organize information for the users. It is just one view to render the template. This app is meant to give the users a good introduction to the hobby and answer many common questions beginners have.

# Features List - Seamus:

## Home page:
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/13d975ad-dbbe-48c3-8d9e-14eec5ea5579)
- The landing point for users on serpent spot. From here users can branch out and explore the site.
- Includes navigation to FAQ, Profile, Identification, Observation Journal, and Forum.
- Provides context and point of entry as well as smooth transition to main features.
 ----------
- Consists mostly of stlyed cards and buttons that serve as access points to other sections of the website.
- No data is stored on this page, it uses a simple view and template. 

## Profile page 
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/b68a73aa-cef4-4126-a38c-dff034d23ff1)
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/eaef08fd-00cf-4a0f-805b-b1a3fd06d5a2)
- A central point for users to express themselves and serves as a sort of homebase for all of their user uploaded content.
- Users can quikcly see if you're active on the forum, mkaing observations, and ranked on the leaderboard. 
- Navigation to the Forum, Observation Journal, ID page, and Leaderboard 
- Users can edit their profile picking a favorite snake, bio and profile picture.
----------
-  The profile model stores user information: Bio, Profile pic, Favorite snake
- The profile template is built out of styled cards, utilizing template engine to render links to the users observations and forum activity. The associated view grabs recent observations, forum posts, total observations and total forum posts. 

## Observation Journal
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/28375000-330d-4b6d-95b3-cd5fd60e38af)
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/757e1d05-78f8-491c-9209-8f77afcbdb14)
- One of Serpent Spot's core functionalities. Users can upload and record snake sightings they've had in the form of their Observation Journal.
- Requires a species ID and a quick note about  your sighting, a picture is optional (honors system)
- Users can view others journals, getting an idea of what they have seen and what they though!
- Links to ID page directly for identification help
----------
- The observation journal is built around the observation model. It consists of a species field, observation text, and an optional photo.
- The view serves two purposes, a central place to view your own observations, but also other users from their profiles. Only 6 observations are displayed on the profile, so you will come here to go for the less recent ones.
- template engine handles the modification of the template based on how the page is accessed. An alternate url is used to pass alternate user paramters.
## Leaderboard 
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/573d6e54-645f-4f75-9c96-a8d7c990463f)
![image](https://github.com/ReverendSafari/SerpentSpotProject/assets/63567335/fed34296-0513-444d-b698-95c6936f71a6)
- Here users can keep track of the platforms most frequent snake observers.
- Track your total observations, and try to get ranked on the leaderboard!
- Gives users an opportunity to interact with other user's profiles outside of the community forum.
- Clicking a user on the leaderboard takes you to their profile.
----------
- The leadboard is very view heavy. It querries all the observations for the current month and determines where users rank out of the ten availible spaces.
- Bootstrap cards are used here again to create the leaderboard tiles/positions, with the top three positions being podium colors.
- Template engine is used to handle different cases for the users leaderboard status, announicng ranked status, no observations, or how many more to reach 10th place. 
## Additional Work
- Login and Registration, built on DJango user auth
- Forum Boards overhaul (Styling, recent posts and threads, layout redesign)
- Individual species view and searchbar on ID page
- Footer (NOT on features list but its not a feature it just looks nice)
- Profile flair (this became the profile overhaul adding activity trackers and links to other page)
