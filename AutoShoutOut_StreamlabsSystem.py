import clr, sys, json, os, codecs, csv
import ctypes, winsound

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Future updates:
#
# - Multi-team & External list
#


ScriptName = "AutoShoutoutTeam"
Website = "https://www.twitch.tv/agnewhawk"
Creator = "Agnew Hawk"
Version = "1.0.0.0"
Description = "Auto-shoutout a member of a stream team when they speak in the chat for the first time. (one team supported)"


global settingsFile, teamFile

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
teamFile = os.path.join(os.path.dirname(__file__), "streamers.json")

class Settings:

    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf8-sig')
        else: #set variables if no settings file
            self.BaseResponse = "Team member detected in chat! If you're not already following {0}, you should, because they're awesome! Check'em out at {1} "
            self.TeamResponse = "Find out more awesome team members at {0}"
            self.StreamTeam = "rageclub"

    def ReloadSettings(self,data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return
        
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile, encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict_, encoding='utf-8-sig')))
        return
 
class StreamerList:
    def __init__(self, teamFile):
        if teamFile is not None:
            if not os.path.isfile(teamFile):
                with codecs.open(teamFile, encoding='utf-8-sig',mode='w+') as t:
                    t.write("{}")
                    t.close()
            with codecs.open(teamFile, encoding='utf-8-sig',mode='r') as t:
                self.team = json.load(t, encoding='utf-8-sig')
                self.ActiveStreamers = []
        
            
def Init():
    global MySettings, Team, Streamers, ServiceURL
    MySettings = Settings(settingsFile)
    Streamers = StreamerList(teamFile)
    ServiceURL = "https://www.twitch.tv/"
    return
    
def Execute(data):

    if data.IsChatMessage() and data.UserName.lower() not in Streamers.ActiveStreamers and data.UserName != Parent.GetChannelName():
        userDisplay = data.UserName
        user = userDisplay.lower()
        
        if user in Streamers.team:
            URL = ServiceURL + user.lower()
            teamURL = ServiceURL + "teams/" + str(MySettings.StreamTeam)
            
            if Streamers.team[user]["greeting"] != "":
                greet = Streamers.team[user]["greeting"].format(userDisplay,URL)
            else:
                greet = MySettings.BaseResponse.format(userDisplay,URL)
                
            team = MySettings.TeamResponse.format(teamURL)
            shoutout = greet + "--" + team
            
            message = shoutout[:507]+'...' if len(shoutout) > 507 else shoutout #Conform to 510 character limit
            Parent.SendStreamMessage(message)  #Message sent to Twitch here
            Streamers.ActiveStreamers.append(user)
            
        else:
            Parent.Log("AutoShoutOut", user+ ": No such user in team.") #Remove before deploying or else it flags Every Message Ever
def Tick():
    return
    
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
    
def ParseAPIResult(result):
  
    return

def FetchTeamMembers():
    Parent.Log("AutoShoutOut", "Fetch Team Members")
    MessageBox = ctypes.windll.user32.MessageBoxW
    team = MySettings.StreamTeam
    
    winsound.MessageBeep()
    answer = MessageBox(0, "Are you sure you want to get new list for {0}?\nThis will overwrite previous list.".format(team),"Confirm",1)

    Parent.Log("AutoShoutOut", team)
   
    if answer == 1:
        if team != "":
            apipath = "https://decapi.me/twitch/team_members/"
            apipath = apipath+team
            Parent.Log("AutoShoutOut",apipath)
            #try:
            teamString = Parent.GetRequest(apipath+"?text=true",{})
            teamString = json.loads(teamString)
            
            try: 
                teamString = teamString["response"].split('\n') #Remove guff and turn it into a list
                teamString = dict.fromkeys(teamString,{"greeting":""})
                
                with codecs.open(teamFile, encoding='utf-8-sig',mode='w+') as f:
                    json.dump(teamString, f, encoding='utf-8-sig',sort_keys=True,indent=4)
                    
                Streamers.ActiveStreamers = []
                    
                MessageBox(0, "Team list updated for team: {0}\nPlease, reload all scripts".format(team), "List updated", 0)
                
                return
            
            except:
                errorCode = teamString["status"]
                
                winsound.MessageBeep()
                if errorCode == 404:
                    MessageBox(0, "Team Not Found: {0}\nPlease check team id, it may not be the same as team name".format(team), "404 - Not Found", 0)
                
                else:
                    MessageBox(0, "Unable to get team list:\n {0}: {1}".format(teamString["status"],teamString["error"]), "Error", 0)
            
        
        else:
            winsound.MessageBeep()
            MessageBox(0, "Unable to get data: Team field empty", "Error", 0)
  
        #teamMemberString = Parent.GetRequest(https://decapi.me/twitch/team_members/:team_id)