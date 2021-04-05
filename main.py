# bot.py
import discord
from discord.ext import commands
from urllib.request import urlopen

from bs4 import BeautifulSoup
import grequests
import requests 
import time
from soup_functions import * #look i can write tho

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=['bf!', 'Bf!', 'bF!', 'BF!'], intents=intents)

# for the soup
def fixText(text):
    if text.find("(") != -1:
        return text[0:text.find("(")]
    return text
def clearEmpty(array):
    fixedArray = []
    #stringArray = []
    for x in range(len(array)):
        if array[x].get_text() != "":
            if array[x].get_text() not in fixedArray:
                #stringArray.append(array[x].get_text())
                fixedArray.append(array[x].get_text())
    return fixedArray
def getEvents(Events):
    eventObj = []
    for x in range(len(Events)):
        #print(Events[x].find("strong").get_text())
        if(len(clearEmpty(Events[x].find_all("strong"))) > 0):
            event = clearEmpty(Events[x].find_all("strong"))[0]
            eventObj.append(fixText(event))
            dateBold = clearEmpty(Events[x].find_all("b"))
            dateStrong = clearEmpty(Events[x].find_all("strong"))
            if(len(dateStrong) < 2):
                if(dateBold):
                    eventObj.append(dateBold[0])
                else:
                    eventObj.append("not found")
            else:
                #print(dateStrong[1].get_text())
                eventObj.append(dateStrong[1])
    return eventObj

# bot starts
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    #thien's thing:
    for guild in client.guilds:
        print(guild.name)
        text_channel_list = []
        channelname = []
        for channel in guild.channels: #getting all channels in the servers
            print(str(channel.name) + " type: " + str(channel.type)) 
            if str(channel.type).lower() == 'text': #if it's a text channel
                text_channel_list.append(channel) #gets actual channel
                channelname.append(channel.name) #gets channel name
                print(channel.name)
        print(text_channel_list)
        await client.get_channel(text_channel_list[channelname.index("bot-spam")].id).send('Your Best BF is Online') #we've connected to DISCORD!!!!

# help command stuff
client.remove_command("help")
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title = "Help",
        description = "Use bf!help <command> for more information for each command"
    )
    embed.add_field(name="ping", value="pong :)")
    embed.add_field(name="comp", value="competition dates")
    embed.add_field(name="cisco", value="PT modules")
    
    await ctx.send(embed=embed)
@help.command()
async def ping(ctx):
    embed = discord.Embed(
        title = "Ping",
        description = "Sends back a pong. The first command that this bot did. " + 
                      "\nIt is very important, and will not be deleted."
    )
    embed.add_field(name="**Syntax**", value="bf!ping")
    await ctx.send(embed=embed)
@help.command(aliases=['comp', 'dates', 'date', 'comp_dates', 'competition', 'competition_dates'])
async def comps(ctx):
    embed = discord.Embed(
        title = "Competition Dates",
        description = "Gets all of the training and competition rounds and dates from the CyberPatriot website and displays them."
    )
    embed.add_field(name="**Syntax**", value="bf!comp <page #>")
    embed.add_field(name="**Aliases**", value="comp, comps, dates, date, comp_dates, competition, competition_dates")
    await ctx.send(embed=embed)
@help.command(aliases=['pt', 'packet_tracer', 'mods', 'h*ll'])
async def cisco(ctx):
    embed = discord.Embed(
        title = "Cisco",
        description = "Says all of the packet tracer modules that is covered for each round."
    )
    embed.add_field(name="**Syntax**", value="bf!cisco")
    embed.add_field(name="**Aliases**", value="cisco, pt, packet_tracer, mods, h*ll")
    await ctx.send(embed=embed)

# im keeping this
@client.command()
async def ping(ctx):
    await ctx.reply("pong!")

# gets comp dates
@client.command(aliases=['comp', 'dates', 'date', 'comp_dates', 'competition', 'competition_dates'])
async def comps(ctx, *args):
    # remake the soup
    url = "https://www.uscyberpatriot.org/competition/current-competition/competition-schedule"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")

    # get args length
    if not args:
        page_num = 1
    else:
        if int(args[0]) > 2 or int(args[0]) < 1:
            page_num = 1
        else:
            page_num = int(args[0])

    # make the embed
    competition_embed = discord.Embed(
        title=f"Competition Dates:"
    )
    competition_embed.set_thumbnail(url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    competition_embed.set_footer(text=f"Viewing page {page_num} of 2.")

    # flavor the soup
    if page_num == 1: # page 1
        trainEvents = tablebody[0].find_all("tr")
        eventObj = getEvents(trainEvents)
        for x in range(1, int(len(eventObj)/2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)
    else: # page 2
        roundEvents = tablebody[1].find_all("tr")
        eventObj = getEvents(roundEvents)
        for x in range(int(len(eventObj)/2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)

    # send the soup
    await ctx.send(embed=competition_embed)

@client.command(aliases=['pt', 'packet_tracer', 'mods', 'h*ll'])
async def cisco(ctx, *args):

    #stolen
    url = "https://www.uscyberpatriot.org/competition/current-competition/challenges-by-round"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")[1].find_all("tr")

    ##set up some dictionary
    mod_dict = {}
    test_string = ''
    for trCount in range(0, len(tablebody)):
        
        strong = tablebody[trCount].find(lambda tag: tag.name=='td' and "Round" in tag.text)
        
        ##for every <strong> tag that's found
        if strong:
            key = strong.get_text()
            mod_dict[key] = ''
            test_string += '\n' + str(key) #testing 

            ## search trs until next td with strong + round is found
            trMod = trCount + 1
            next_strong = tablebody[trMod].find(lambda tag: tag.name=='td' and "Round" in tag.text)
            
            while not next_strong and trMod < len(tablebody)-1:
            #for trMod in range(trCount + 1, len(tablebody)):

                module = tablebody[trMod].find(lambda tag: tag.name=='td' and "Module" in tag.text)
                ##search until the text in the tr tag has the text "module"
                if module:
                    mod_dict[key] += '\n' +  str(module.get_text())
                    test_string += '\n' +  str(module.get_text())
                    ##add to dictionary
                trMod+=1
                next_strong = tablebody[trMod].find(lambda tag: tag.name=='td' and "Round" in tag.text) #recursion potential
    
    ##for each key in dict... make an embed
    cisco_embed = discord.Embed(
        title=f"cisco mods <3:"
    )
    cisco_embed.set_thumbnail(url="https://www.saashub.com/images/app/service_logos/51/4ef1468caaa3/large.png?1558762812")
    for key in mod_dict.keys():
        cisco_embed.add_field(name=key, value=mod_dict[key], inline=False)

    await ctx.send(embed=cisco_embed)

client.run(TOKEN)