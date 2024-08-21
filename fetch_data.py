import requests
from datetime import datetime, timezone
import pytz
import concurrent.futures
import database
import time
import traceback
import threading

stop_event = threading.Event()
matches_existing_count = 0
matches_existing_count_lock = threading.Lock()  

def fetch_and_process(match, api_key, true_region, database, fetched_id):
    global matches_existing_count
    try:
        if stop_event.is_set():  
            return
        
        match_data = fetch_match_data(match, api_key, true_region)
        game_end = match_data['info']['gameEndTimestamp'] / 1000
        game_end_date = datetime.fromtimestamp(game_end)

        time.sleep(1.3) 
        
        if database.match_already_exists(match):
            print(f"Match {match} already exists in the database. Skipping...")
            

            with matches_existing_count_lock:
                matches_existing_count += 1
                if matches_existing_count >= 1:
                    stop_event.set()
                    print("Stopping further processing due to 3 existing matches.")
            return

        print(f"Processing match ID: {match}")  


        (
            assists, control_wards, damage_per_min, damage_taken, dodge_skill_close, enemy_cc, gold_per_min, kda, kp,
            knock_into_team, land_skills, minions_10, dodge_skill, skill_hit, solo_kill, ward_placed, team_dmg,
            turret_plates, turret_takedown, champ_exp, champ_lvl, champ_name, dmg_obj, dmg_turrets, deaths, total_gold,
            item0, item1, item2, item3, item4, item5, item6, kills, lane, magic_dmg, runes, physical_dmg, total_dmg,
            total_minion, time_cc, result, spell1, spell2, spell3, spell4
        ) = extract_match_data(match_data, fetched_id)
        for player in match_data["info"]["participants"]:
            if player['puuid'] != fetched_id and player['individualPosition'] == lane:
                opponent = player['championName']

        result = 'Win' if result else 'Lose'
        

        rune_variables = {}
        for i, style in enumerate(runes):
            for j, rune in enumerate(style['selections']):
                fetch_rune_value = fetch_rune(rune['perk'])
                var_name = f"PRune_{i+1}_{j}"
                rune_variables[f"{var_name}_fetch_rune"] = fetch_rune_value
                rune_variables[f"{var_name}_var1"] = rune['var1']
                rune_variables[f"{var_name}_var2"] = rune['var2']
                rune_variables[f"{var_name}_var3"] = rune['var3']
        

        database.insert_game(
            match,
            database.fetch_player_id_by_puuid(fetched_id),
            champ_name,
            match_data['info']['gameDuration'],
            result,
            lane,
            kills,
            deaths,
            assists,
            round(kda, 2),
            round(kp, 2),
            champ_lvl,
            fetch_item(item0),
            fetch_item(item1),
            fetch_item(item2),
            fetch_item(item3),
            fetch_item(item4),
            fetch_item(item5),
            fetch_item(item6),
            gold_per_min,
            control_wards,
            ward_placed,
            magic_dmg,
            physical_dmg,
            total_dmg,
            total_minion,
            round(total_minion / int(match_data['info']['gameDuration'] / 60), 1),
            dmg_obj,
            dmg_turrets,
            damage_per_min,
            team_dmg,
            damage_taken,
            dodge_skill_close,
            solo_kill,
            spell1,
            spell2,
            spell3,
            spell4,
            turret_plates,
            turret_takedown,
            enemy_cc,
            knock_into_team,
            minions_10,
            land_skills,
            dodge_skill,
            skill_hit,
            champ_exp,
            int(champ_exp / int(match_data['info']['gameDuration'] / 60)),
            total_gold,
            time_cc,
            rune_variables.get('PRune_1_0_fetch_rune'),
            rune_variables.get('PRune_1_0_var1'),
            rune_variables.get('PRune_1_0_var2'),
            rune_variables.get('PRune_1_0_var3'),
            rune_variables.get('PRune_1_1_fetch_rune'),
            rune_variables.get('PRune_1_1_var1'),
            rune_variables.get('PRune_1_1_var2'),
            rune_variables.get('PRune_1_1_var3'),
            rune_variables.get('PRune_1_2_fetch_rune'),
            rune_variables.get('PRune_1_2_var1'),
            rune_variables.get('PRune_1_2_var2'),
            rune_variables.get('PRune_1_2_var3'),
            rune_variables.get('PRune_1_3_fetch_rune'),
            rune_variables.get('PRune_1_3_var1'),
            rune_variables.get('PRune_1_3_var2'),
            rune_variables.get('PRune_1_3_var3'),
            rune_variables.get('PRune_2_0_fetch_rune'),
            rune_variables.get('PRune_2_0_var1'),
            rune_variables.get('PRune_2_0_var2'),
            rune_variables.get('PRune_2_0_var3'),
            rune_variables.get('PRune_2_1_fetch_rune'),
            rune_variables.get('PRune_2_1_var1'),
            rune_variables.get('PRune_2_1_var2'),
            rune_variables.get('PRune_2_1_var3'),
            opponent,
            game_end_date
        )
        print(f"Successfully Inserted {match}")
    except Exception as e:
        print(f"Error processing match ID {match}: {e}")
        traceback.print_exc()


def fetch_rune(rune_id):
    patch_version = "14.16.1"

    url = f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/data/en_US/runesReforged.json"
    

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch runes data. Status code: {response.status_code}")
        return None
    
    
    rune_data = response.json()
    rune_mappings = {}
    

    for tree in rune_data:
        for slot in tree['slots']:
            for rune in slot['runes']:
                rune_mappings[rune['id']] = rune['name']
    
    return rune_mappings[rune_id]

def fetch_match_data(match_id, api_key, true_region):
    #api url request link to riot
    specific_match_api_url = f'https://{true_region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'

    #actual request
    response = requests.get(specific_match_api_url)
    print(response)
    return response.json()

def extract_match_data(match_data, fetched_id):
    #Goes through each player of the game
    for player in match_data["info"]["participants"]:
        if player['puuid'] == fetched_id: #checks if the participant is user
            #Returns all the requested stats
            return player['assists'], player['challenges']['controlWardsPlaced'], int(player['challenges']['damagePerMinute']), round(player['challenges']['damageTakenOnTeamPercentage'],2), player['challenges']['dodgeSkillShotsSmallWindow'], player['challenges']['enemyChampionImmobilizations'], int(player['challenges']['goldPerMinute']), player['challenges']['kda'], round(player['challenges']['killParticipation'],2), player['challenges']['knockEnemyIntoTeamAndKill'], player['challenges']['landSkillShotsEarlyGame'], player['challenges']['laneMinionsFirst10Minutes'], player['challenges']['skillshotsDodged'], player['challenges']['skillshotsHit'], player['challenges']['soloKills'], player['challenges']['stealthWardsPlaced'], round(player['challenges']['teamDamagePercentage'],2), player['challenges']['turretPlatesTaken'], player['challenges']['turretTakedowns'], player['champExperience'], player['champLevel'], player['championName'], player['damageDealtToObjectives'], player['damageDealtToTurrets'], player['deaths'], player['goldEarned'], player['item0'], player['item1'], player['item2'], player['item3'], player['item4'], player['item5'], player['item6'], player['kills'], player['individualPosition'], player['magicDamageDealtToChampions'], player['perks']['styles'], player['physicalDamageDealtToChampions'], player['totalDamageDealtToChampions'], player['totalMinionsKilled'], player['totalTimeCCDealt'], player['win'], player["spell1Casts"], player["spell2Casts"], player["spell3Casts"], player["spell4Casts"]
    return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def fetch_item(itemid):
    if itemid == 0:
        return "None"

    patch_version = "14.16.1"


    url = f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/data/en_US/item.json"


    response = requests.get(url)
    item_data = response.json()


    item_mapping = {int(item_id): item_info['name'] for item_id, item_info in item_data['data'].items()}


    return item_mapping[itemid]


def fetch_id(ingame_region, ingame_ign, api_key):
    split_name = ingame_ign.split('#') #splits into ign and tag
    ingame_ign = split_name[0] #ign
    ingame_tag = split_name[1] #tag
    #true region calculation for api requests
    if ingame_region in ('NA', 'BR', 'LAN', 'LAS'):
        true_region = 'americas'    
    elif ingame_region in ('KR', 'JP', 'PH'):
        true_region = 'asia'
    elif ingame_region in ('EUNE', 'EUW', 'ME1', 'TR', 'RU'):
        true_region = 'europe'
    else:
        true_region = 'sea'
    #api request url
    id_api_url = f'https://{true_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{ingame_ign}/{ingame_tag}?api_key={api_key}'
    fetched_info = requests.get(id_api_url) #actual api request
    if fetched_info.status_code == 404: #if errors
        print("Invalid Ign")
        return "Invalid Ign"
    fetched_info = fetched_info.json()
    fetched_id = fetched_info['puuid']
    return fetched_id, true_region
    

def fetch_matches(ingame_region, fetched_id, true_region, api_key):
    time_zone = pytz.timezone('America/Los_Angeles')
    season_start = int(datetime(2024, 5, 15, 12, 0, 0, tzinfo=time_zone).timestamp())
    type_match = 'ranked'
    starting_index = 0
    matches_requested = 100
    if ingame_region == "PH":
        true_region = "sea"
    all_matches = []
    while True:
        matches_api_url = f'https://{true_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{fetched_id}/ids?startTime={season_start}&type={type_match}&start={starting_index}&count={matches_requested}&api_key={api_key}'
        response = requests.get(matches_api_url)
        if response.status_code != 200:
            print(f"Error fetching matches: {response.status_code}")
            break
        
        bundled_matches = response.json()
        if not bundled_matches:
            break
            
        all_matches.extend(bundled_matches)
        

        starting_index += matches_requested

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_match = {executor.submit(fetch_and_process, match, api_key, true_region, database, fetched_id): match for match in all_matches}
        for future in concurrent.futures.as_completed(future_to_match):
            if stop_event.is_set():  
                print("Stopping further processing of matches.")
                break  
            
            match_id = future_to_match[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing match ID {match_id}: {e}")
                traceback.print_exc()
        

        for future in future_to_match:
            if not future.done():
                future.cancel()

    return