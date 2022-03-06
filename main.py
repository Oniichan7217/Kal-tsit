import discord
import os
import keep_alive

client = discord.Client()


@client.event
async def on_ready():
    print('{0.user} is already online'.format(client))


@client.event
async def on_message(message):
    if message.content == '!k Greeting':
        await message.channel.send("Doctor.")
    if message.content == '!k Tap':
        await message.channel.send("What are you doing?")
    if message.content == '!k Trust Tap':
        await message.channel.send(
            "You seem to have grown used to your own work and responsibility. You\'ve become much like a leader."
        )
    if message.content == '!k Idle':
        await message.channel.send("Are you awake, or still in a dream.")
    if message.content == '!k Appointed as Assistant':
        await message.channel.send(
            "Doctor, please sit. I\'m just here to check up on your body\'s state, so don\'t be so stiff. If there are any irregularities, please tell me in full. Meaning? We\'ll set aside what it means to Rhodes Island for now. To me, the meaning it holds is quite significant.")
    if str(message.content).lower() == "cunny":
        await message.add_reaction("😭") #Can use unicode of emoji too but I just simply copy the emoji I want in the code


      

        

keep_alive.keep_alive()
client.run(os.getenv('Token'))
