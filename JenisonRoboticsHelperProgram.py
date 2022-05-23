#Programmed using Python 3.10.1
#Please read the ReadMe!
import datetime
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import discord
from discord.ext import commands
import json
import random

driver1 = webdriver.Chrome() #Change!
driver1.get('https://www.robotevents.com/robot-competitions/vex-robotics-competition/standings/skills')
html1 = driver1.page_source
soup1 = BeautifulSoup(html1, 'lxml')

record = []
teamData = []

def filterType(teamType):
    driver1.refresh()
    driver1.implicitly_wait(5)
    
    if(teamType == 1): #Select Michigan
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[1]/div/select/optgroup[1]/option[1]').click() #Selects Country USA
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[2]/div/select/option[35]').click()
    elif(teamType == 2): #Select Country
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[1]/div/select/optgroup[1]/option[1]').click() #Selects Country USA
    
def getTeam(row, teamType):
    row = str(row)
    obj = []
    if(teamType == 1): #State
        obj = [" ", " ", " ", " ", " ", " ", " "]
    elif(teamType == 2): #Country
        obj = [" ", " ", " ", " ", " ", " ", " ", " "] #Adds Event Region
        obj[7] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[14]').text
    elif(teamType == 3): #World
        obj = [" ", " ", " ", " ", " ", " ", " ", " ", " "] #Adds ER + Country
        obj[7] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[14]').text
        obj[8] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[15]').text

    obj[0] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[1]').text #Rank
    obj[1] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[2]').text #Total
    obj[2] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[3]').text #Program
    obj[3] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[4]').text #Driver
    obj[4] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[11]').text #Team Number
    obj[5] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[12]').text #Team Name
    obj[6] = driver1.find_element(By.XPATH, '//*[@id="standings"]/table/tbody/tr[' + row + ']/td[13]').text #Organization

    return obj

"""state = getTeam(, 1)
print(state[2])
print("Testing")"""

def getMultiple(howMany, teamType):
    teamData = []
    record.clear()
    if(teamType == 1):
        for team in range(1, howMany + 1):
            teamData = getTeam(team, teamType)
            record.append(teamData)
    elif(teamType == 2):
        for team in range(1, howMany + 1):
            teamData = getTeam(team, teamType)
            record.append(teamData)
    elif(teamType == 3):
        for team in range(1, howMany + 1):
            teamData = getTeam(team, teamType)
            record.append(teamData)

def discordDisplayTeams(embed, howMany, teamType):
    getMultiple(howMany, teamType)
    column = []
    teamInfo = " "
    rowName = " "
    if(teamType == 1):
        for column in record:
            teamInfo = "Rank: {0}, Total: {1}, Programming: {2}, Driver: {3}, Number: {4}, Name: {5}, Organization: {6}".format(column[0], column[1], column[2], column[3], column[4], column[5], column[6])
            #print(teamInfo)
            rowName = column[0] + ": " + column[4] + ' - "' + column[5] + '" with a score of ' + column[1]
            #print(rowName)
            embed.add_field(name = rowName, value = teamInfo, inline = False)
    elif(teamType == 2):
        for column in record:
            teamInfo = "Rank: {0}, Total: {1}, Programming: {2}, Driver: {3}, Number: {4}, Name: {5}, Organization: {6}, From: {7}".format(column[0], column[1], column[2], column[3], column[4], column[5], column[6], column[7])
            #print(teamInfo)
            rowName = column[0] + ": " + column[4] + ' - "' + column[5] + '", from: ' + column[7] + ' with a score of ' + column[1]
            #print(rowName)
            embed.add_field(name = rowName, value = teamInfo, inline = False)
    elif(teamType == 3):
        for column in record:
            teamInfo = "Rank: {0}, Total: {1}, Programming: {2}, Driver: {3}, Number: {4}, Name: {5}, Organization: {6} From: {7}, {8}".format(column[0], column[1], column[2], column[3], column[4], column[5], column[6], column[7], column[8])
            #print(teamInfo)
            rowName = column[0] + ": " + column[4] + ' - "' + column[5] + '", from: ' + column[7] + ", " + column[8] + ' with a score of ' + column[1]
            #print(rowName)
            embed.add_field(name = rowName, value = teamInfo, inline = False)

def discordSearchTeams(embed, team, teamType):
    try:
        filterType(teamType)
        driver1.implicitly_wait(5)
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[1]/div[1]/div/div/input').send_keys(team)
        discordDisplayTeams(embed, 1, teamType)
    except: #Didn't work? It could be because they are a Middle School Team.
        try:
            filterType(teamType)
            driver1.implicitly_wait(5)
            driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[3]/div/select/option[2]').click() #Selects Middle School
            driver1.implicitly_wait(7)
            driver1.find_element(By.XPATH, '//*[@id="filters"]/div[1]/div[1]/div/div/input').send_keys(team)
            discordDisplayTeams(embed, 1, teamType)
        except:
            teamInfo = "There was no data on the team, please try again."
            #print(teamInfo)
            rowName = "Error"
            #print(rowName)
            embed.add_field(name = rowName, value = teamInfo, inline = False)

###
### Initializing Bot
###

bot=commands.Bot(command_prefix=".")
bot.remove_command('help')
#myid = '<@722624613783175229>' #Bot UserID
myid = '<@607643088231464980>'

@bot.event
async def on_ready():
    print('The Discord bot is now ready. Using: '+ str(bot.user.name) + ' With user ID: '+ str(bot.user.id))

def makeTable(ctx, selectType, numberOfTeams, teamType):
    sendEmbed = [] 
    sendEmbed = discord.Embed(
                    title = "Top " + str(numberOfTeams) + " High School Teams in " + selectType,
                    color = discord.Color.blue()
                )
    discordDisplayTeams(sendEmbed, numberOfTeams, teamType)
    sendEmbed.set_footer(text="Info gathered at: " + str(datetime.datetime.now()))
    sendEmbed.set_thumbnail(url = "https://www.robotevents.com/images/robotevents-logo.png")
    return ctx.send(embed = sendEmbed) #Change

@bot.command(pass_context=True)
async def world(ctx, numberOfTeams:int=10, grade:str="h"):
    if(numberOfTeams > 25):
        numberOfTeams = 25
        await ctx.send("Cannot enter more than 25 teams. Finding top 25 teams.")

    if(grade == "h" or grade == "b" or grade == "hi" or grade == "bo"): #Gets High School
        filterType(3)
        driver1.implicitly_wait(5)
        await makeTable(ctx, "World for High School!", numberOfTeams, 3)
    if(grade == "m" or grade == "b" or grade == "mi" or grade == "bo"): #Gets Middle School
        filterType(3)
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[3]/div/select/option[2]').click() #Selects Middle School
        driver1.implicitly_wait(5)
        await makeTable(ctx, "World for Middle School!", numberOfTeams, 3)

@bot.command(pass_context=True)
async def usa(ctx, numberOfTeams:int=10, grade:str="h"):
    if(numberOfTeams > 25):
        numberOfTeams = 25
        await ctx.send("Cannot enter more than 25 teams. Finding top 25 teams.")

    if(grade == "h" or grade == "b" or grade == "hi" or grade == "bo"): #Gets High School
        filterType(2)
        driver1.implicitly_wait(5)
        await makeTable(ctx, "USA for High School!", numberOfTeams, 2)
    if(grade == "m" or grade == "b" or grade == "mi" or grade == "bo"): #Gets Middle School
        filterType(2)
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[3]/div/select/option[2]').click() #Selects Middle School
        driver1.implicitly_wait(5)
        await makeTable(ctx, "USA for Middle School!", numberOfTeams, 2)

@bot.command(pass_context=True)
async def state(ctx, numberOfTeams:int=10, grade:str="h"):
    if(numberOfTeams > 25):
        numberOfTeams = 25
        await ctx.send("Cannot enter more than 25 teams. Finding top 25 teams.")

    if(grade == "h" or grade == "b" or grade == "hi" or grade == "bo"): #Gets High School
        filterType(1)
        driver1.implicitly_wait(5)
        await makeTable(ctx, "Michigan for High School!", numberOfTeams, 1)
    if(grade == "m" or grade == "b" or grade == "mi" or grade == "bo"): #Gets Middle School
        filterType(1)
        driver1.find_element(By.XPATH, '//*[@id="filters"]/div[2]/div[3]/div/select/option[2]').click() #Selects Middle School
        driver1.implicitly_wait(5)
        await makeTable(ctx, "Michigan for Middle School!", numberOfTeams, 1)

@bot.command(pass_context=True)
async def rank(ctx, team:str="!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", teamType:str="s"):
    if(team == "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"):
        await ctx.send("Invalid team. Correct Usage: ,rank 2140A")
    else:
        if(teamType == "s" or teamType == "state"):
            selectType = "Michigan!"
            teamType = 1
        elif(teamType == "c" or teamType == "country"):
            selectType = "the USA!"
            teamType = 2
        elif(teamType == "w" or teamType == "world"):
            selectType = "the World!"
            teamType = 3
            
        sendEmbed = []
        temp = ""
        sendEmbed = discord.Embed(
                        title = "Searching for team " + team +  " in " + selectType,
                        color = discord.Color.green()
                    )
        
        discordSearchTeams(sendEmbed, team, teamType)
        
        sendEmbed.set_footer(text="Info gathered at: " + str(datetime.datetime.now()))

        sendEmbed.set_thumbnail(url = "https://www.robotevents.com/images/robotevents-logo.png")
        
        await ctx.send(embed = sendEmbed) #Change

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("pong")

@bot.command(pass_context=True)
async def game(ctx): ### Game

    gameEmbed = discord.Embed(
                title = "Vex 2022-2023 Game: Spin Up",
                description= "Description of the Vex 2022-2023 Game",
                color = discord.Color.green()
            )
    gameEmbed.add_field(name = "The Details: ", value = "There are sixty (60) Discs and four (4) Rollers on a VRC Spin Up Field. Discs can be Scored in the two High Goals, one per Alliance, at opposite corners of the field.  Each Disc scored in a High Goal is worth 5 points. However, Robots aiming for the High Goal had better be accurate!  Because underneath each High Goal, is a 1-point Low Goal for the opposing Alliance. In addition to Discs, Robots can also spin the four Rollers mounted to the field perimeter.  If the area inside of a Roller’s pointers only shows one color, that is considered “Owned” by that Alliance.  Each Owned Roller is worth 10 points. As the clock winds down, it’s time for the Endgame. At the end of the Match, Alliances will receive a 3 point bonus for each tile their Robots are Covering. So, during the last 10 seconds of the Match, there are no horizontal expansion limits. The Alliance that scores more points in the Autonomous period is awarded with ten (10) bonus points, added to the final score at the end of the match. Each Alliance also has the opportunity to earn an Autonomous Win Point by scoring at least two Discs in Alliance’s High Goals, and owning Both Rollers on their side of the field. This Bonus can be earned by both Alliances, regardless of who wins the Autonomous Bonus", inline = True)
    gameEmbed.set_footer(text="More info at https://www.vexrobotics.com/vexedr/competition/vrc-current-game")
    gameEmbed.set_image(url = "https://www.vexrobotics.com/media/wysiwyg/Artboard_7_copy-100.jpg")
    await ctx.send(embed = gameEmbed) #Change

@bot.command(pass_context=True)
async def links(ctx): ### Links

    linkEmbed = discord.Embed(
                title = "Useful Links",
                description= "Some more useful links",
                color = discord.Color.orange()
            )
    linkEmbed.add_field(name = "Spin Up Video Introduction: ", value = "https://www.youtube.com/watch?v=wIZgvVDZc2Y")
    linkEmbed.add_field(name = "Jenison Robotics Website: ", value = "https://www.jenisonrobotics.org/")
    linkEmbed.add_field(name = "Jenison Robotics Youtube: ", value = "https://www.youtube.com/jenisonrobotics/")
    linkEmbed.add_field(name = "Jenison Robotics Twitter: ", value = "https://twitter.com/JenisonRobotics")
    linkEmbed.add_field(name = "Jenison Robotics Facebook: ", value = "https://facebook.com/JenisonRobotics")
    linkEmbed.set_thumbnail(url = "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.clipartbest.com%2Fcliparts%2FnTX%2Fog7%2FnTXog78qc.png&f=1&nofb=1")
    await ctx.send(embed = linkEmbed) #Change

@bot.command(pass_context=True)
async def help(ctx): ### Help

    helpEmbed = discord.Embed(
                title = "Command List for Vex Bot",
                description= "Bot made by agentAMP#9671",
                color = discord.Color.red()
            )
    helpEmbed.add_field(name = ",world [School Level] [# of teams (Automatically set to 10)]", value = "Displays the top teams of the world! ,world mid 15 will show the top 15 Middle School teams of the World.", inline = True)
    helpEmbed.add_field(name = ",usa [School Level] [# of teams (Automatically set to 10)]", value = "Displays the top teams of the USA! ,usa high 21 will show the top 21 High School teams of the USA.", inline = True)
    helpEmbed.add_field(name = ",state [School Level] [# of teams (Automatically set to 10)]", value = "Displays the top teams of Michigan! ,mi mid 9 will show the top 9 Middle School teams of Michigan.", inline = True)
    helpEmbed.add_field(name = ",rank [Team Number] [high/h/mid/m] [state, country, world]", value ="Shows the certain rank of the selected team in the selected sectional. ,rank 1234A h country will show the rank of 1234A in the USA.", inline = True)
    helpEmbed.add_field(name = ",game", value ="Gives a picture of the field and the definition of the game.", inline = True)
    helpEmbed.add_field(name = ",links", value ="Shows more useful links.", inline = True)
    helpEmbed.set_footer(text="Version 3")
    await ctx.send(embed = helpEmbed) #Change

bot.run("") #Do not share with anyone else!
 
