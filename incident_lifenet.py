from Tools import tools_v000 as tools
from Topdesk import topdesk as t
from Jira import jira as j
from MyHours import myhours as m
import os
from os.path import dirname


# -16 for the name of this project Incident_Lifenet
# save_path = dirname(__file__)[ : -16]
save_path = os.path.dirname(os.path.abspath("__file__"))[ : -16]
propertiesFolder_path = save_path + "\\"+ "Properties"

test = False # If False, create Jira Ticket else if True We are in test mode => no creation of the JIRA ticket

t.incidentNumber = "I2010-00146"
j.sprint = "PNN-TOS-PI2020.4.2"

j.epic_link = tools.readProperty(propertiesFolder_path, 'Incident_Lifenet', 'epic_link=')
j.save_path = tools.readProperty(propertiesFolder_path, 'Incident_Lifenet', 'save_path=')

# Open Browser
tools.openBrowserChrome()

# Start MyHours
if test != True :
    print ("Start the clock for the ticket")
    m.connectToMyHours()
    m.enterCredentials()
    m.startTrack()
else :
    print ("We are in test mode - no start new time")

# TopDesk part
t.connectViaLink()
t.incidentTitle()

# Jira part
j.connectToJiraBoard()

jiraTitle = t.incidentNumber + " - " + t.incidentTitle 
if test != True :
    print ("Creation of the JIRA ticket")
    j.createJira(jiraTitle, t.description_text, t.incidentNumber)
else :
    print ("We are in test mode - no creation of the JIRA ticket")
j.selectJira()

j.connectToJira(j.jira)
j.recoverJiraInformation()
j.startJira()

# Create folder link to this JIRA
j.createFolderJira(j.jira)
j.createFileInto(j.jira, j.jiraTitle, j.description_text, j.jira, j.jira + "_Comment_v001" )

# Start MyHours
m.connectToMyHours()
if test != True :
    print ("We are already connected not needed to enter credential")
else :
    m.enterCredentials()
m.modifyTrack(j.jira, j.jira + ' - ' + j.jiraTitle, j.epic_link)

# 
tools.openFolder(j.save_path + j.jira)
tools.openFile(j.save_path + j.jira + '/' + j.jira + '_Comment_v001.txt')

# Exit Chrome
tools.driver.quit()