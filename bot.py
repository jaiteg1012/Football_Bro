import discord 
from discord.ext import commands 
from scraper import active_games, get_scores, exercise
from time import sleep 

client = commands.Bot(command_prefix = '.')

@client.event 
async def on_ready():
    print('Bot is ready')



@client.command(aliases=['NFL', 'nfl', 'Football'])
async def football(context):
    games = active_games()
    options = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔼', '🔽', '⏩', '⏪', '⏫', '⏬' ]
    predictions = {'1️⃣': 'Touchdown', '2️⃣': 'Field Goal', '3️⃣': 'Punt', '4️⃣': 'Turnover on Downs', '5️⃣': 'Fumble', '6️⃣' : 'Interception' }
    embed = discord.Embed(title = 'NFL: Active Games', color = discord.Colour.blue())

    game_option = {}
    for game, num in zip(games, options):
        game_option[num] = game


    for game in game_option:
        embed.add_field( name = game_option[game] , value = game, inline = False)
        
    file = discord.File("NFL_Logos/football.png", "football.png")
    embed.set_thumbnail(url = "attachment://football.png")
    message= await context.send(embed=embed, file=file)
    def check(reaction, user): 
            return reaction.emoji in game_option 

    reaction = await client.wait_for('reaction_add', check = check)
   
    await context.send('You are following ' + game_option[reaction[0].emoji])
    
    loop = True 
    total_drives = 0 
    prediction = None 
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

            if(prediction != None):
                    if (predictions[reaction_2[0].emoji] != info[1]):
                        embed =  discord.Embed(title = 'Prediction Wrong', color = discord.Colour.red())
                        embed.add_field( name = 'DO' , value = exercise(), inline = False)
                    else:
                        embed =  discord.Embed(title = 'Prediction Correct', color = discord.Colour.green())
                    await context.send(embed=embed)

            if(drive[1][0:8] == 'End of 4'):
                loop = False
                break

            embed = discord.Embed(title = 'Make your predictions for the next drive', color = discord.Colour.blue())
            for p in predictions: 
                embed.add_field( name = predictions[p] , value = p, inline = False)
            file = discord.File("NFL_Logos/football.png", "football.png")
            embed.set_thumbnail(url = "attachment://football.png")
            prediction = await context.send(file=file, embed=embed)

            def check_prediction(reaction, user):
                return reaction.emoji in predictions 

            reaction_2 = await client.wait_for('reaction_add', check = check_prediction)
            await context.send('Prediction made')

        sleep(60)



   

client.run("{Insert Key}")