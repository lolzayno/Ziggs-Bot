from discord import Embed
import textwrap
import database
import fetch_data
import fetch_database
API_KEY = database.get_json("API_KEY")
def handle_response(message, output):
    player_id = output
    message = message.split()
    command = message[0]
    if command == "!update":
        region = message[1]
        ign = message[2]
        if isinstance(player_id, str):
            return player_id
        else:
            fetched_id, true_region = fetch_data.fetch_id(region, ign, API_KEY)
            fetch_data.fetch_matches(region, fetched_id, true_region, API_KEY)
            champions = fetch_database.fetch_unique_champions(player_id)
            for champion in champions:
                result = database.fetch_games(player_id, champion)
                if result != 0:
                    champ_average = fetch_database.fetch_champ_averages(player_id, champion)
            react_options = textwrap.dedent("""
                - React to 🏠 to return to this main page
                - React to 🎮 to view your match history and see match specifics
                - React to 🌟 to view your champions' averages
                                            
                Accessible after selecting 🌟:
                - React to 🔮 to see your stats on each rune
                - React to 🃏 to see your stats on each item
                - React to ⚔️ to see your stats on each matchup
                """)
            embed = Embed(
            title=f"List of Reacts:",
            description=react_options,
            color=0xC8A2C8
            )
            react_options = textwrap.dedent("""
            - Wait for all the reacts to be present before making a selection
            """)
            embed.set_footer(text=react_options)
            return embed
    elif command == "!user":
        region = message[1]
        ign = message[2]
        if isinstance(player_id, str):
            return player_id
        else:
            react_options = textwrap.dedent("""
                - React to 🏠 to return to this main page
                - React to 🎮 to view your match history and see match specifics
                - React to 🌟 to view your champions' averages
                                            
                Accessible after selecting 🌟:
                - React to 🔮 to see your stats on each rune
                - React to 🃏 to see your stats on each item
                - React to ⚔️ to see your stats on each matchup
                """)
            embed = Embed(
            title=f"List of Reacts:",
            description=react_options,
            color=0xC8A2C8
            )
            react_options = textwrap.dedent("""
            - Wait for all the reacts to be present before making a selection
            """)
            embed.set_footer(text=react_options)
            return embed
    return 'Command not recognized'

def home_page():
    react_options = textwrap.dedent("""
    - React to 🏠 to return to this main page
    - React to 🎮 to view your match history and see match specifics
    - React to 🌟 to view your champions' averages
                                
    Accessible after selecting 🌟:
    - React to 🔮 to see your stats on each rune
    - React to 🃏 to see your stats on each item
    - React to ⚔️ to see your stats on each matchup
""")
    embed = Embed(
        title=f"List of Reacts:",
        description=react_options,
        color=0xC8A2C8
        )
    react_options = textwrap.dedent("""
    - Wait for all the reacts to be present before making a selection
    """)
    embed.set_footer(text=react_options)
    return embed

def help_output():
    command_options = textwrap.dedent("""
    - First time using me? Use command below me (ex. @Ziggs Kobe Bot !update NA Zayno#NA1)
    - !update region ign#tag (ex. NA Zayno#NA1) for your account stats (updates your information so its up to date)
    - !user region ign#tag (ex. NA Zayno#NA1) for your account stats (current information on file)
    - !matchups - Displays all the available champions that have laning tips for ziggs
    - !matchup champion (ex. !matchup zed) - which displays tips on how to lane against a specific champ when playing ziggs (MUST BE LOWER CASE)
    """)
    embed = Embed(
        title=f"List of commands I understand:",
        description=command_options,
        color=0xC8A2C8
    )
    return embed

def champ_averages(champ_average, ingame_name):
    champion = champ_average[2]
    total_games = champ_average[3]
    champ_wr = champ_average[6]
    avg_kills = champ_average[32]
    avg_deaths = champ_average[33]
    avg_assits = champ_average[34]
    avg_kda = champ_average[35]
    avg_kp = champ_average[36]
    avg_champlvl = champ_average[37]
    avg_goldPerMin = champ_average[38]
    avg_control_wards = champ_average[39]
    avg_stealth_wards = champ_average[40]
    avg_magic = champ_average[41]
    avg_physical = champ_average[42]
    avg_total = champ_average[43]
    avg_minions = champ_average[44]
    avg_minionsPerMin = champ_average[45]
    avg_objdmg = champ_average[46]
    avg_turretdmg = champ_average[47]
    avg_dmgPerMin = champ_average[48]
    avg_team_dmgPercent = champ_average[49]
    avg_team_receivePercent = champ_average[50]
    avg_dodge_close = champ_average[51]
    avg_solo = champ_average[52]
    avg_q = champ_average[53]
    avg_w = champ_average[54]
    avg_e = champ_average[55]
    avg_r = champ_average[56]
    avg_turretPlates = champ_average[57]
    avg_turretTakedowns = champ_average[58]
    avg_enemyCC = champ_average[59]
    avg_knockIntoTeam = champ_average[60]
    avg_minions10Min = champ_average[61]
    avg_skillshotsearly = champ_average[62]
    avg_dodge = champ_average[63]
    avg_skillshots = champ_average[64]
    avg_champexp = champ_average[65]
    avg_champexpPerMin = champ_average[66]
    avg_gold = champ_average[67]
    avg_timeCC = champ_average[68]
    stats_output_general = textwrap.dedent(f"""
    General:
    - You have played a total of {total_games} games on {champion}
    - Your overall winrate is {int(champ_wr * 100)}%
    - Average KDA is {avg_kda} ({avg_kills}/{avg_deaths}/{avg_assits} - Kills(🔪)/Deaths(☠️)/Assists(🤝))
    - You have {avg_solo} solo kills every game 🔥
    - Average Kill Participation is {int(avg_kp * 100)}% meaning you assisted or killed on {int(avg_kp * 100)}% of your team's kills
    - You average about {int(avg_goldPerMin)} gold per minute and average {int(avg_gold)} gold for the entire match 💰
    - On average, you get about {int(avg_champexpPerMin)} experience per minute and {avg_champexp} experience for the entire game, ending with an average level of {avg_champlvl} each game 🧠
    - You cast Q {int(avg_q)} times, W {int(avg_w)} times, E {int(avg_e)} times, and R {avg_r} times a game 🌀
    - Every game, you average {avg_minions} minions per game, {avg_minionsPerMin} creeps per minute, and at minute 10, you usually have {avg_minions10Min} farm, meaning you kill {round(avg_minions - avg_minions10Min,1)} minions after 10 minutes 👾
    - You place {avg_stealth_wards} stealth wards every game, and purchase {avg_control_wards} every game 👁️

    Damage💥:
    - You deal about {int(avg_physical)} physical damage 🗡️, {int(avg_magic)} magic damage 💣, and {int(avg_total)} total damage 💥 every game
    - Per game, you deal {int(avg_dmgPerMin)} damage per minute 💥
    - You make up about {int(avg_team_dmgPercent * 100)}% of all your team's damage 💥
    - Out of all the damage your team has taken, you receive {int(avg_team_receivePercent * 100)}% of the all damage 💥

    Objectives:
    - You deal about {int(avg_objdmg)} damage to Barons, Dragons, Rift Heralds, and Grubs every game 🐉
    - Typically, you do {int(avg_turretdmg)} damage to turrets, destroy {avg_turretPlates} turret plates, and kill {avg_turretTakedowns} turrets throughout each game 🏰

    Skillshots:
    - You have {avg_dodge_close} close encounters with skillshots (really close dodge) 💨
    - You dodge a total of {avg_dodge} skillshots the entire game 🏃
    - On average, you land {avg_skillshots} skillshots every game 🎯
    - During the early game, you typically land {avg_skillshotsearly} skill shots 🎯

    Crowd Control (CC):
    - The average time your opponent is CC'd by your abilities is {int(avg_timeCC / 60)} minute(s) and {int(avg_timeCC % 60)} seconds ⏳
    - You knock your opponent into your teams' reach {avg_knockIntoTeam} times a game ⚡
    - You CC'd your opponents {avg_enemyCC} times each game 😵
    """)
    embed_general = Embed(
        title=f"{champion} Stats for {ingame_name}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general, champion


def item_output(item_snippet, ingame_name):
    champion = item_snippet[2]
    item_name = item_snippet[3]
    games = item_snippet[4]
    wins = item_snippet[5]
    losses = item_snippet[6]
    wr = item_snippet[7]
    pr = item_snippet[8]
    stats_output_general = textwrap.dedent(f"""
    - Number of games you purchased {item_name}: {games}
    - Games won: {wins} 🏆
    - Games lost: {losses} 🚫
    - Total winrate using {item_name}: {int(wr*100)}%
    - You buy this item in {int(pr * 100)}% of your games
    """)
    embed_general = Embed(
        title=f"{champion} Stats for {ingame_name}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general

def matchup_output(matchup_snippet, ingame_name):
    champion = matchup_snippet[2]
    opponent = matchup_snippet[3]
    lane = matchup_snippet[4]
    games = matchup_snippet[5]
    wins = matchup_snippet[6]
    losses = matchup_snippet[7] 
    wr = matchup_snippet[8]
    pr = matchup_snippet[9]
    stats_output_general = textwrap.dedent(f"""
    - Number of games you're vs'd {opponent}: {games}
    - Games won: {wins} 🏆
    - Games lost: {losses} 🚫
    - Overall winrate against {opponent}: {int(wr *100)}%
    - You play this matchup {int(pr*100)}% of your games played in {lane}
    """)
    embed_general = Embed(
        title=f"{champion} Stats for {ingame_name} against {opponent}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general

def rune_output(rune_snippet, ingame_name):
    champion = rune_snippet[2]
    rune = rune_snippet[3]
    games = rune_snippet[4]
    wins = rune_snippet[5]
    losses = rune_snippet[6] 
    wr = rune_snippet[7]
    pr = rune_snippet[8]
    var1 = rune_snippet[9]
    var2 = rune_snippet[10]
    var3 = rune_snippet[11]
    stats_output_general = textwrap.dedent(f"""
    - Number of games you ran {rune}: {games}
    - Games won: {wins} 🏆
    - Games lost: {losses} 🚫
    - Overall winrate using {rune}: {int(wr *100)}%
    - You use this rune {int(pr*100)}% of your games played using {champion}
    """)
    if rune == "Arcane Comet":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Arcane Comet
        - Average Damage: {var1} 💥                    
        """)
    if rune == "Electrocute":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Electrocute
        - Average Damage: {var1} 💥                           
        """)
    if rune == "Fleet Footwork":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Fleet Footwork
        - Average Total Healing: {var1} 💖                       
        """)
    if rune == "Conqueror":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Conqueror
        - Average Total Healing: {var1} 💖                    
        """)
    if rune == "Press the Attack":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Press the Attack
        - Average Total Damage: {var1} 💥
        - Average Bonus Damage: {var2} 🎁
        - Average Expose Damage: {var3} 🕵️‍♂️
        """)
    if rune == "Dark Harvest":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Dark Harvest
        - Average Total Damage: {var1} 💥
        - Average Total Souls Harvested: {var2} 👻
        """)
    if rune == "Hail of Blades":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Hail of Blades
        - Average Attacks made with extra attack speed: {var1} ⚔️
        - Average Percentage of Hail attacks landed: {int(var2*100)}
        """)
    if rune == "Summon Aery":
        stats_output_general +=textwrap.dedent(f"""
        Keystone: Summon Aery
        - Average Total Damage: {var1} 💥
        - Average Total Shield: {var2} 🛡️
        """)
    if rune == "Glacial Augment":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Glacial Augment
        - Average Duration enemy champions slowed: {var1}s 🐌
        - Average Damage reduced: {var2} 📉
        """)
    if rune == "Aftershock":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Aftershock
        - Average Total Damage: {var1} 💥
        - Average Total Damage Mitigated: {var2} 📉
        """)
    if rune == "Phase Rush":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Phase Rush
        - Average Total Activations: {var1} 🏃
        """)
    if rune == "Grasp of the Undying":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Grasp of the Undying
        - Average Total Damage: {var1} 💥
        - Average Total Healing: {var2} 💖
        """)
    if rune == "Guardian":
        stats_output_general += textwrap.dedent(f"""
        Keystone: Guardian
        - Average Total Shielding Strength: {var1} 🛡️
        """)
    if rune == "First Strike":
        stats_output_general += textwrap.dedent(f"""
        Keystone: First Strike
        - Average Total Damage: {var1} 💥
        - Average Total Gold Earned: {var2} 💰
        """)
    if rune == "Unsealed Spellbook":
        stats_output_general += textwrap.dedent(f"""
        Unsealed Spellbook
        - Average Total Times rune was changed: {var1}
        """)
    if rune == "Absorb Life":
        stats_output_general += textwrap.dedent(f"""
        Rune: Absorb Life
        - Average Total Healing: {var1} 💖
        """)
    if rune == "Legend: Haste":
        stats_output_general += textwrap.dedent(f"""
        Rune: Legend: Haste
        - Average Time Completed: {var1} ⏰
        """)
    if rune == "Last Stand":    
        stats_output_general += textwrap.dedent(f"""
        Rune: Last Stand
        - Average Total Bonus Damage: {var1} 💥
        """)
    if rune == "Manaflow Band":
        stats_output_general += textwrap.dedent(f"""
        Rune: Manaflow Band
        - Average Total bonus Mana: {var1} 💧
        - Average Total mana restored: {var2} 🌧️
        """)
    if rune == "Transcendence":
        stats_output_general += textwrap.dedent(f"""
        Rune: Transcendence
        - Average Seconds refunded: {var1} ⏰
        """)
    if rune == "Sudden Impact":
        stats_output_general += textwrap.dedent(f"""
        Rune: Sudden Impact
        - Average Bonus Damage: {var1} 💥
        """)
    if rune == "Eyeball Collection":
        stats_output_general += textwrap.dedent(f"""
        Rune: Eyeball Collection
        - Average Total Bonus AD/AP: {var1} 💥
        """)
    if rune == "Ultimate Hunter":
        stats_output_general += textwrap.dedent(f"""
        Rune: Ultimate Hunter
        - Average Total Stacks: {var1}
        """)
    if rune == "Triumph":
        stats_output_general += textwrap.dedent(f"""
        Rune: Triumph
        - Average Total Health Restored: {var1} 💖
        - Average Total bonus gold granted: {var2} 💰
        """)
    if rune == "Coup de Grace":
        stats_output_general += textwrap.dedent(f"""
        Rune: Coup de Grace
        - Average Total Bonus Damage: {var1} 💥
        """)
    if rune == "Scorch":
        stats_output_general += textwrap.dedent(f"""
        Rune: Scorch
        - Average Total Bonus Damage: {var1} 💥
        """)
    if rune == "Presence of Mind":
        stats_output_general += textwrap.dedent(f"""
        Rune: Presence of Mind
        - Average Resource Restored: {var1} 💧
        """)
    if rune == "Cut Down":
        stats_output_general += textwrap.dedent(f"""
        Rune: Cut Down
        - Average Total Bonus Damage: {var1} 💥
        """)
    if rune == "Magical Footwear":
        stats_output_general += textwrap.dedent(f"""
        Rune: Magical Footwear
        - Average Boots Arrival Time: {var1} ⏰
        """)
    if rune == "Biscuit Delivery":
        stats_output_general += textwrap.dedent(f"""
        Rune: Biscuit Delivery
        - Average Biscuits Received: {var1} 🍪
        """)
    if rune == "Cosmic Insight":
        stats_output_general += textwrap.dedent(f"""
        Rune: Cosmic Insight 👁️
        """)
    if rune == "Legend: Alacrity":
        stats_output_general += textwrap.dedent(f"""
        Rune: Legend: Alacrity
        - Average Time Completed: {var1} ⏰
        """)
    if rune == "Overgrowth":
        stats_output_general += textwrap.dedent(f"""
        Rune: Overgrowth
        - Average Total Bonus Max Health: {var1} 💚
        """)
    if rune == "Conditioning":
        stats_output_general += textwrap.dedent(f"""
        Rune: Conditioning
        - Average Percent of game active: {var1}
        - Average Total Bonus Armor: {var2} 🛡️
        - Average Total Bonus Magic Resist: {var3} 🏰
        """)
    if rune == "Legend: Bloodline":
        stats_output_general += textwrap.dedent(f"""
        Rune: Legend: Bloodline
        - Average Time Completed: {var1} ⏰
        """)
    if rune == "Celerity":
        stats_output_general += textwrap.dedent(f"""
        Rune: Celerity
        - Average Extra Distance Travelled: {var1} 📍
        """)
    if rune == "Gathering Storm":
        stats_output_general += textwrap.dedent(f"""
        Rune: Gathering Storm
        - Average Total Bonus AD/AP: {var1} 💥
        """)
    if rune == "Demolish":
        stats_output_general += textwrap.dedent(f"""
        Rune: Demolish
        - Average Total Bonus Damage: {var1} 💥
        """)
    if rune == "Approach Velocity":
        stats_output_general += textwrap.dedent(f"""
        Rune: Approach Velocity
        - Average Time Spent Hasted: {var1} ⏰
        """)
    if rune == "Shield Bash":
        stats_output_general += textwrap.dedent(f"""
        Rune: Shield Bash
        - Average Total Damage: {var1} 💥
        """)
    if rune == "Second Wind":
        stats_output_general += textwrap.dedent(f"""
        Rune: Second Wind
        - Average Total Healing: {var1} 💖
        """)
    if rune == "Cheap Shot":
        stats_output_general += textwrap.dedent(f"""
        Rune: Cheap Shot
        - Average Total Damage: {var1} 💥
        """)
    if rune == "Taste of Blood":
        stats_output_general += textwrap.dedent(f"""
        Rune: Taste of Blood
        - Average Total Healing: {var1} 💖
        """)
    if rune == "Treasure Hunter":
        stats_output_general += textwrap.dedent(f"""
        Rune: Treasure Hunter
        - Average Gold Collected: {var1} 💰
        - Average Total Stacks: {var2}
        """)
    if rune == "Zombie Ward":
        stats_output_general += textwrap.dedent(f"""
        Rune: Zombie Ward
        - Average Wards spawned: {var1} 👁️
        - Average Adaptive Force Gained: {var2} 💥
        """)
    if rune == "Hextech Flashtraption":
        stats_output_general += textwrap.dedent(f"""
        Rune: Hextech Flashtraption
        - Average Times Hexflashed: {var1}
        """)
    if rune == "Relentless Hunter":
        stats_output_general += textwrap.dedent(f"""
        Rune: Relentless Hunter
        - Average Total Stacks: {var1}
        - Average {var2}% Move Speed Increase 👢
        """)
    if rune == "Water Walking":
        stats_output_general += textwrap.dedent(f"""
        Rune: Water Walking
        - Average Total time active: {var1} ⏰
        """)
    if rune == "Nullifying Orb":
        stats_output_general += textwrap.dedent(f"""
        Rune: Nullifying Orb
        - Average Total Shield Granted: {var1} 🛡️
        """)
    if rune == "Absolute Focus":
        stats_output_general += textwrap.dedent(f"""
        Rune: Absolute Focus
        - Average Total time active: {var1} ⏰
        """)
    if rune == "Ghost Poro":
        stats_output_general += textwrap.dedent(f"""
        Rune: Ghost Poro
        - Average Ghost Poros Spawned: {var1}
        - Average Enemies Spotted: {var2} 👁️
        """)
    if rune == "Nimbus Cloak":
        stats_output_general += textwrap.dedent(f"""
        Rune: Nimbus Cloak
        - Average Times activated: {var1} 
        """)
    if rune == "Font of Life":
        stats_output_general += textwrap.dedent(f"""
        Rune: Font of Life
        - Average Total Ally Healing: {var1} 💖
        """)
    if rune == "Bone Plating":
        stats_output_general += textwrap.dedent(f"""
        Rune: Bone Plating
        - Average Total Damage Blocked: {var1} 🛡️
        """)
    if rune == "Revitalize":
        stats_output_general += textwrap.dedent(f"""
        Rune: Revitalize
        - Average Bonus Healing: {var1} 💖
        - Average Bonus Shielding: {var2} 🛡️
        """)
    if rune == "Cash Back":
        stats_output_general += textwrap.dedent(f"""
        Rune: Cash Back
        - Average Gold Gained: {var1} 💰
        """)
    if rune == "Triple Tonic":
        stats_output_general += textwrap.dedent(f"""
        Rune: Triple Tonic
        - Average Items Gained: {var1}
        """)
    if rune == "Unflinching":
        stats_output_general += textwrap.dedent(f"""
        Rune: Unflinching
        - Average Seconds in combat with bonus resistances: {var1} ⏰
        """)
    if rune == "Time Warp Tonic":    
        stats_output_general += textwrap.dedent(f"""
        Rune: Time Warp Tonic
        - Average Total Immediate Health Restored: {var1} 💖
        """)
    if rune == "Jack of All Trades":
        stats_output_general += textwrap.dedent(f"""
        Rune: Jack of All Trades
        - Average Bonus stats gained: {var1}
        """)    
    embed_general = Embed(
        title=f"{champion} Stats for {ingame_name} using {rune}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general

def item_output(item_snippet, ingame_name):
    champion = item_snippet[2]
    item = item_snippet[3]
    games = item_snippet[4]
    wins = item_snippet[5]
    losses = item_snippet[6] 
    wr = item_snippet[7]
    pr = item_snippet[8]
    stats_output_general = textwrap.dedent(f"""
    - Number of games you ran {item}: {games}
    - Games won: {wins} 🏆
    - Games lost: {losses} 🚫
    - Overall winrate using {item}: {int(wr *100)}%
    - You use this item {int(pr*100)}% of your games played using {champion}
    """)
    embed_general = Embed(
        title=f"{champion} Stats for {ingame_name} using {item}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general

def matchups_output(item_snippet, ingame_name):
    champion = item_snippet[2]
    opponent = item_snippet[3]
    lane = item_snippet[4]
    count = item_snippet[5]
    win = item_snippet[6] 
    loss = item_snippet[7]
    wr = item_snippet[8]
    pr = item_snippet[9]
    stats_output_general = textwrap.dedent(f"""
    - Lane Matchup: {lane}
    - Number of games you vs'd against {opponent}: {count}
    - Games won: {win} 🏆
    - Games lost: {loss} 🚫
    - Overall winrate against {opponent}: {int(wr *100)}%
    - You laned against {opponent} {int(pr*100)}% of your games played using {champion}
    """)
    embed_general = Embed(
        title=f"{champion} Stats for {ingame_name} laning against {opponent}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general

def match_output(match_snippet, ingame_name):
    match_code = match_snippet[2]
    champion = match_snippet[3]
    gameDuration = match_snippet[4]
    result = match_snippet[5]
    lane = match_snippet[6]
    kills = match_snippet[7]
    deaths = match_snippet[8]
    assists = match_snippet[9]
    kda = match_snippet[10]
    kp = match_snippet[11]
    champ_lvl = match_snippet[12]
    item0 = match_snippet[13]
    item1 = match_snippet[14]
    item2 = match_snippet[15]
    item3 = match_snippet[16]
    item4 = match_snippet[17]
    item5 = match_snippet[18]
    item6 = match_snippet[19]
    goldPerMinute = match_snippet[20]
    control_wards = match_snippet[21]
    stealth_wards = match_snippet[22]
    magic_dmg = match_snippet[23]
    physical_dmg = match_snippet[24]
    total_dmg = match_snippet[25]
    total_minions = match_snippet[26]
    minionsPerMinute = match_snippet[27]
    dmg_obj = match_snippet[28]
    dmg_turrets = match_snippet[29]
    damagePerMinute = match_snippet[30]
    dmg_dealtPercent = match_snippet[31]
    dmg_receivePercent = match_snippet[32]
    dodge_smallWindow = match_snippet[33]
    solokill = match_snippet[34]
    q_cast = match_snippet[35]
    w_cast = match_snippet[36]
    e_cast = match_snippet[37]
    r_cast = match_snippet[38]
    turret_plates = match_snippet[39]
    turret_takedowns = match_snippet[40]
    enemyCC = match_snippet[41]
    knock_intoTeam = match_snippet[42]
    minions_first10 = match_snippet[43]
    skillshots_early = match_snippet[44]
    skillshots_dodged = match_snippet[45]
    skillshots_hit = match_snippet[46]
    champExp = match_snippet[47]
    champExp_perMin = match_snippet[48]
    gold = match_snippet[49]
    totalTimeCC = match_snippet[50]
    key_stone = match_snippet[51]
    key_stone_var1 = match_snippet[52]
    key_stone_var2 = match_snippet[53]
    key_stone_var3 = match_snippet[54]
    rune_2 = match_snippet[55]
    rune_2_var1 = match_snippet[56]
    rune_2_var2 = match_snippet[57]
    rune_2_var3 = match_snippet[58]
    rune_3 = match_snippet[59]
    rune_3_var1 = match_snippet[60]
    rune_3_var2 = match_snippet[61]
    rune_3_var3 = match_snippet[62]
    rune_4 = match_snippet[63]
    rune_4_var1 = match_snippet[64]
    rune_4_var2 = match_snippet[65]
    rune_4_var3 = match_snippet[66]
    rune_5 = match_snippet[67]
    rune_5_var1 = match_snippet[68]
    rune_5_var2 = match_snippet[69]
    rune_5_var3 = match_snippet[70]
    rune_6 = match_snippet[71]
    rune_6_var1 = match_snippet[72]
    rune_6_var2 = match_snippet[73]
    rune_6_var3 = match_snippet[74]
    opponent = match_snippet[75]

    stats_output_general = textwrap.dedent(f"""
    - Champion Played: {champion}
    - Lane Played: {lane}
    - Laned Against: {opponent}
    - Game Duration: {int(gameDuration / 60)} minutes and {gameDuration % 60} seconds
    - Result: {result}
    - {kills}/{deaths}/{assists} (KDA - Kills(🔪)/Deaths(☠️)/Assists(🤝) - {kda})]
    - Total Solo Kills: {solokill} 🔥
    - Kills participated in {int(kp * 100)}% 🤝
    - Champion Level: {champ_lvl} 🧠
    - Total Champion Experience: {champExp} ({champExp_perMin} experience per minute) 🧠
    - Build: {item0}, {item1}, {item2}, {item3}, {item4}, {item5}, and {item6}
    - Total Gold: {gold} ({goldPerMinute} gold per minute) 💰
    - Control wards placed: {control_wards} 👁️
    - stealth wards placed: {stealth_wards} 👁️
    - Magic damage dealt: {magic_dmg} 💣
    - Physical damage dealt: {physical_dmg} 🗡️
    - total damage dealt: {total_dmg} ({damagePerMinute} damage per minute) 💥
    - Total minions slain: {total_minions} ({minionsPerMinute} minions per minute - {minions_first10} minions killed during first 10 minutes) 👾
    - Total damage dealt to turrets: {dmg_turrets} 🏰
    - Total damage dealt to objectives: {dmg_obj} 🐉
    - Percent of teams damage dealt by you: {int(dmg_dealtPercent*100)}% 💥
    - Percent of teams received damage inflicted on you: {int(dmg_receivePercent*100)}%
    - Total skillshots dodged that came close: {dodge_smallWindow} 💨
    - Total Q casts: {q_cast}
    - Total W casts: {w_cast}
    - Total E casts: {e_cast}
    - Total R casts: {r_cast}
    - Turret Plates taken: {turret_plates} 🏰
    - Turrets Killed: {turret_takedowns} 🏰
    - Total times an enemy was CC'd: {enemyCC} 😵
    - Times you knocked opponents into your team: {knock_intoTeam} ⚡
    - Total skill shots landed in early game: {skillshots_early} 🎯
    - Total skill shots dodged: {skillshots_dodged} 💨
    - Total skill shots landed: {skillshots_hit} 🎯
    - Total time enemy was CC'd: {int(totalTimeCC / 60)} minute(s) and {int(totalTimeCC % 60)} seconds ⏰
    """)
    runes_type = [
    (key_stone, key_stone_var1, key_stone_var2, key_stone_var3, 1),
    (rune_2, rune_2_var1, rune_2_var2, rune_2_var3, 2),
    (rune_3, rune_3_var1, rune_3_var2, rune_3_var3, 3),
    (rune_4, rune_4_var1, rune_4_var2, rune_4_var3, 4),
    (rune_5, rune_5_var1, rune_5_var2, rune_5_var3, 5),
    (rune_6, rune_6_var1, rune_6_var2, rune_6_var3, 6)
    ]
    for rune, var1, var2, var3, number in runes_type:
        if number == 1:
            stats_output_general += textwrap.dedent(f"""
            Primary Tree:
            """)
        if number == 5:
            stats_output_general += textwrap.dedent(f"""
            Secondary Tree:
            """)
        if rune == "Arcane Comet":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Arcane Comet
            - Average Damage: {var1} 💥                    
            """)
        if rune == "Electrocute":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Electrocute
            - Average Damage: {var1} 💥                           
            """)
        if rune == "Fleet Footwork":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Fleet Footwork
            - Average Total Healing: {var1} 💖                       
            """)
        if rune == "Conqueror":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Conqueror
            - Average Total Healing: {var1} 💖                    
            """)
        if rune == "Press the Attack":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Press the Attack
            - Average Total Damage: {var1} 💥
            - Average Bonus Damage: {var2} 🎁
            - Average Expose Damage: {var3} 🕵️‍♂️
            """)
        if rune == "Dark Harvest":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Dark Harvest
            - Average Total Damage: {var1} 💥
            - Average Total Souls Harvested: {var2} 👻
            """)
        if rune == "Hail of Blades":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Hail of Blades
            - Average Attacks made with extra attack speed: {var1} ⚔️
            - Average Percentage of Hail attacks landed: {int(var2*100)}
            """)
        if rune == "Summon Aery":
            stats_output_general +=textwrap.dedent(f"""
            Keystone: Summon Aery
            - Average Total Damage: {var1} 💥
            - Average Total Shield: {var2} 🛡️
            """)
        if rune == "Glacial Augment":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Glacial Augment
            - Average Duration enemy champions slowed: {var1}s 🐌
            - Average Damage reduced: {var2} 📉
            """)
        if rune == "Aftershock":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Aftershock
            - Average Total Damage: {var1} 💥
            - Average Total Damage Mitigated: {var2} 📉
            """)
        if rune == "Phase Rush":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Phase Rush
            - Average Total Activations: {var1} 🏃
            """)
        if rune == "Grasp of the Undying":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Grasp of the Undying
            - Average Total Damage: {var1} 💥
            - Average Total Healing: {var2} 💖
            """)
        if rune == "Guardian":
            stats_output_general += textwrap.dedent(f"""
            Keystone: Guardian
            - Average Total Shielding Strength: {var1} 🛡️
            """)
        if rune == "First Strike":
            stats_output_general += textwrap.dedent(f"""
            Keystone: First Strike
            - Average Total Damage: {var1} 💥
            - Average Total Gold Earned: {var2} 💰
            """)
        if rune == "Unsealed Spellbook":
            stats_output_general += textwrap.dedent(f"""
            Unsealed Spellbook
            - Average Total Times rune was changed: {var1}
            """)
        if rune == "Absorb Life":
            stats_output_general += textwrap.dedent(f"""
            Rune: Absorb Life
            - Average Total Healing: {var1} 💖
            """)
        if rune == "Legend: Haste":
            stats_output_general += textwrap.dedent(f"""
            Rune: Legend: Haste
            - Average Time Completed: {var1} ⏰
            """)
        if rune == "Last Stand":    
            stats_output_general += textwrap.dedent(f"""
            Rune: Last Stand
            - Average Total Bonus Damage: {var1} 💥
            """)
        if rune == "Manaflow Band":
            stats_output_general += textwrap.dedent(f"""
            Rune: Manaflow Band
            - Average Total bonus Mana: {var1} 💧
            - Average Total mana restored: {var2} 🌧️
            """)
        if rune == "Transcendence":
            stats_output_general += textwrap.dedent(f"""
            Rune: Transcendence
            - Average Seconds refunded: {var1} ⏰
            """)
        if rune == "Sudden Impact":
            stats_output_general += textwrap.dedent(f"""
            Rune: Sudden Impact
            - Average Bonus Damage: {var1} 💥
            """)
        if rune == "Eyeball Collection":
            stats_output_general += textwrap.dedent(f"""
            Rune: Eyeball Collection
            - Average Total Bonus AD/AP: {var1} 💥
            """)
        if rune == "Ultimate Hunter":
            stats_output_general += textwrap.dedent(f"""
            Rune: Ultimate Hunter
            - Average Total Stacks: {var1}
            """)
        if rune == "Triumph":
            stats_output_general += textwrap.dedent(f"""
            Rune: Triumph
            - Average Total Health Restored: {var1} 💖
            - Average Total bonus gold granted: {var2} 💰
            """)
        if rune == "Coup de Grace":
            stats_output_general += textwrap.dedent(f"""
            Rune: Coup de Grace
            - Average Total Bonus Damage: {var1} 💥
            """)
        if rune == "Scorch":
            stats_output_general += textwrap.dedent(f"""
            Rune: Scorch
            - Average Total Bonus Damage: {var1} 💥
            """)
        if rune == "Presence of Mind":
            stats_output_general += textwrap.dedent(f"""
            Rune: Presence of Mind
            - Average Resource Restored: {var1} 💧
            """)
        if rune == "Cut Down":
            stats_output_general += textwrap.dedent(f"""
            Rune: Cut Down
            - Average Total Bonus Damage: {var1} 💥
            """)
        if rune == "Magical Footwear":
            stats_output_general += textwrap.dedent(f"""
            Rune: Magical Footwear
            - Average Boots Arrival Time: {var1} ⏰
            """)
        if rune == "Biscuit Delivery":
            stats_output_general += textwrap.dedent(f"""
            Rune: Biscuit Delivery
            - Average Biscuits Received: {var1} 🍪
            """)
        if rune == "Cosmic Insight":
            stats_output_general += textwrap.dedent(f"""
            Rune: Cosmic Insight 👁️
            """)
        if rune == "Legend: Alacrity":
            stats_output_general += textwrap.dedent(f"""
            Rune: Legend: Alacrity
            - Average Time Completed: {var1} ⏰
            """)
        if rune == "Overgrowth":
            stats_output_general += textwrap.dedent(f"""
            Rune: Overgrowth
            - Average Total Bonus Max Health: {var1} 💚
            """)
        if rune == "Conditioning":
            stats_output_general += textwrap.dedent(f"""
            Rune: Conditioning
            - Average Percent of game active: {var1}
            - Average Total Bonus Armor: {var2} 🛡️
            - Average Total Bonus Magic Resist: {var3} 🏰
            """)
        if rune == "Legend: Bloodline":
            stats_output_general += textwrap.dedent(f"""
            Rune: Legend: Bloodline
            - Average Time Completed: {var1} ⏰
            """)
        if rune == "Celerity":
            stats_output_general += textwrap.dedent(f"""
            Rune: Celerity
            - Average Extra Distance Travelled: {var1} 📍
            """)
        if rune == "Gathering Storm":
            stats_output_general += textwrap.dedent(f"""
            Rune: Gathering Storm
            - Average Total Bonus AD/AP: {var1} 💥
            """)
        if rune == "Demolish":
            stats_output_general += textwrap.dedent(f"""
            Rune: Demolish
            - Average Total Bonus Damage: {var1} 💥
            """)
        if rune == "Approach Velocity":
            stats_output_general += textwrap.dedent(f"""
            Rune: Approach Velocity
            - Average Time Spent Hasted: {var1} ⏰
            """)
        if rune == "Shield Bash":
            stats_output_general += textwrap.dedent(f"""
            Rune: Shield Bash
            - Average Total Damage: {var1} 💥
            """)
        if rune == "Second Wind":
            stats_output_general += textwrap.dedent(f"""
            Rune: Second Wind
            - Average Total Healing: {var1} 💖
            """)
        if rune == "Cheap Shot":
            stats_output_general += textwrap.dedent(f"""
            Rune: Cheap Shot
            - Average Total Damage: {var1} 💥
            """)
        if rune == "Taste of Blood":
            stats_output_general += textwrap.dedent(f"""
            Rune: Taste of Blood
            - Average Total Healing: {var1} 💖
            """)
        if rune == "Treasure Hunter":
            stats_output_general += textwrap.dedent(f"""
            Rune: Treasure Hunter
            - Average Gold Collected: {var1} 💰
            - Average Total Stacks: {var2}
            """)
        if rune == "Zombie Ward":
            stats_output_general += textwrap.dedent(f"""
            Rune: Zombie Ward
            - Average Wards spawned: {var1} 👁️
            - Average Adaptive Force Gained: {var2} 💥
            """)
        if rune == "Hextech Flashtraption":
            stats_output_general += textwrap.dedent(f"""
            Rune: Hextech Flashtraption
            - Average Times Hexflashed: {var1}
            """)
        if rune == "Relentless Hunter":
            stats_output_general += textwrap.dedent(f"""
            Rune: Relentless Hunter
            - Average Total Stacks: {var1}
            - Average {var2}% Move Speed Increase 👢
            """)
        if rune == "Water Walking":
            stats_output_general += textwrap.dedent(f"""
            Rune: Water Walking
            - Average Total time active: {var1} ⏰
            """)
        if rune == "Nullifying Orb":
            stats_output_general += textwrap.dedent(f"""
            Rune: Nullifying Orb
            - Average Total Shield Granted: {var1} 🛡️
            """)
        if rune == "Absolute Focus":
            stats_output_general += textwrap.dedent(f"""
            Rune: Absolute Focus
            - Average Total time active: {var1} ⏰
            """)
        if rune == "Ghost Poro":
            stats_output_general += textwrap.dedent(f"""
            Rune: Ghost Poro
            - Average Ghost Poros Spawned: {var1}
            - Average Enemies Spotted: {var2} 👁️
            """)
        if rune == "Nimbus Cloak":
            stats_output_general += textwrap.dedent(f"""
            Rune: Nimbus Cloak
            - Average Times activated: {var1} 
            """)
        if rune == "Font of Life":
            stats_output_general += textwrap.dedent(f"""
            Rune: Font of Life
            - Average Total Ally Healing: {var1} 💖
            """)
        if rune == "Bone Plating":
            stats_output_general += textwrap.dedent(f"""
            Rune: Bone Plating
            - Average Total Damage Blocked: {var1} 🛡️
            """)
        if rune == "Revitalize":
            stats_output_general += textwrap.dedent(f"""
            Rune: Revitalize
            - Average Bonus Healing: {var1} 💖
            - Average Bonus Shielding: {var2} 🛡️
            """)
        if rune == "Cash Back":
            stats_output_general += textwrap.dedent(f"""
            Rune: Cash Back
            - Average Gold Gained: {var1} 💰
            """)
        if rune == "Triple Tonic":
            stats_output_general += textwrap.dedent(f"""
            Rune: Triple Tonic
            - Average Items Gained: {var1}
            """)
        if rune == "Unflinching":
            stats_output_general += textwrap.dedent(f"""
            Rune: Unflinching
            - Average Seconds in combat with bonus resistances: {var1} ⏰
            """)
        if rune == "Time Warp Tonic":    
            stats_output_general += textwrap.dedent(f"""
            Rune: Time Warp Tonic
            - Average Total Immediate Health Restored: {var1} 💖
            """)
        if rune == "Jack of All Trades":
            stats_output_general += textwrap.dedent(f"""
            Rune: Jack of All Trades
            - Average Bonus stats gained: {var1}
            """)    
    embed_general = Embed(
        title=f"Stats for viewed match {match_code} under {ingame_name}",
        description=stats_output_general,
        color=0xC8A2C8
    )
    return embed_general


def rune_options(list_runes):
    rune_output = textwrap.dedent(f"""
    Runes used (Sorted From Highest to Lowest Used) on {list_runes[0][2]}

    """)
    sorted_rune_data = sorted(list_runes, key=lambda x: x[4], reverse=True)
    for index, rune in enumerate(sorted_rune_data, start=1):
        rune_output += textwrap.dedent(f"""
        {index}. Rune: {rune[3]}, Games Played: {rune[4]}, Winrate: {int(rune[7] * 100)}%, Playrate: {int(rune[8] * 100)}%
        """)
    return rune_output