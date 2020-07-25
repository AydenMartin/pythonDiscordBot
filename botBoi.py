"""
Discord bot made by Ayden Martin 2020 and Simon Hillebrands
To use the bot you need to have a discord auth token and a OpenWeatherMap api key
"""

#word of the day https://www.dictionary.com/e/word-of-the-day/


import discord
import random
import os
import requests as r
import time as t
import othello
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations
from sympy.parsing.sympy_parser import implicit_multiplication_application
from sympy.plotting import plot
#import othello

gamesAvail = ['othello','chess','connectfour']

foodPlaces = ['arby', 'bosnia', 'mcdonald', 'tacobell', 'pizza', 'subway', 'culvers', 'jimmy']

menuGang = {'arby': ['gobbler', 'mountain', 'beefboi', 'sliders'],
            'bosnia': ['gyro', 'borger', 'fries'],
            'tacobell': ['quesodilla', 'steak quesorita', 'chicken melt', 'tacos', 'big box'],
            'mcdonald': ['bigmac', 'cheesborger', 'chicken sandy', 'double patty'],
            'pizza': ['uhhh idk make your own bish'],
            'subway': ['steakboi', 'ham and egg', 'ham', 'meatball', 'italian', 'idk make ur own'],
            'culvers': ['random culver burger here'],
            'jimmy': ['random jimmy sub here']}


# uses the OpenWeatherMap site and personal api key, to use this feature you will need to get own api key
def openWeatherMapCall(city,country):
    apikey = 'apikey'
    weather = r.get('http://api.openweathermap.org/data/2.5/weather?q='+city+','+country+'&appid='+apikey)
    data = str(weather.content)
    weather.close()
    unwantedchars = ['b\'','\"','{','[',']','}','\'']
    for d in unwantedchars:
        data = data.replace(d,'')
    data = data.split(',')
    citytime = data[23].split(':')[1]
    time = t.time() + int(citytime)
    time = t.gmtime(time)

    temp = float(data[7].split(':')[2])
    Ftemp = round((temp-273.15) * (9/5) + 32)
    Ctemp = round((temp-273.15))
    description = str(data[4].split(':')[1])
    result = city + ' ' + country +'\n Time(24H): ' + str(time.tm_hour) + ':' + str(time.tm_min) \
             + '\n Fahreinheit: ' + str(Ftemp) + ' Celsius: ' + str(Ctemp)\
             +'\n Description: ' + description
    return result


def define(word):
    sentence = word.split(' ')
    query = "https://www.dictionary.com/browse/"
    for i in range(1,len(sentence)-1):
        query += sentence[i]+'-'
    query += sentence[len(sentence)-1]
    try:
        google = r.get(query)
    except r.exceptions.ConnectionError:
        return("wait a few seconds and try again please, bot had trouble connecting to site")
    except Exception as e:
        print(e)
        return("uhh sumthin went wrong try again pls")

    results = google.text
    google.close()
    if results.find('name=\"description\" content=') > 0:
        resultsBegin = results.find('name=\"description\" content=')
        resultsEnd = results.find(' See more.\">')
        results = results[int(resultsBegin)+28:int(resultsEnd)]
    else:
        results = "could not find this word"

    return results


def clearFile(id):
    f = open(os.getcwd() + '\\Users\\' + str(id) + '\\foodList', 'w+')
    f.truncate()
    f.close()


def chooseRando(dict):
    rest = random.randint(0, len(dict) - 2)
    rest = dict[rest]
    rest = rest.split(',')
    restchoice = random.randint(1, len(rest) - 1)
    return str(rest[0] + ' ' + rest[restchoice])


def listFood(id):
    file = open(os.getcwd() + '\\Users\\' + str(id) + '\\foodList', 'r')
    result = file.read()
    file.close()
    result = result.split(';')
    string = 'your current restaurants are: \n'
    for i in result:
        string += str(i) + '\n'
    return string


def ListGames(author,game):
    game = str(game).lower()
    gameFolder = os.getcwd() + '\\Users\\' + str(author) + '\\games'
    string = ""
    if (os.path.exists(gameFolder)) != True:
        textFile = open(str(gameFolder), 'w+')
        textFile.write("")
        textFile.close()
        return "you currently have no games at all"
    f = open(gameFolder, "r")
    contents = f.read()
    if contents == "":
        return "you currently have no games at all"
    games = contents.split(';')
    for Games in games:
        if Games.startswith(game):
            currentGames = Games.split(',')
            for i in range(1, len(currentGames)):
                string += currentGames[i] + ';'
            string = "These are your current " + game + ' games;' + string
            return string
    return "could not find any current " + game + '\'s that you had going'

def creatGame(id1,id2,game):
    files = []
    newfiles = []
    game = game.strip(' ')

    if os.path.exists(os.getcwd() + '\\Games\\'+ game + str(id1) + 'v' + str(id2)):
        return 2
    if os.path.exists(os.getcwd() + '\\Users\\' + str(id1) + '\\games'):
        files.append(open((os.getcwd() + '\\Users\\' + str(id1) + '\\games'),'r+'))
    else:
        newfiles.append(open((os.getcwd() + '\\Users\\' + str(id1) + '\\games'), 'w'))
    if os.path.exists(os.getcwd() + '\\Users\\' + str(id2) + '\\games'):
        files.append(open((os.getcwd() + '\\Users\\' + str(id2) + '\\games'),'r+'))
    else:
        newfiles.append(open((os.getcwd() + '\\Users\\' + str(id2) + '\\games'),'w'))

    if len(newfiles) != 0:
        for file in newfiles:
            file.write(game + ',game1' + ' ' + str(id1) + 'v' + str(id2)+';')
            file.close()

    for i in files:
        found = False
        contents = i.read()
        type = contents.split(';')
        newcontents = ''
        for n in type:
            inside = n.split(',')
            inside[0] = str(inside[0]).replace(u'\x00', '')
            if inside[0] == game:
                found = True
                gamenumber = len(inside)
                newcontents += n + ',game' + str(gamenumber) + ' '+ str(id1) + 'v' + str(id2) + ';'
            else:
                newcontents += n

        if found == False:
            contents += game + ',game1 ' + str(id1) + 'v'+ str(id2) + ';'
            i.write(contents)
            i.close()
        else:
            i.truncate(0)
            i.write(newcontents)
            i.close()
        f = open(os.getcwd() + '\\Games\\' + game + str(id1) + 'v' + str(id2),'w+')
        f.close()
    return 1

def gameExists(author,game,gamenum):
    if (os.path.exists(os.getcwd() + '\\Users\\' + str(author) + '\\games')):
        f = open(os.getcwd() + '\\Users\\' + str(author) + '\\games')
        contents = f.read()
        f.close()
    contents = contents.split(';')
    for n in contents:
        if n.startswith(game):
            for i in n.split(','):
                if i.startswith('game'+str(gamenum)):
                    return i.split(' ')[1]
    return False



class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        if (os.path.exists(os.getcwd() + '\\Users')) == False:
            os.mkdir(os.getcwd() + '\\Users')
        if (os.path.exists(os.getcwd() + '\\Server')) == False:
            os.mkdir(os.getcwd() + '\\Server')
        if (os.path.exists(os.getcwd() + '\\Games')) == False:
            os.mkdir(os.getcwd() + '\\Games')
        for i in self.users:
            customUser = os.getcwd() + '\\Users' + '\\' + str(i.id)
            if (os.path.exists(customUser)) != True:
                os.mkdir(customUser)
        for i in self.guilds:
            serverDir = os.getcwd() + '\\Server' + '\\' + str(i.id)
            if (os.path.exists(serverDir)) != True:
                os.mkdir(serverDir)

    async def on_message(self, message):
        # don't respond to ourselves

        text = str(message.content)
        if message.author == self.user:
            return

        if text.lower().__contains__("bosnia"):
            emoji = r'🇧🇦'
            await message.add_reaction(emoji)

        # if message.author == message.guild.owner and str(message.content).startswith('daily channel')
        # and len(str(message.content).split(' ')) == 3:
        #     channel = message.content.split(' ')[2]
        #     channels = message.guild.channels
        #     channelFound = False
        #     print(channel)
        #     for i in channels:
        #         print(i)
        #         if i == channel:
        #             channelFound = True
        #     if channelFound == True:
        #         await message.channel.sent('found channel')
        #         # if (os.path.exists(os.getcwd() + '\\Server\\' + str(message.guild) +'\\settings')) == False:
        #         #     file = open(os.getcwd() + '\\Server\\' + str(message.guild) +'\\settings','w+')
        #         #     file.write("daily_word:"+ channel)
        #         #     file.close()
        #         # else:
        #         #     file = open(os.getcwd() + '\\Server\\' + str(message.guild) +'\\settings','a+')
        #     else:
        #         await message.channel.send("could not find that channel")

        if text == 'ping':
            await message.channel.send('pong')

        if text.startswith('define') and len(text.split(' ')) >= 2:
            await message.channel.send(define(text))

        if text.startswith('weather') and len(text.split(' ')) == 3:
            string = str(message.content).split(' ')
            weather = openWeatherMapCall(string[1],string[2])
            await message.channel.send(weather)

        if text.startswith('!game'):
            if len(text.split(' ')) == 1:
                string = 'the current games available are: \n'
                for i in gamesAvail:
                    string += i + '\n'
                await message.channel.send(string)
            if len(text.split(' ')) == 2:
                result = ListGames(message.author.id,str(message.content).split(' ')[1])
                await message.channel.send(result)
            if len(text.split(' ')) > 2:
                await message.channel.send('to use this command do \n'
                                           '\'!game\' or \n'
                                           '\'!game (game of choice)\'')

        if message.content == "food???":
            place = random.choice(foodPlaces)
            food = random.choice(menuGang[place])
            string = str(place + "  " + food)
            await message.channel.send(string)

        if text.startswith('!othello') and len(text.split(' ')) == 3:
            commands = text.split(' ')
            file = 'othello'
            if commands[1].isdigit():
                gamenum = commands[1]
            else:
                await message.channel.send('please type in a valid game\n'
                                           '\'othello (number) (letter)(number)\', EX: othello 1 f6 etc')
                return

            if commands[2][0].isalpha() and commands[2][1].isdigit():
                move = commands[2]
                othello.updateGame(move)
                await message.channel.send(file=discord.File('boardState.png'))
            else:
                await message.channel.send('please type in a valid move\n'
                                           '\'(letter)(number)\', EX: f5,g3,etc')
                return
            game = gameExists(message.author.id,'othello',gamenum)
            if game == False:
                await message.channel.send('could not find that game, type '
                                           '\'!game\' to get your current games')
                return
            else:
                print('uwu')
                file += game
                print(file)
                #othellogame = othello




        if text.startswith('!challenge'):
            commands = text.split(' ')
            if len(commands) == 1:
                await message.channel.send("challange is a function to send game challagnes such as chess and othello"
                                           "to another player\n"
                                           "To use challange do it like this\n "
                                           "\'!challange game Userid/@user\'")
                return
            if len(commands) != 3:

                await message.channel.send("To use challange do it like this\n "
                                           "\'!challange game Userid/@user\'")
                return
            if len(commands) == 3:
                if len(message.mentions) == 0:
                    await message.channel.send("To use challange do it like this\n "
                                               "\'!challange game Userid/@user\'")
                    return

                for i in gamesAvail:
                    if commands[1] == i:
                        result = creatGame(message.author.id,message.mentions[0].id,commands[1])
                        if(commands[1] == 'othello'):
                            othello.startGame(message.author.id,message.mentions[0].id)
                            await message.channel.send(file=discord.File('boardState.png'))
                        if result == 1:
                            await message.channel.send("succesfully made challange\n"
                                                       "to start the game do "
                                                       "!(yourchosengame) (gamenumber) (move)")
                        if result == 2:
                            await message.channel.send("You have a " + str(commands[1]) +
                                                       ' game with that user active right now')
                        return

                await message.channel.send("we currently do not have that game, to get a list of our games use "
                                               "\n \'!game\'")

        if text.startswith('myfood'):

            # makes sure you dont open a file that doesnt exist, creates if no exist
            foodFolder = os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList'
            if (os.path.exists(foodFolder)) != True:
                textFile = open(str(foodFolder), 'w')
                textFile.close()

            # runs a function to clear the users food file
            if message.content == 'myfood clear':
                clearFile(message.author.id)
                await message.channel.send("your file has been cleared")
                return

            # runs a function to choose a random restaurant and item from the users food list
            if message.content == 'myfood random':
                f = open(foodFolder, 'r')
                contents = f.read()
                f.close()
                contents = contents.split(';')
                choice = chooseRando(contents)
                await message.channel.send(choice)
                return

            # prints current items in users food file, only runs this section when message is 'myfood'
            listresult = listFood(message.author.id)
            await message.channel.send(listresult)
            return

        if text.startswith('addfood'):
            if os.path.exists(os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList'):
                foodFolder = open(os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList', 'r+')
            else:
                foodFolder = open(os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList', 'a+')

            parse = foodFolder.read()
            parse.strip('')
            parse = parse.split(';')
            strmsg = str(message.content).split(' ')

            if len(strmsg) == 1:
                await message.channel.send("please add restaurant to add, in this format "
                                           "\'addfood restaurant food1 food2\' \n"
                                           "or to clear file use \'myfood clear\'")
                return

            elif len(strmsg) == 2:
                for i in range(0, len(parse) - 1):
                    menu = parse[i].split(',')
                    print(menu)
                    if menu[0] == strmsg[1]:
                        await message.channel.send("restaurant is already in the list")
                        return
                text = strmsg[1] + ';'
                foodFolder.write(text)
                await message.channel.send("restaurant added to list")

            else:
                found = False
                for i in range(0, len(parse) - 1):
                    menu = parse[i].split(',')

                    if menu[0] == strmsg[1]:
                        found = True
                        foodFolder.close()
                        unwantedchars = ['\'', '[', ']', ' ']
                        foodFolder2 = open(os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList', 'r+')
                        strmsg.pop(0)
                        newstring = str(menu + list(set(strmsg) - set(menu)))

                        for l in unwantedchars:
                            newstring = newstring.replace(l, '')
                        parse[i] = newstring
                        newfile = ''

                if found == True:
                    for i in range(0, len(parse) - 1):
                        menu = parse[i].split(',')
                        for m in menu:
                            if m != menu[len(menu) - 1]:
                                newfile += m + ','
                            else:
                                newfile += m
                        newfile += ';'

                    foodFolder2.write(newfile)
                    foodFolder2.close()
                    await message.channel.send("succesfully added")
                    return

                addition = ''
                for i in range(1, len(strmsg)):
                    if (i != len(strmsg) - 1):
                        addition += strmsg[i] + ','
                    else:
                        addition += strmsg[i] + ';'
                print(addition)
                foodFolder.write(addition)
                foodFolder.close()
                await message.channel.send("succesfully added")

        if text.replace(' ','').startswith('y=') and message.author != self.user and len(text) > 2:
            msg = str(message.content).replace(' ','')
            msg = msg.replace('^','**')

            eq = msg[2:]
            try:
                transformations = (standard_transformations + (implicit_multiplication_application,))
                y = parse_expr(eq, transformations=transformations)
            except Exception as e:
                print(e)
                return
            p1 = plot(y, show=False)
            backend = p1.backend(p1)
            backend.process_series()
            backend.fig.savefig('graph.png', dpi=300)
            await message.channel.send(file=discord.File('graph.png'))
            return

        if text.startswith('botHelp') and len(text.split(' ')) < 3:
            if (message.content == 'botHelp myfood'):
                await message.channel.send('the myfood command by itself gives a lsit of all restuarants'
                                           'and food currently on your list \n'
                                           '\'myfood clear\' will empty your list \n'
                                           '\'myfood random\' will choose a random restaurant '
                                           'and food item from your lists')
                return
            if (message.content == 'botHelp addfood'):
                await message.channel.send("To add restuarant, please do it in this format "
                                           "\'addfood restaurant food1 food2\'")
                return
            if (message.content == 'botHelp weather'):
                await message.channel.send("To find the weather, please do it in this format"
                                           "\'weather city country\' please dont put spaces in city or country name")
            await message.channel.send("ping,food???,myfood,addfood \n "
                                       "to find out more information on a specific command do "
                                       "\' botHelp command\'")


def Main():
    client = MyClient()

    client.run('NzI4NzY1OTI2MDY1MDQ1NTQ0.XxjQog.KOgb0OZ9sAjJUU3X0BLLXK68zG4')


Main()