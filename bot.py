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
pin = ''
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
    print('-' * len(str(client.user.id)))
    startTime = time.time()
    f.close()
    print('Token File Closed Successfully')


async def respond(message):
    await message.add_reaction('☑')
    pass


async def poll(message):
    global pollDict
    try:
        if any(k in str(message.content) for k in pollDict):
            pollDict[str(message.content)] += 1
        else:
            pass
    except KeyError:
        pass


def get_time(currenttime, starttime):
    uptime = currenttime - starttime
    hours = uptime / 3600
    minutes = (uptime % 3600) / 60
    seconds = uptime % 60
    return str(int(hours)) + 'h ' + str(int(minutes)) + 'm ' + str(int(seconds)) + 's'

# future function to listen to console commands


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

    if message.type == discord.MessageType.pins_add:
        await message.delete()
        print('Pin Notification Deleted')

    # Commands
    if message.author == client.user:
        global pin
        if message.content.startswith('To'):
            pin = message
            await pin.pin()

        elif message.content.startswith('```Poll'):
            await pin.unpin()

    else:
        # Poll
        if isPolling:
            await poll(message)

            # test command
        if message.content.startswith('!test'):
            counter = 0
            tmp = await message.channel.send('Calculating messages...')
            async for log in message.channel.history(limit=100):
                if log.author == message.author:
                    counter += 1
            await tmp.edit(content=f'You have {counter} messages.')
            await respond(message)

            # returns a command list for built in commands
        elif message.content.startswith('!commands'):
            commandString = '```!test - returns length of a message log gathered from a message channel (default function in example)\n' \
                            '!commands - returns a list of commands available to user from a file of all commands (not complete)\n' \
                            '!poll - takes in x number of arguements and converts to a unique dictionary and accumulates sums for each key\n' \
                            '!stoppoll - stops current poll and displays results\n' \
                            '!fprint - takes in the name of a file and prints its contents (not complete)\n' \
                            '!info - shows diagnostic bot information (Name,Server Size, Channel, Server, Uptime)\n' \
                            '!setplay - sets playing to (args)\n' \
                            '!gn - sends message \'Good Night Everybody!\'\n' \
                            '!remindme - takes int x minutes and string and notifies user in x amount of minutes of string\n' \
                            '!getmyshotty - disconnect command (note terminates all bot processes) ```'
            await message.channel.send(f'List of commands includes: \n {commandString}')
            await respond(message)

            # poll command (can compound into one function)
        elif message.content.startswith('!poll') and not isPolling:
            isPolling = True
            pollList = str(message.content).split()
            pollList.pop(0)
            await message.channel.send(f'To vote, simply enter your choice {" ".join(pollList)}')
            # pollArg = pollList[0]
            for i in range(0, len(pollList)):
                pollDict[str(pollList[i])] = 0
            await respond(message)

            # poll command error handling
        elif message.content.startswith('!poll') and isPolling:
            await message.channel.send('Stop the current poll to start a new poll!')
            await respond(message)

            # stop poll command
        elif message.content.startswith('!stoppoll') and isPolling:
            isPolling = False
            pollResultString = ''
            i = 0
            for items in pollDict:
                pollResultString = pollResultString + '\n' + str(items) + ' received ' + str(pollDict[items]) + ' votes'
                i += 1
            await message.channel.send(f'```Poll Results: {pollResultString}```')
            pollDict = {}

            # !fprint command prints from local file, if exists
        elif message.content.startswith('!print'):
            fi = str(message.content).split()
            fi.pop(0)
            fileString = ''
            with open(fileString) as fil:
                pass

            # bot diagnostic command
        elif message.content.startswith('!info'):
            serversize = str(len(set(client.get_all_members())))
            name = 'I AM Snek🐍!\n'
            threads = thr.active_count()
            uptime = get_time(time.time(), startTime)
            channelname = str(message.channel)
            servername = str(message.guild)
            await message.channel.send(f'```'
                                       f'{"-" * 14}\n'
                                       f'Currently harrasing {serversize} people\n'
                                       f'Active Threads: {str(threads)}\n'
                                       f'Uptime: {uptime}\n'
                                       f'Current Channel: {channelname}\n'
                                       f'Server: {servername}'
                                       f'```')
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
            await client.change_presence(status=discord.Game(name=gamestr))
            await respond(message)

            # simple text return command
        elif message.content.startswith('!gn'):
            await message.channel.send('Good Night Everybody!')
            await respond(message)

            # remindme command sets a reminder in x minutes
        elif message.content.startswith('!remindme'):
            remindString = str(message.content).split()
            remindString.pop(0)
            remindTime = remindString.pop(0)
            await message.channel.send(f'I will remind {message.author.display_name}\n'
                                       f'{" ".join(remindString)} in {remindTime} minutes')
            await asyncio.sleep(int(remindTime) * 60)
            await message.channel.send(f'{message.author.mention} {" ".join(remindString)}!')
            await respond(message)

            # disconnect command
        elif message.content.startswith('!getmyshotty'):
            await message.channel.send('AHHH!')
            await client.close()
            if client.is_closed:
                print('Successfully closed')
            else:
                print('wtf')
# end on_message

client.run(token)
