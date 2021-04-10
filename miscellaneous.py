from bot import *
import random
from fish import *
import csv

magic_ball_responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]


@client.command(name="8ball")
async def _8ball(ctx):
    await ctx.reply(random.choice(magic_ball_responses))

@client.command()
async def ping(ctx):
    await ctx.reply("pong!")
    if ctx.message.author.has_role("Leadership"):
        await ctx.reply("AHHHHHH")

@client.command()
async def yeehaw(ctx):
    await ctx.reply("cowbois \🤠")

@client.command()
async def gofish(ctx):
    rand_num = random.randint(0, (len(fish_names) - 1))
    rand_fish = fish_names[rand_num]
    rand_pic = fish_img[rand_num]
    fish_embed = discord.Embed(
        title=f"You caught a {rand_fish} \✨"
    )
    if rand_fish == "Crappie" or rand_fish == "Weakfish":
      fish_embed.add_field(name="please be kind", value="all fish can become a catch with your love and support \🥰", inline=False)
    # file = discord.File("path/to/image/file.png", filename="image.png")
    # fish_embed.set_image(url=f"fish_pics://{rand_pic}.png")
    fish_link = "[all about the " + rand_fish + "](https://fishingbooker.com/fish/" + rand_pic + ")"
    fish_embed.add_field(name="learn more!", value=fish_link, inline=False)
    fish_embed.set_image(
        url=f"https://static.fishingbooker.com/public/images/fish/275x160/{rand_pic}.png")
    await ctx.reply(embed=fish_embed)

client.in_session = False
@client.command()
async def wormie(ctx, *args):
    ubuntu = ["Ubuntu", "ubuntu", "u", "ub"]
    windows = ["Windows", "windows", "w", "win", "Win"]
    pt = ["PT", "pt", "cisco", "packet", "Packet", "Cisco"]
    
    if not client.in_session:
        ##did the user specify an operating system?
        user_os = ""
        if args:
            my_input = str(args[0])
            if my_input in ubuntu:
                user_os = "Ubuntu"
            elif my_input in pt:
                user_os = "PT"
            elif my_input in windows:
                user_os = "Windows"
            else:
                pass
        
        client.in_session = True
        question = ""
        answer = ""
        worm_os = ""

        all_wormies = []
        with open('knowledge_wormies.csv', newline='') as csvfile:
            all_wormies = list(csv.reader(csvfile))

        # file = open("knowledge_wormies.csv")
        # reader = csv.reader(file)
        # lines= len(list(reader))
        
        rand_worm = random.randint(1, (len(all_wormies) - 1))
        row = all_wormies[rand_worm]
        worm_os = row[2]

        if not user_os == "":
            while user_os != worm_os:
                rand_worm = random.randint(1, (len(all_wormies) - 1))
                row = all_wormies[rand_worm]
                worm_os = row[2]
                
            
        question = row[0]
        answer = row[1]

        # with open('knowledge_wormies.csv') as csv_file:
            
        #     csv_reader = csv.reader(csv_file, delimiter=',')
        #     rand_worm = random.randint(1, (len(csv_reader) - 1))
        #     line_count = 0

        #     row = csv_reader[rand_worm]
        #     if line_count == 0:
        #         # print(f'Column names are {", ".join(row)}')
        #         # line_count += 1
        #         line_count+=1
        #     else:
        #         question = row[0]
        #         answer = row[1]
        #         worm_os = row[2]

        question_embed = discord.Embed(
            title=f"Answer correctly and get a worm!"
        )   
        question_embed.set_thumbnail(
            url="https://icon-library.com/images/worm-icon/worm-icon-9.jpg")
        question_embed.add_field(name=worm_os, value=question, inline=False)
        await ctx.reply(embed=question_embed)

        my_answer = ""
        while my_answer != answer and my_answer != "quit":
            my_response = await client.wait_for("message")
            my_answer = my_response.content.lower()
            if my_answer == answer:
                await ctx.reply('you get one knowledge wormie! :worm:')
                client.in_session = False
            elif my_answer == "quit":
                await ctx.reply('better luck next time \🐟')
                client.in_session = False
            else:
                await ctx.reply('quit or try again \✨')