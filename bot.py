import discord
from dispatcher import dispatcher
import random
import sys
from unicodedata import lookup
import string

async def add_react(message,name):
    reaction = discord.utils.get(message.guild.emojis,name=name)
    if reaction:
        await message.add_reaction(reaction)

async def add_funny_letters(message, text):
    upper_text = text.upper()
    if any(c not in set(string.ascii_uppercase) for c in upper_text):
        return
    for char in upper_text: 
        await message.add_reaction(lookup(f'REGIONAL INDICATOR SYMBOL LETTER {char}'))

async def gottem_replies(message):
    if any(funny_word in message for funny_word in ['ligma','sugma','chokema']):
        await message.channel.send(funny_word + ' ' + random.choice(['balls','dick','nuts'])+'! :gottem:')

d = dispatcher()
d.register_builtin('!ping', lambda msg: msg.channel.send('pong'))
d.register_builtin('!source', lambda msg: msg.channel.send('https://github.com/mr1337357/discordbot'))
d.register_builtin('!log',lambda msg: print(msg))
d.register_builtin('!reload',lambda msg: sys.exit(0))

d.register_cmd('!roll', lambda msg: msg.channel.send(random.randint(1,20)))
d.register_cmd('!socks', lambda msg: msg.channel.send(random.choice(['UwU','OwO','onii-chan'])),channels = ['programming-socks-gone-wild'])
d.register_cmd('.*(?i)socks.*',lambda msg: add_react(msg,'bonk'),channels = ['^((?!programming-socks-gone-wild).)*$'])
d.register_cmd('.*(?i)js.*', lambda msg: add_funny_letters(msg, 'bad'))
d.register_cmd('.*(?i)\b(ligma|sugma|chokema)\b.*', lambda msg: gottem_replies(msg))
d.register_cmd('.*(?i)socks.*',lambda msg: add_react(msg,'nice'),channels = ['programming-socks-gone-wild'])

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'logged on as {self.user}!')

    async def on_message(self,message):
        if message.author == self.user:
            return
        await d.dispatch_cmd(message)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
with open('.secret','r') as sec:
    secret = sec.readline()[:-1]
    client.run(secret)
