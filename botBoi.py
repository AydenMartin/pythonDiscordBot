import discord
import random
import os


foodPlaces = ['arby','bosnia','mcdonald','tacobell','pizza','subway','culvers','jimmy']

menuGang = {'arby': ['gobbler','mountain','beefboi','sliders'],
            'bosnia': ['gyro','borger','fries'],
            'tacobell':['quesodilla','steak quesorita','chicken melt','tacos','big box'],
            'mcdonald':['bigmac','cheesborger','chicken sandy','double patty'],
            'pizza': ['uhhh idk make your own bish'],
            'subway':['steakboi','ham and egg','ham','meatball','italian','idk make ur own'],
            'culvers':['random culver burger here'],
            'jimmy':['random jimmy sub here']}

def clearFile(id):
    if os.path.exists(os.getcwd() + '\\Users\\' + str(id) + '\\foodList'):
            f = open(os.getcwd() + '\\Users\\' + str(id) + '\\foodList','w+')
            f.truncate()
            f.close()
            
    else:
            return


class MyClient(discord.Client):



    async def on_ready(self):
        print('Logged on as', self.user)
        if(os.path.exists(os.getcwd()+'\\Users')) == False:
            os.mkdir(os.getcwd()+'\\Users')
        if (os.path.exists(os.getcwd() + '\\Server')) == False:
            os.mkdir(os.getcwd() + '\\Server')
        for i in self.users:
            customUser = os.getcwd()+'\\Users' + '\\' + str(i.id)
            if (os.path.exists(customUser)) != True:
                os.mkdir(customUser)
        for i in self.guilds:
            serverDir = os.getcwd() + '\\Server' + '\\' + str(i.id)
            if (os.path.exists(serverDir)) != True:
                os.mkdir(serverDir)



    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
           return

        if message.content == 'serverTest':
            self.onServer()

        if message.content == 'botOff':
            self.close()

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == "food???":
            place = random.choice(foodPlaces)
            food = random.choice(menuGang[place])
            string = str(place + "  " + food)
            await message.channel.send(string)

        if str(message.content).startswith('myfood'):
            foodFolder = os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList'

            if message.content == 'myfood clear':

                clearFile(message.author.id)
                await message.channel.send("your file has been cleared")
                return
            if (os.path.exists(foodFolder)) != True:
                textFile = open(str(foodFolder), 'w')
                textFile.close()
                string = 'your food list is empty rn user ' \
                         + str(message.author.id) \
                         + ' to add food use command addfood'
                await message.channel.send(string)
                return
            else:
                foodFolder = open(os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList', 'r')
                parse = foodFolder.readline(100)
                parse = parse.split(';')
                restaurants = {}
                print(parse)
                string = "your current restuarants and food are: "
                for i in range(0,len(parse)-1):
                    menu = parse[i].split(',')
                    string += str(menu) + '\n'
                    restaurants[menu[0]] = menu

                print(restaurants)
                foodFolder.close()

            await message.channel.send(string)


            return

        if str(message.content).startswith('addfood'):
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
                        unwantedchars = ['\'','[',']',' ']
                        foodFolder2 = open(os.getcwd() + '\\Users\\' + str(message.author.id) + '\\foodList', 'r+')
                        strmsg.pop(0)
                        newstring = str(menu + list(set(strmsg)-set(menu)))

                        for l in unwantedchars:
                            newstring = newstring.replace(l,'')
                        parse[i] = newstring
                        newfile = ''

                if found == True:
                    for i in range(0,len(parse)-1):
                        menu = parse[i].split(',')
                        for m in menu:
                            if m != menu[len(menu)-1]:
                                newfile += m + ','
                            else:
                                newfile += m
                        newfile += ';'

                    foodFolder2.write(newfile)
                    foodFolder2.close()
                    await message.channel.send("succesfully added")
                    return


                addition = ''
                for i in range(1,len(strmsg)):
                    if(i != len(strmsg)-1):
                        addition += strmsg[i] + ','
                    else:
                        addition += strmsg[i] + ';'
                print(addition)
                foodFolder.write(addition)
                foodFolder.close()
                await message.channel.send("succesfully added")

        if str(message.content).startswith('botHelp') and len(str(message.content).split(' ')) < 3:
            if(message.content == 'botHelp myfood'):
                await message.channel.send('the myfood command by itself gives a lsit of all restuarants'
                                           'and food currently on your list \n'
                                           '\'myfood clear\' will empty your list \n'
                                           '\'myfood random\' will choose a random restaurant '
                                           'and food item from your lists')
                return
            if(message.content == 'botHelp addfood'):
                await message.channel.send("please add restaurant to add, in this format "
                                           "\'addfood restaurant food1 food2\'")
                return
            await message.channel.send("ping,food???,myfood,addfood \n "
                                       "to find out more information on a specific command do "
                                       "\' botHelp command\'")


def Main():
    client = MyClient()

    client.run('Token')

Main()
