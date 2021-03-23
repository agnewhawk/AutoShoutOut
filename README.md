by Agnew Hawk
Version: 1.0.0.0
Last Updated: March 24 2021

Description:
-------------
Forget configuring events for individual members!

AutoShoutOut enables you to fetch a memberlist of your stream team with a click of a button. 
If a member of that team speaks in Twitch chat, their channel and stream team's team page are automatically shouted out by the chatbot.

You can customize the greets in Script settings, and by editing the streamers.json file you can assign unique greets to each individual team member!

Installation:
-------------

1) Make sure your Streamlabs Chatbot is set up to work with Python 2.7 scripts according to their manual: https://streamlabs.com/content-hub/post/chatbot-scripts-desktop
2) Import 'AutoShoutOut' to Streamlabs Chatbot.

How to Setup and Fetch team list?
-------------

Before you press the big 'UPDATE TEAM LIST' button, you must type in the Stream Team you wish to fetch by its TEAM ID, not team name. 
Most of the time the team ID is just team name without spaces, in lowercase letters, but not always. 

    Eg. Rage Club's team name is 'Rage Club', but its team ID is 'rageclub'
    
If you're unsure, your team's Twitch page has the team ID in its URL, `https://www.twitch.tv/team/[YOUR_TEAM_ID]`

After typing in your Team ID, press 'Save Settings' first and only then hit 'Update Team List'.
The script  lets you know if the operation is successful, and the list of team members is saved on your computer.

Finally you should reload all scripts and you're good to go.
