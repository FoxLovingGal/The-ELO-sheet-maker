# The-ELO-sheet-maker
Program that takes columns showing placement in 4 player games and creates an ELO Timeline on google sheets using a base ELO of 800 while also updating in a separate sheet an all time and season ELO count for each individual player. 

# Installation
It should only require Python 3.13 (may work on older versions, but it was developed in Python 3.13). In order to run you will need google's api credentials, to learn how to set that up you can look here: https://developers.google.com/workspace/guides/create-credentials#oauth-client-id
In order to run it you will also need to acquire a token.json, when you try to run it on your spreadsheet it will automatically open up what is needed to do that, you simply need to give it permissions. 

# Usage
It requires a little bit of set up, I intend to create future versions that will be better able to handle more unique set ups, but for now it requires 4 columns containing 4 players, with the furthest left column being the 1st place holder, and the furthest left being the 4th place holder, it also requires a separate sheet (currently has to be named "People", but this will be changed very shortly to allow any name to be selected for it) to contain up to date values on each players stats. It also requires a cell to be named Timeline where you wish the Timeline to be placed.
The images below should help illustrate the structure that is required

![The highlighted cells/information is that which is required to be the same as in the image in terms of content](https://i.imgur.com/gpq7LEM.png)
![The highlighted cells/information is that which is required to be the same as in the image in terms of content](https://i.imgur.com/a3D13V5.png)
![The highlighted cells/information is that which is required to be the same as in the image in terms of content](https://i.imgur.com/9BZfXlk.png)

The settings and config are largely self-explanatory, but here is an explanation anyways
SPREADSHEET - contained within the config file, simply requires the spreadsheet ID, you know, that thing at the end of the really long url https://docs.google.com/spreadsheets/d/ID
num_players - no need to do anything with this, it is entirely managed by the script
in settings.txt
Timeline_name - the name of the sheet which the Timeline and the placement info will be stored in
Timeline_start_row - the row in which that info will be stored on
season_elo - row in which season_elo is located on
all_time_elo - row in which all_time_elo is located on
name_locations - location of player names in the non-timeline sheet
name_sheet - currently unutilized but once it is implemented in a day or two it will be the name of that secondary sheet.

# Contributing
If for whatever reason you wish to contribute to the project, please open up an issue, for very minor changes feel free to make pull requests.

# License
[GNU Lesser General Public License v3.0](https://choosealicense.com/licenses/lgpl-3.0/)
