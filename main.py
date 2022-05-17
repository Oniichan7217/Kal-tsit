import discord
import os #for hiding my bot token
import keep_alive 
import requests
import json 
from discord.ext import commands

client = discord.Client()

@client.event
async def on_ready():
    print('{0.user} is already online'.format(client))

client = commands.Bot(command_prefix='!')

client.remove_command('help') #because this library already has help command. To customize I need to remove help command.

#Commands section

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = "Archetto command",
    description="All bot commands listed below.",
    color = discord.Color.blue(),
    author="Phudit"
    )   
  embed.set_thumbnail(url="https://bit.ly/3sh3Qsp")
  embed.add_field(name="!help",value="To see all bot command",inline=False) #inline make embed massage into row by row if It's false.
  embed.add_field(name="!serverinfo",value="Display server information.",inline=False)
  embed.add_field(name="!weather + city or country",value="Display weather information",inline=False)
  await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
  name= ctx.guild.name
  icon = ctx.guild.icon_url
  membercount =ctx.guild.member_count
  embed = discord.Embed(
    title = name,
    color = discord.Color.magenta()
  )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Member Count",value=membercount,inline=False)
  await ctx.send(embed=embed)


with open('api_key.json', 'r') as f:
    api_key = json.load(f)
 
@client.command()
@commands.cooldown(2, 1, commands.BucketType.default)
async def weather(ctx, city, country = None):
 
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={api_key['Weather_report']}")
    json_data = r.json()
 
    weather = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = json_data['main']['temp']
    feels_like = json_data['main']['feels_like']
    temp_min = json_data['main']['temp_min']
    temp_max = json_data['main']['temp_max']
    icon = "http://openweathermap.org/img/wn/" + json_data['weather'][0]['icon'] + "@2x.png"
 
    embed = discord.Embed(
        title="Current Weather",
        description=f"{city.upper()}",
        color=discord.Color.dark_blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name=weather, value=description, inline=False)
    embed.add_field(name="Temperature", value=f" {temp}\u2103", inline=True)
    embed.add_field(name="Feels Like", value=f" {feels_like}\u2103", inline=True)
    embed.add_field(name="Min Temperature", value=f" {temp_min}\u2103", inline=True)
    embed.add_field(name="Max Temperature", value=f" {temp_max}\u2103", inline=True)
  
    await ctx.send(embed=embed)
 
 
@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Not a valid city or Country.")


keep_alive.keep_alive()
client.run(os.getenv('Token'))
