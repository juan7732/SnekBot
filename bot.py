import discord
import asyncio
import logging
import time
import datetime
try:
    with open('tokenid.txt') as f:
        token = f.read()
except IOError:
    print('Error with token file, Client may not launch')
    token = ''
logging.basicConfig(level=logging.INFO)
prevchannel = ''
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-' * len(client.user.id))

async def respond(message):
    await client.add_reaction(message, 'Jebaited:288754567347175424')


@client.event
async def on_message(message):
    # Logging
    # new comment to test
    global prevchannel
    ts = time.time()
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    if str(message.channel) != prevchannel:
        print('\nIn Channel: ' + str(message.channel) + '\n' + ('-' * 30))
        prevchannel = str(message.channel)
    print(str(message.author) + '(' + stamp + ')' + ': ' + message.content)

    # Commands
    if message.author == client.user:
        pass
    else:
            # test command
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit= 100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
            await respond(message)

            # returns a command list for built in commands
        elif message.content.startswith('!commands'):
            await client.send_message(message.channel, 'List of commands includes: \n!test\n!sleep\n!gn\n!commands')
            await respond(message)

            # bot diagnostic command
        elif message.content.startswith('!botinfo'):
            await client.send_message(message.channel, 'I AM SnekBot!\n' + ('-' * 14))
            serversize = str(len(set(client.get_all_members())))
            await client.send_message(message.channel, 'Currently serving: ' + serversize + ' hoomans.')
            await respond(message)

            # set playing command
        elif message.content.startswith('!setplay'):
            gamePlaying = str(message.content)
            gamePlayinglist = gamePlaying.split()
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
        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')
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