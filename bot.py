import discord
from dispatcher import dispatcher
import random

d = dispatcher()

d.register_cmd('!roll', lambda msg: msg.channel.send(random.randint(1,20)))

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'logged on as {self.user}!')

    async def on_message(self,message):
        print(f'Message from {message.author}: {message.content}')
        await d.dispatch_cmd(message)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
with open('.secret','r') as sec:
    secret = sec.readline()[:-1]
    client.run(secret)