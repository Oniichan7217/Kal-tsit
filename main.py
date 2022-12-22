#importing necessary libraries
import discord
import os #for hiding my bot token
import keep_alive
import requests
import json

#importing commands module from discord.ext
from discord.ext import commands

#creating a client object
client = discord.Client()

#event that triggers when the bot is ready
@client.event
async def on_ready():
#printing a message to console indicating that the bot is ready
  print('{0.user} is already online'.format(client))

#creating a Bot object with command prefix as !
client = commands.Bot(command_prefix='!')

#removing the default help command because we will create a custom help command
client.remove_command('help') 

#Commands section

#creating a help command
@client.command()
async def help(ctx):
#creating an embed object
  embed = discord.Embed(
  title = "Archetto command", #title of the embed message
  description="All bot commands listed below.", #description of the embed message
  color = discord.Color.blue(), #color of the embed message
  author="Phudit" #author of the embed message
  )
  #setting the thumbnail image of the embed message
  embed.set_thumbnail(url="https://bit.ly/3sh3Qsp")
  #adding a field to the embed message
  embed.add_field(name="!help",value="To see all bot command",inline=False) #inline make embed massage into row by row if It's false.
  #adding another field to the embed message
  embed.add_field(name="!serverinfo",value="Display server information.",inline=False)
  #adding another field to the embed message
  embed.add_field(name="!weather + city or country",value="Display weather information",inline=False)
  #sending the embed message
  await ctx.send(embed=embed)

#creating a serverinfo command
@client.command()
async def serverinfo(ctx): 
  name= ctx.guild.name #getting the server name
  icon = ctx.guild.icon_url #getting the server icon url
  membercount =ctx.guild.member_count #getting the server member count
  #creating an embed object
  embed = discord.Embed(
    title = name,
    color = discord.Color.magenta()
  )
  embed.set_thumbnail(url=icon) #setting the thumbnail image of the embed message
  embed.add_field(name="Member Count",value=membercount,inline=False) #adding a field to the embed message
  await ctx.send(embed=embed) #sending the embed message

#reading the api key from a json file
with open('api_key.json', 'r') as f:
    api_key = json.load(f)

#creating a weather command
@client.command()
@commands.cooldown(2, 1, commands.BucketType.default)
async def weather(ctx, city, country = None):
  #sending a request to the OpenWeatherMap API to get weather data for the specified city and country
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={api_key['Weather_report']}")
    #converting the response to json format
    json_data = r.json()
    #getting the weather and description from the json data
    weather = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = json_data['main']['temp']
    feels_like = json_data['main']['feels_like']
    temp_min = json_data['main']['temp_min']
    temp_max = json_data['main']['temp_max']
    icon = "http://openweathermap.org/img/wn/" + json_data['weather'][0]['icon'] + "@2x.png"
    #creating an embed object
    embed = discord.Embed(
        title="Current Weather", #title of the embed message
        description=f"{city.upper()}", #description of the embed message
        color=discord.Color.dark_blue() #color of the embed message
    )
    embed.set_thumbnail(url=icon) #setting the thumbnail image of the embed message
    embed.add_field(name=weather, value=description, inline=False) #adding a field to the embed message
    embed.add_field(name="Temperature", value=f" {temp}\u2103", inline=True) 
    embed.add_field(name="Feels Like", value=f" {feels_like}\u2103", inline=True)
    embed.add_field(name="Min Temperature", value=f" {temp_min}\u2103", inline=True)
    embed.add_field(name="Max Temperature", value=f" {temp_max}\u2103", inline=True)
    #sending the embed message
    await ctx.send(embed=embed)
 
#error handling for the weather command 
@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): #if the error is due to the command being on cooldown
        await ctx.send("This command is on cooldown.") #send a message indicating that the command is on cooldown
    elif isinstance(error, commands.CommandInvokeError): #if the error is due to an invalid city or country being specified
        await ctx.send("Not a valid city or Country.") #send a message indicating that the city or country is invalid


#running the bot using the bot's token stored in an environment variable
keep_alive.keep_alive()
client.run(os.getenv('Token'))
