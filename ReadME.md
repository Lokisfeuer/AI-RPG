# This Project 
## in a few bullet points:
- This is a text based RPG Framework.
- Users can create roleplay adventures through a web application.
- Everybody can play adventures created from anybody.
- The full game is mostly text input and text output with only very few exceptions.
- This makes it possible to have multiple different applications.
In this case there is a webapp, a discord bot and a simple direct print/input variant.
- It uses OpenAI to create natural language input and output.
- It uses multiple pytorch AI-modules to process input as well as output.
## The structure of an adventure:
The structure of an adventure is defined in adventure.py.
An adventure consists of 5 types of objects:
### Non-Player-Characters or NPCs
Characters the player might meet and interact with.
### Locations
Locations where the adventure takes place
### Secrets
What would an adventure be without secrets you can find out?
NPCs and locations have an attribute of secrets the player can find while interaction with the NPC or location.
Secrets store a boolean value whether they are found or not.
### Flags
A flag holds a boolean value and conditions for that value.
When the conditions are fulfilled the value is set to true and when the conditions aren't fulfilled the value gets set to false. 
This value is regularly updated.
Every adventure object that's not a flag has an activation flag attribute.
Only objects that are "active" appear during normal procedure of the game.
This gives the possibility to have the story evolve:
Only when a certain secret is found new NPCs with new secrets get activated and the story moves forward.
### Trigger
A trigger is called when a certain flag is set to true.
The trigger then calls a custom function with the full game object as parameter.
The function can then manipulate the game in any way as well as interact with the player.
The functions of triggers are stored in the trigger_files directory.
## Explanations of the files:
### adventure.py
The structure of an adventure is defined in adventure.py.
An adventure consists of 5 types of objects:
- Non-Player-Characters or NPCs
- Locations
- Secrets
- Flags
- Trigger

This file defines each of these objects.
For a more detailed explanation see the structure of adventures.
### game.py
This file defines the class for a running game containing its adventure, the current status of the game and functions to play.
### menu.py
Every user has one menu that manages their games.
It stores all games from the user and also which one the user is currently playing.
Here other options can easily be added and managed.
### bot.py
This file uses the discord library to access a discord bot through which the full game can be played.
### webapp.py
This file uses flask to create a wep application through which the game can be played and new adventures can be written.
### main.py
Here either the webapp or the discord bot are run, or it just runs the full game via the simple main() function.
### writer.py
This file writes adventures. Currently, adventures can only be written via the web application.
### adventures.json
Stores all adventures.
### user_data.json
stores the menu of every user.
## The use of AIs
// add detailed explanation of AI use.