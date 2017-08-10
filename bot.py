import discord
import asyncio
import logging
import time
import datetime
import threading as thr

try:
    with open('tokenid.txt') as f:
        token = f.read()
except IOError:
    print('Error with token file, Client may not launch')
    token = ''

# logging module: Critical, Error, Warning, Info, and Debug
logging.basicConfig(level=logging.INFO)

# Global Variables
prevchannel = ''
isPolling = False
pollDict = {}
startTime = ''
# client naming
client = discord.Client()


# Join event
@client.event
async def on_ready():
    global startTime
    global f
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-' * len(client.user.id))
    startTime = time.time()
    f.close()

async def respond(message):
    await client.add_reaction(message, 'Jebaited:288754567347175424')

async def poll(message):
    global pollDict
    if any(k in str(message.content) for k in pollDict):
        pollDict[str(message.content)] += 1
    else:
        pass


def get_time(currenttime, starttime):
    uptime = currenttime - starttime
    hours = uptime / 3600
    minutes = (uptime % 3600) / 60
    seconds = uptime % 60
    return str(int(hours)) + 'h ' + str(int(minutes)) + 'm ' + str(int(seconds)) + 's'


@client.event
async def on_message(message):
    # global variable usage
    global isPolling
    global prevchannel
    global startTime
    global pollDict

    # Logging
    ts = time.time()
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    if str(message.channel) != prevchannel:
        print('\nIn Channel: ' + str(message.channel) + '\n' + ('-' * 30))
        prevchannel = str(message.channel)
    print(str(message.author) + '(' + stamp + ')' + ': ' + message.content)

    # Commands
    if message.author == client.user:
        pass  # ignores self text
    else:
        # Poll
        if isPolling:
            await poll(message)

            # test command
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
            await respond(message)

            # returns a command list for built in commands
        elif message.content.startswith('!commands'):
            await client.send_message(message.channel, 'List of commands includes: \n!test\n!sleep\n!gn\n!commands')
            await respond(message)

            # poll command (can compound into one function)
        elif message.content.startswith('!poll') and not isPolling:
            isPolling = True
            pollList = str(message.content).split()
            pollList.pop(0)
            pollString = ''
            for i in (0, len(pollList) - 1):
                pollString = pollString + pollList[i] + ' '
            await client.send_message(message.channel, 'To vote, simply enter your choice: ' + pollString)
            # pollArg = pollList[0]
            for i in range(0, len(pollList)):
                pollDict[str(pollList[i])] = 0
            await respond(message)

            # poll command error handling
        elif message.content.startswith('!poll') and isPolling:
            await client.send_message(message.channel, 'Stop the current poll to start a new poll hiss!')
            await respond(message)

            # stop poll command
        elif message.content.startswith('!stoppoll') and isPolling:
            isPolling = False
            pollResultString = ''
            i = 0
            for items in pollDict:
                pollResultString = pollResultString + '\n' + str(items) + ' received ' + str(pollDict[items]) + ' votes'
                i += 1
            await client.send_message(message.channel, '```Poll results:' + str(pollResultString) + '```')
            pollDict = {}

            # !fprint command prints from local file, if exists
        elif message.content.startswith('!print'):
            fi = str(message.content).split()
            fi.pop(0)
            fileString = ''
            with open(fi) as fil:
                pass

            # bot diagnostic command
        elif message.content.startswith('!info'):
            serversize = str(len(set(client.get_all_members())))
            threads = thr.active_count()
            uptime = get_time(time.time(), startTime)
            await client.send_message(message.channel, '```' + 'I AM SnekBot!\n' + ('-' * 14) + '\nCurrently serving: ' + serversize + ' hoomans.' + '\nActive Threads: ' + str(threads) + '\nUptime: ' + uptime + '```')
            await respond(message)

            # set playing command
        elif message.content.startswith('!setplay'):
            gamePlayinglist = str(message.content).split()
            gamePlayinglist.pop(0)
            gamestr = gamePlayinglist[0] + ' '
            try:
                for i in range(1, len(gamePlayinglist)):
                    gamestr = gamestr + gamePlayinglist[i] + ' '
            except IndexError:
                gamestr = ''
            await client.change_presence(game=discord.Game(name=gamestr))
            await respond(message)

            # simple text return command
        elif message.content.startswith('!gn'):
            await client.send_message(message.channel, 'Good Night Everybody!')
            await respond(message)

            # sleeper thread test
        elif message.content.startswith('!remindme'):
            remindString = str(message.content).split()
            remindString.pop(0)
            remindTime = remindString.pop(0)
            await client.send_message(message.channel,"I will remind " + str(message.author) + '\n' + " ".join(remindString) + ' in: ' + remindTime + ' minutes')
            await asyncio.sleep(int(remindTime) * 60)
            await client.send_message(message.channel, " ".join(remindString) + '!')
            await respond(message)

            # disconnect command
        elif message.content.startswith('!getmyshotty'):
            await client.send_message(message.channel, 'AHHH!')
            await client.close()
            if client.is_closed:
                print('Successfully closed')
            else:
                print('wtf')
# end on_message

client.run(token)
