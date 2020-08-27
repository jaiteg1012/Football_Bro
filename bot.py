import discord 
from discord.ext import commands 
from scraper import active_games, get_scores
from time import sleep 

client = commands.Bot(command_prefix = '.')

@client.event 
async def on_ready():
    print('Bot is ready')



@client.command(aliases=['NFL', 'nfl', 'Football'])
async def football(context):
    games = active_games()
    options = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔼', '🔽', '⏩', '⏪', '⏫', '⏬' ]
    embed = discord.Embed(title = 'NFL: Active Games', color = discord.Colour.blue())

    game_option = {}
    for game, num in zip(games, options):
        game_option[num] = game


    for game in game_option:
        embed.add_field( name = game_option[game] , value = game, inline = False)
        

    message= await context.send(embed=embed)
    def check(reaction, user): #checks emoji to be one of the required ones
            return reaction.emoji in game_option 

    reaction = await client.wait_for('reaction_add', check = check)
   
    await context.send('You are following ' + game_option[reaction[0].emoji])
    
    loop = True 
    total_drives = 0 
    while loop: 
        print('getting info')
        info = get_scores(game_option[reaction[0].emoji], total_drives)
        if(info != -1):
            for drive in info[1]:
                embed = discord.Embed(title = game_option[reaction[0].emoji] + " "  + info[0], color = discord.Colour.blue())
                file = discord.File("NFL_Logos/" + drive[0] + '.png' , drive[0] + '.png')
                embed.set_thumbnail(url = "attachment://" + drive[0] + '.png')
                embed.add_field(name = 'Result', value = drive[1])
                embed.add_field(name = 'Plays', value = drive[2])
                embed.add_field(name = 'Start', value = drive[3])
                embed.add_field(name = 'Yards', value = drive[4])
                embed.add_field(name = 'Time', value = drive[5])
                total_drives = drive[6]
                await context.send(file=file, embed=embed)
            if(drive[1][0:8] == 'End of 4'):
                loop = False
                break
        sleep(60)



   

client.run("{key}")