import discord
import bot_response
import database
import fetch_data
import fetch_database
import asyncio
from discord import Embed
import textwrap
import matchup
API_KEY = database.get_json("API_KEY")
selected_champion = None
async def send_stats(message, user_message, is_private, client): #runs everytime a message is received
    try:
        message_split = user_message.split()
        if len(message_split) == 1:
            if user_message == "!help":
                command_options = bot_response.help_output()
                await message.channel.send(embed=command_options)
                return
            elif user_message == "!matchups":
                matchup_options = matchup.match_up_list()
                await message.channel.send(embed=matchup_options)
                return
        elif len(message_split) == 2:
            champion = message_split[1]
            if message_split[0] == "!matchup":
                matchup_output = matchup.match_up_output(champion)
                await message.channel.send(embed=matchup_output)
                return
        elif len(message_split) == 3:
            region, ign = user_message.split()[1:3] #to extract the region and the ign from the message
            if "#" not in ign:
                embed = Embed(
                title=f"Invalid Input",
                description="My guess is you're missing your tag",
                color=0xC8A2C8
                )
                await message.channel.send(embed=embed)
                return
            if isinstance(fetch_data.fetch_id(region, ign, API_KEY), str):
                embed = Embed(
                title=f"Invalid User",
                description="Inputted Riot IGN and Region doesn't exist, maybe you typed it in wrong. If you need help, type !help for a list of commands",
                color=0xC8A2C8
                )
                await message.channel.send(embed=embed)
                return
            output = database.fetch_player(ign, region) #fetches the id associated with the ign and region
            if isinstance(output, str): #checks if player was in database or not
                title = "Player not Detected:"
                description = "Please wait, I'm entering your data in. Should take around 15-20 minutes. Please come back later"
                output = database.fetch_player(ign, region)
            else:
                title = "Updating your data"
                description = "Please wait a few seconds, Loading your data..."
            
            #Change in message (Loading message)
            embed_general = Embed(
            title=f"{title}",
            description=f"{description}",
            color=0xC8A2C8
            )

            loading_message = await message.channel.send(embed=embed_general) if not is_private else await message.author.send("Loading...")
            
            response = bot_response.handle_response(user_message, output) #calls function to handle the command
            if isinstance(response, discord.Embed): #checks if output is embed type
                await loading_message.edit(content=f"Region: {region}, IGN: {ign}", embed=response) #Changes loading message to the output of the handle_response. With text title under content, and sends embed
                
                #Add a reaction to the message
                if not is_private:
                    await loading_message.add_reaction("🎮")
                    await loading_message.add_reaction("🌟")

            else: #if its a string type
                await loading_message.edit(content=response)
        elif len(message_split) == 4:
            embed = Embed(
            title=f"Invalid Input",
            description="My guess is you're seperating your tag. Put your ign and tag together like Zayno#NA1 (!command NA Zayno#NA1)",
            color=0xC8A2C8
            )
            await message.channel.send(embed=embed)
            return
        else:
            embed = Embed(
            title=f"Invalid Input",
            description="Can't Recognize your command. Use !help command to see all available commands",
            color=0xC8A2C8
            )
            await message.channel.send(embed=embed)
            return
    #error handling
    except Exception as e:
        print(e)

async def handle_reaction(reaction, user, client): #handles main pages
    global selected_champion #indicates that you are using global variable
    if user == client.user: #checks if react is from the person who requested the message
        return
    region, ign = reaction.message.content.split()[1], reaction.message.content.split()[3] #seperates region and ign from the text message added on top
    region = region[:2] #seperates region

    if reaction.emoji == "🏠" and reaction.message.author == client.user: #checks the reaction emoji and if its from the person who requested the bots service
        original_embed = bot_response.home_page() #return to home page
        await reaction.message.edit(embed=original_embed) #edits the message to be home page
        await reaction.message.clear_reactions() #clears any reaction
        
        await reaction.message.add_reaction("🎮") #adds reactions
        await reaction.message.add_reaction("🌟") #adds reactions
        return

    if reaction.emoji == "⚔️" and reaction.message.author == client.user: #checks the reaction emoji and if its from the person who requested the bots service
        #Display lane selection page
        embed = discord.Embed(
            title="Select Lane you want to see your matchups on",
            description="1. TOP\n2. JUNGLE\n3. MIDDLE\n4. BOTTOM\n5. SUPPORT",
            color=0xC8A2C8
        )
        react_options = textwrap.dedent("""
        - Wait for all the reacts to be present before making a selection
        - Select a lane using the number reactions to view your lane specific matchup stats
        """)
        embed.set_footer(text=react_options)
        await reaction.message.edit(embed=embed) #changes the message
        await reaction.message.clear_reactions() #clears all the current reactions on

        #Add number reactions for lane selection
        lane_reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣'] #initialize different lane reaction optioons
        await reaction.message.add_reaction("🏠")
        await reaction.message.add_reaction("🌟") #adds to return to the champion averages beginning
        for reaction_emoji in lane_reactions:
            await reaction.message.add_reaction(reaction_emoji) #adds each reaction necessary for the page

        def lane_check(reaction, user):
            return user != client.user and reaction.message.id == reaction.message.id and (
                str(reaction.emoji) in ["🏠", "🌟"] or str(reaction.emoji) in lane_reactions
            )

        try:
            lane_reaction, _ = await client.wait_for('reaction_add', timeout=60.0, check=lane_check) #checks for response
            if lane_reaction == "🏠":
                return
            if lane_reaction == "🌟":
                return
            if lane_reaction.emoji in lane_reactions: #if reaction is in options
                lane_map = {
                    '1⃣': 'TOP',
                    '2⃣': 'JUNGLE',
                    '3⃣': 'MIDDLE',
                    '4⃣': 'BOTTOM',
                    '5⃣': 'SUPPORT'
                }
                selected_lane = lane_map[str(lane_reaction.emoji)] #selected lane
                player_id = database.fetch_player(ign, region) #fetches player
                if isinstance(player_id, str): #checks if player is present in database
                    error_message = f"Error: {player_id}"
                    await reaction.message.channel.send(error_message)
                    return
                data = fetch_database.fetch_matchups(player_id, selected_champion, selected_lane) #fetches all matchups from champion
                data_sorted = sorted(data, key=lambda x: x[4], reverse=True) #sorts by most played champion
                await send_paginated(reaction.message, data_sorted, client, ign, "Matchups") #calls paginated

        except asyncio.TimeoutError:
            await reaction.message.clear_reactions()

        return

    if reaction.emoji in ["🔮", "🃏", "🎮","🌟"] and reaction.message.author == client.user: #checks emojis
        content = reaction.message.content #information from message
        parts = content.split()
        if len(parts) >= 3:
            region = parts[1].split(',')[0]
            ign = parts[3]
        else:
            await reaction.message.channel.send("Error: Unable to retrieve region and IGN.")
            return

        player_id = database.fetch_player(ign, region) #fetch players id
        if isinstance(player_id, str):
            error_message = f"Error: {player_id}"
            await reaction.message.channel.send(error_message)
            return
        
        if reaction.emoji == "🔮":
            data = fetch_database.fetch_rune_averages(player_id, selected_champion)
            data_sorted = sorted(data, key=lambda x: x[4], reverse=True)
            subject = "Runes"
        elif reaction.emoji == "🃏":
            data = fetch_database.fetch_item_all(player_id, selected_champion)
            data_sorted = sorted(data, key=lambda x: x[4], reverse=True)
            subject = "Items"
        elif reaction.emoji == "🎮":
            data = fetch_database.fetch_matches_all(player_id)
            data_sorted = sorted(data, key=lambda x: x[76], reverse=True)
            subject = "Matches"
        elif reaction.emoji == "🌟":
            champs = fetch_database.fetch_champions(player_id)
            data_sorted = sorted(champs, key=lambda x: x[3], reverse=True)
            subject = "Averages"
        await send_paginated(reaction.message, data_sorted, client, ign, subject)

        await reaction.remove(user)
        return

def create_page(info, page, subject):
    #specify column to display
    if subject == "Averages":
        spot = 2
    else:
        spot = 3
    start = (page - 1) * 5
    end = start + 5
    pages = info[start:end]
    description = "\n".join([f"{index + 1}. {item[spot]}" for index, item in enumerate(pages)])
    embed = discord.Embed(
        title=f"{subject} List - Page {page}",
        description=description,
        color=0xC8A2C8
    )
    if subject == "Averages":
        react_options = textwrap.dedent("""
        - Wait for all the reacts to be present before making a selection
        - Select a champion using the number reactions to view your average stats
        """)
    elif subject == "Runes":
        react_options = textwrap.dedent("""
        - Wait for all the reacts to be present before making a selection
        - Select a Rune using the number reactions to view your average stats
        """)
    elif subject == "Items":
        react_options = textwrap.dedent("""
        - Wait for all the reacts to be present before making a selection
        - Select an Item using the number reactions to view your average stats
        """)
    elif subject == "Matchups":
        react_options = textwrap.dedent("""
        - Wait for all the reacts to be present before making a selection
        - Select an Champion using the number reactions to view your average stats against that champion
        """)
    embed.set_footer(text=react_options)
    return embed

def create_page_matches(info, page, subject):
    start = (page - 1) * 5
    end = start + 5
    pages = info[start:end]
    description = "\n".join([
        f"{index + 1}. {item[3]} vs. {item[75]}, Lane: {item[6]}, Result: {'🏆' if item[5] == 'Win' else '❌' if item[5] == 'Lose' else 'Draw'}"
        for index, item in enumerate(pages)
    ])
    embed = discord.Embed(
        title=f"Match History - Page {page}",
        description=description,
        color=0xC8A2C8
    )
    react_options = textwrap.dedent("""
    - Wait for all the reacts to be present before making a selection
    - Select a Match using the number reactions to view your match stats
    - Use the different arrow keys to view different pages
    """)
    embed.set_footer(text=react_options)
    return embed


async def send_paginated(message, info, client, ign, subject):
    global selected_champion #indicate to use global variable
    page = 1
    total_pages = (len(info) + 4) // 5
    #creates desired page
    if subject != "Matches":
        embed = create_page(info, page, subject)
    else:
        embed = create_page_matches(info, page, subject)

    #Edit the original message instead of sending a new one
    await message.edit(embed=embed)
    await message.clear_reactions()
    #Add reactions for pagination and number selection
    if page != 1:
        await message.add_reaction("◀️") 
    await message.add_reaction("🏠")
    await message.add_reaction("▶️")


    async def add_number_reactions():
        numeric_emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
        for i in range(1, 6):
            if i <= len(info) - (page - 1) * 5:
                await message.add_reaction(numeric_emojis[i-1])

    await add_number_reactions() #adds reactions corresponding to number of items per page

    def check(reaction, user): #checks if reaction wasnt added by bot
        numeric_emojis = {
            '1⃣': 1,
            '2⃣': 2,
            '3⃣': 3,
            '4⃣': 4,
            '5⃣': 5
        }
        return user != client.user and reaction.message.id == message.id and (
            str(reaction.emoji) in ["◀️", "▶️", "🏠", "🌟"] or str(reaction.emoji) in numeric_emojis
        )

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #waits for reaction for 60 seconds
            if str(reaction) == "🏠":
                break
            if str(reaction) == "🌟":
                break
            emoji = str(reaction.emoji)
            numeric_emojis = {
                '1⃣': 1,
                '2⃣': 2,
                '3⃣': 3,
                '4⃣': 4,
                '5⃣': 5
            }
            #checks if emoji is numerical
            if emoji in numeric_emojis: #checks if emoji reacted with is in numeric_emojis
                number = numeric_emojis[emoji]
                if 1 <= number <= 5: #checks if its valid number
                    index = (page - 1) * 5 + (number - 1) #calculates correct index
                    if 0 <= index < len(info): #checks within bounds
                        info_snippet = info[index]
                        #checks to output correct one
                        if subject == "Runes":
                            embed = bot_response.rune_output(info_snippet, ign)
                            react_options = textwrap.dedent("""
                            - Wait for all the reacts to be present before making a selection
                            - React to ◀️ to view previous page
                            - React to 🏠 to return to home page
                            """)
                            embed.set_footer(text=react_options)
                        elif subject == "Items":
                            embed = bot_response.item_output(info_snippet, ign)
                            react_options = textwrap.dedent("""
                            - Wait for all the reacts to be present before making a selection
                            - React to ◀️ to view previous page
                            - React to 🏠 to return to home page
                            """)
                            embed.set_footer(text=react_options)
                        elif subject == "Matchups":
                            embed = bot_response.matchups_output(info_snippet, ign)
                            react_options = textwrap.dedent("""
                            - Wait for all the reacts to be present before making a selection
                            - React to ◀️ to view previous page
                            - React to 🏠 to return to home page
                            """)
                            embed.set_footer(text=react_options)
                        elif subject == "Matches":
                            embed = bot_response.match_output(info_snippet, ign)
                            react_options = textwrap.dedent("""
                            - Wait for all the reacts to be present before making a selection
                            - React to ◀️ to view previous page
                            - React to 🏠 to return to home page
                            """)
                            embed.set_footer(text=react_options)
                        elif subject == "Averages":
                            embed, selected_champion = bot_response.champ_averages(info_snippet, ign)
                            react_options = textwrap.dedent("""
                            - Wait for all the reacts to be present before making a selection
                            - React to 🌟 to see your stats on each champion
                            - React to 🔮 to see your stats on each rune
                            - React to 🃏 to see your stats on each item
                            - React to ⚔️ to see your stats on each matchup
                            """)
                            embed.set_footer(text=react_options)

                        await message.edit(embed=embed) #change message

                        #add reacts for averages (going outside of pages so needs to stop)
                        if subject == "Averages":
                            await message.clear_reactions()
                            await message.add_reaction("🏠")
                            await message.add_reaction("🌟")
                            await message.add_reaction("🔮")
                            await message.add_reaction("🃏")
                            await message.add_reaction("⚔️")
                            break
                        #if number is selected, then you select a specific option (might interfere with selecting champion)
                        else:
                            await message.clear_reactions()
                            await message.add_reaction("◀️")
                            await message.add_reaction("🏠")

                        def back_check(reaction, user):
                            return user != client.user and reaction.message.id == message.id and str(reaction.emoji) in ["◀️", "🏠"]
                        try:
                            #checks if its home button
                            back_reaction, _ = await client.wait_for('reaction_add', timeout=60.0, check=back_check) #waits for back
                            if back_reaction:
                                if str(back_reaction) == "🏠":
                                    break
                                embed = create_page(info, page, subject) if subject != "Matches" else create_page_matches(info, page, subject)
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                if page == total_pages:
                                    await message.add_reaction("◀️")
                                    await message.add_reaction("🏠")
                                elif page == 1:
                                    await message.add_reaction("🏠")
                                    await message.add_reaction("▶️")
                                else:
                                    await message.add_reaction("◀️")
                                    await message.add_reaction("🏠")
                                    await message.add_reaction("▶️")
                                await add_number_reactions()
                                await message.remove_reaction(back_reaction, user)
                        except asyncio.TimeoutError:
                            await message.clear_reactions()
                            
            #checks if emoji reaction is directional (change in page)
            elif emoji == "◀️" and page == 1+1:
                page -= 1
                embed = create_page(info, page, subject) if subject != "Matches" else create_page_matches(info, page, subject)
                await message.edit(embed=embed)
                await message.clear_reactions()
                await message.add_reaction("🏠")
                await message.add_reaction("▶️")
                await add_number_reactions()
                await message.remove_reaction(reaction, user)

            elif emoji == "▶️" and page == total_pages - 1:
                page += 1
                embed = create_page(info, page, subject) if subject != "Matches" else create_page_matches(info, page, subject)
                await message.edit(embed=embed)
                
                await message.clear_reactions()
                await message.add_reaction("◀️")
                await message.add_reaction("🏠")
                await add_number_reactions()
                await message.remove_reaction(reaction, user)

            elif emoji == "◀️" and page > 1:
                page -= 1
                embed = create_page(info, page, subject) if subject != "Matches" else create_page_matches(info, page, subject)
                await message.edit(embed=embed)
                await message.clear_reactions()
                await message.add_reaction("◀️")
                await message.add_reaction("🏠")
                await message.add_reaction("▶️")
                await add_number_reactions()
                await message.remove_reaction(reaction, user)
                
            elif emoji == "▶️" and page < total_pages:
                page += 1
                embed = create_page(info, page, subject) if subject != "Matches" else create_page_matches(info, page, subject)
                await message.edit(embed=embed)
                
                await message.clear_reactions()
                await message.add_reaction("◀️")
                await message.add_reaction("🏠")
                await message.add_reaction("▶️")
                await add_number_reactions()
                await message.remove_reaction(reaction, user)
            else:
                break


        except asyncio.TimeoutError:
            await message.clear_reactions()
            break

def run_discord_bot():
    TOKEN = database.get_json("token")
    intents = discord.Intents.default() #Inititializes with basic intents (basic events)
    intents.messages = True #Enables bot to listen to message events
    intents.message_content = True #Enables bot to access the content of messages
    intents.reactions = True
    client = discord.Client(intents=intents) #interacts with discord API, represents bot client. Central object that allows bot to handle events, send messages...

    @client.event #Register event handlers that will respond to specific events
    #Triggered when bot successfully connects to discord, indicates if bot is running
    async def on_ready(): #discord.py knows to run this because of the function name on_ready()
        print(f"{client.user} is now running!")

    @client.event #Register event handlers that will respond to specific events
    #This event is triggered whenever a message is sent in a server where the bot is present
    async def on_message(message): #discord.py knows to run this because of the function name on_message()
        if message.author == client.user: #checks if message is from bot, it prevents it from responding to its own messages
            return
        
        if client.user in message.mentions: #checks if bot was mentioned in the message
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            user_message = user_message.replace(f'<@{client.user.id}>', '').strip() #removes mention of the bot from message so its only users' input remains
            
            #Message processing
            if user_message[0] == '?':  #putting a question mark indicates that the bot sends you a private message
                user_message = user_message[1:]
                await send_stats(message, user_message, is_private=True, client=client) #private
            else:
                await send_stats(message, user_message, is_private=False, client=client) #public

    @client.event #Register event handlers that will respond to specific events
    #this event is triggered whenever a user adds a reaction to a message the bot can see
    async def on_reaction_add(reaction, user): #discord.py knows to run this because of the function name on_reaction_add()
        #reaction processing
        await handle_reaction(reaction, user, client)

    client.run(TOKEN) #starts the bot by connecting it to discord using the provided token.
    #must keep token somewhere safe, like a file.

