from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import fetch_data
import fetch_database
import json
import os

def get_json(subject):
    script_dir = os.path.dirname(__file__)

    config_path = os.path.join(script_dir,'config.json')

    with open(config_path, 'r') as file:
        config = json.load(file)

    return config.get(subject)

API_KEY = get_json('API_KEY')

def insert_player(ign, tag, region):
    fetched_id, true_region = fetch_data.fetch_id(region, ign + '#' + tag, API_KEY)
    engine = establish_connection()
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO players(player_ign, player_tag, player_region, player_riot) VALUES (:ign, :tag, :region, :player_riot)"),{"ign": ign, "tag": tag, "region": region, "player_riot": fetched_id})

def establish_connection():
    #engine = create_engine(f'mysql+mysqlconnector://{get_json("user")}:{get_json("google_pw")}@{get_json("google_host")}/{get_json("database")}')
    engine = create_engine(f'mysql+mysqlconnector://{get_json("user")}:{get_json("host_pw")}@{get_json("host_host")}/{get_json("database")}')
    try:
        with engine.connect() as connection:
            print("Connection to the database was successful!")
    except Exception as e:
        print(f"Error: {e}")

    return engine

def fetch_player(ign, player_region):
    split_name = ign.split('#') #split the ign and the tag
    ingame_name = split_name[0] #ign
    ingame_tag = split_name[1] #tag
    engine = establish_connection() #establishes connection with database
    
    sql = """
    SELECT * FROM players
    WHERE player_ign = :ign
    AND player_tag = :tag
    AND player_region = :region
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "ign": ingame_name,
            "tag": ingame_tag,
            "region": player_region
        })
        
        #Fetch all matching rows (should be one)
        rows = result.fetchall()
        
        #Check if any rows are returned
        if rows:
            print("Player found:")
            for row in rows:
                print(row)
                return row[0]
        else:
            #if not found, then inserts a player into database
            insert_player(ingame_name, ingame_tag, player_region)
            print("Player not found. Inserted into Database")
            return "Player not found. Now inserting into Database. Please try again in about 5 minutes"

def fetch_player_id_by_puuid(puuid):
    engine = establish_connection()
    
    with engine.connect() as connection:
        query = text("SELECT player_Id FROM players WHERE player_riot = :player_riot")

        result = connection.execute(query, {"player_riot": puuid})

        row = result.fetchone()
        return row[0]

def fetch_games(player_id, champ):
    engine = establish_connection()
    with engine.connect() as connection:
        query = text("SELECT * FROM matches WHERE player_id = :player_id AND championName = :champ")
        result = connection.execute(query, {"player_id": player_id, "champ": champ})
        rows = result.fetchall()

        if not rows:
            print("No games found for this champion.")
            return 0
        champ_wins= champ_losses= champ_mid= champ_bot= total_kill= total_death= total_assit= total_kda= total_kp= total_champlvl= total_goldpermin= total_controlwards= total_stealthwards= total_magic= total_physical= total_total= total_minions= total_minionspermin= total_dmgobj = 0
        total_dmgturrets= total_dmgpermin= total_dmgpercent= total_dmgreceive= total_closedodge= total_solokill= total_q= total_w= total_e= total_r= total_turretplates= total_turrettakedown= total_enemycc= total_knockteam= total_minionfirst10= total_skillshotearly = 0
        total_skilldodge= total_skillland= total_champexp= total_champexppermin= total_gold= total_timecc=champ_top=champ_jg=champ_support = 0
        total_top_win=total_top_loss=total_jg_win=total_jg_loss=total_mid_win=total_mid_loss=total_bot_win=total_bot_loss=total_support_win=total_support_loss=top_wr=jg_wr=mid_wr=bot_wr=support_wr=0
        for row in rows:
            if row[5] == "Win":
                champ_wins += 1
            else:
                champ_losses += 1
            if row[6] == "MIDDLE":
                champ_mid += 1
                if row[5] == "Win":
                    total_mid_win += 1
                else:
                    total_mid_loss += 1
            elif row[6] == "BOTTOM":
                champ_bot += 1
                if row[5] == "Win":
                    total_bot_win += 1
                else:
                    total_bot_loss += 1
            elif row[6] == "TOP":
                champ_top += 1
                if row[5] == "Win":
                    total_top_win += 1
                else:
                    total_top_loss += 1
            elif row[6] == "JUNGLE":
                champ_jg += 1
                if row[5] == "Win":
                    total_jg_win += 1
                else:
                    total_jg_loss += 1
            else:
                champ_support += 1
                if row[5] == "Win":
                    total_support_win += 1
                else:
                    total_support_loss += 1
            if champ_mid == 0:
                mid_wr = 0
            else:
                mid_wr = round(total_mid_win / champ_mid,2)
            if champ_top == 0:
                top_wr = 0
            else:
                top_wr = round(total_top_win / champ_top,2)
            if champ_jg == 0:
                jg_wr = 0
            else:
                jg_wr = round(total_jg_win / champ_jg,2)
            if champ_bot == 0:
                bot_wr = 0
            else:
                bot_wr = round(total_bot_win / champ_bot,2)
            if champ_support == 0:
                support_wr = 0
            else:
                support_wr = round(total_support_win / champ_support,2)
            total_kill += row[7]
            total_death += row[8]
            total_assit += row[9]
            total_kda += row[10]
            total_kp += row[11]
            total_champlvl += row[12]
            total_goldpermin += row[20]
            total_controlwards += row[21]
            total_stealthwards += row[22]
            total_magic += row[23]
            total_physical += row[24]
            total_total += row[25]
            total_minions += row[26]
            total_minionspermin += row[27]
            total_dmgobj += row[28]
            total_dmgturrets += row[29]
            total_dmgpermin += row[30]
            total_dmgpercent += row[31]
            total_dmgreceive += row[32]
            total_closedodge += row[33]
            total_solokill += row[34]
            total_q += row[35]
            total_w += row[36]
            total_e += row[37]
            total_r += row[38]
            total_turretplates += row[39]
            total_turrettakedown += row[40]
            total_enemycc += row[41]
            total_knockteam += row[42]
            total_minionfirst10 += row[43]
            total_skillshotearly += row[44]
            total_skilldodge += row[45]
            total_skillland += row[46]
            total_champexp += row[47]
            total_champexppermin += row[48]
            total_gold += row[49]
            total_timecc += row[50]
            rune_list = []
            item_list = []
            for x in range(6):
                if row[51+4*x] not in rune_list:
                    rune_list.append(row[51+4*x])
                if row[13 + x] != "None":
                    if row[13 + x] not in item_list:
                        item_list.append(row[13+x])
        total_games = len(rows)
    insert_champ(player_id, champ, total_games, champ_wins, champ_losses, round(champ_wins/total_games,2), champ_bot, round(champ_bot/total_games,2), total_bot_win, total_bot_loss, bot_wr, champ_mid, round(champ_mid / total_games,2), total_mid_win, total_mid_loss, mid_wr, champ_top, round(champ_top / total_games, 2), total_top_win, total_top_loss, top_wr, champ_jg, round(champ_jg /total_games,2), total_jg_win, total_jg_loss, jg_wr, champ_support, round(champ_support / total_games, 2), total_support_win, total_support_loss, support_wr, round(total_kill/total_games,2), round(total_death/total_games,2), round(total_assit/total_games,2), round(total_kda/total_games,2), round(total_kp/total_games,2), round(total_champlvl/total_games,1), int(total_goldpermin/total_games), round(total_controlwards/total_games,1), round(total_stealthwards/total_games,1), int(total_magic/total_games), int(total_physical/total_games), int(total_total/total_games), round(total_minions/total_games,1), round(total_minionspermin/total_games,1), int(total_dmgobj/total_games), int(total_dmgturrets/total_games), int(total_dmgpermin/total_games), round(total_dmgpercent/total_games,2), round(total_dmgreceive/total_games,2), round(total_closedodge/total_games,1), round(total_solokill/total_games,1), int(total_q/total_games), int(total_w/total_games), int(total_e/total_games), round(total_r/total_games,1), round(total_turretplates/total_games,1), round(total_turrettakedown/total_games,1), round(total_enemycc/total_games,1), round(total_knockteam/total_games,1), round(total_minionfirst10/total_games,1), round(total_skillshotearly/total_games,1), round(total_skilldodge/total_games,1), round(total_skillland/total_games,1), int(total_champexp/total_games), int(total_champexppermin/total_games), int(total_gold/total_games), int(total_timecc/total_games))
    check_rune(player_id, champ, total_games, rune_list)
    check_champ(player_id, champ, total_games, item_list)
    check_opponent(player_id, champ, total_games)
    return
def insert_champ(player_id, champ_name, total_games, champ_wins, champ_losses, champ_wr, bot_count, bot_playrate, bot_win, bot_loss, bot_wr, mid_count, mid_playrate, mid_win, mid_loss, mid_wr, top_count, top_playrate, top_win, top_loss, top_wr, jg_count, jg_playrate, jg_win, jg_loss, jg_wr, support_count, support_playrate, support_win, support_loss, support_wr, avg_kills, avg_deaths, avg_assists, avg_kda, avg_kp, avg_champlvl, avg_goldPerMin, avg_control_wards, avg_stealth_wards, avg_magic_dmg, avg_physical_dmg, avg_total_dmg, avg_minions, avg_minionsPerMin, avg_obj_dmg, avg_turret_dmg, avg_dmgPerMin, avg_team_dmg_percent, avg_damage_receive, avg_dodge_close, avg_soloKill, avg_q, avg_w, avg_e, avg_r, avg_turretPlates, avg_turretTakedowns, avg_EnemyCC, avg_knockTeam, avg_minions10Min, avg_skillShotsEarly, avg_dodge, avg_SkillShots, avg_champExp, avg_champExpPerMin, avg_gold, avg_timeCC):
    engine = establish_connection()

    check_sql = """
    SELECT COUNT(*) FROM champions 
    WHERE player_id = :player_id 
    AND champ_name = :champ_name
    """
    
    update_sql = """
    UPDATE champions 
    SET 
        total_games = :total_games,
        champ_wins = :champ_wins,
        champ_losses = :champ_losses,
        champ_wr = :champ_wr,
        bot_count = :bot_count,
        bot_playrate = :bot_playrate,
        bot_win = :bot_win,
        bot_loss = :bot_loss,
        bot_wr = :bot_wr,
        mid_count = :mid_count,
        mid_playrate = :mid_playrate,
        mid_win = :mid_win,
        mid_loss = :mid_loss,
        mid_wr = :mid_wr,
        top_count = :top_count,
        top_playrate = :top_playrate,
        top_win = :top_win,
        top_loss = :top_loss,
        top_wr = :top_wr,
        jg_count = :jg_count,
        jg_playrate = :jg_playrate,
        jg_win = :jg_win,
        jg_loss = :jg_loss,
        jg_wr = :jg_wr,
        support_count = :support_count,
        support_playrate = :support_playrate,
        support_win = :support_win,
        support_loss = :support_loss,
        support_wr = :support_wr,
        avg_kills = :avg_kills,
        avg_deaths = :avg_deaths,
        avg_assists = :avg_assists,
        avg_kda = :avg_kda,
        avg_kp = :avg_kp,
        avg_champlvl = :avg_champlvl,
        avg_goldPerMin = :avg_goldPerMin,
        avg_control_wards = :avg_control_wards,
        avg_stealth_wards = :avg_stealth_wards,
        avg_magic_dmg = :avg_magic_dmg,
        avg_physical_dmg = :avg_physical_dmg,
        avg_total_dmg = :avg_total_dmg,
        avg_minions = :avg_minions,
        avg_minionsPerMin = :avg_minionsPerMin,
        avg_obj_dmg = :avg_obj_dmg,
        avg_turret_dmg = :avg_turret_dmg,
        avg_dmgPerMin = :avg_dmgPerMin,
        avg_team_dmg_percent = :avg_team_dmg_percent,
        avg_damage_receive = :avg_damage_receive,
        avg_dodge_close = :avg_dodge_close,
        avg_soloKill = :avg_soloKill,
        avg_q = :avg_q,
        avg_w = :avg_w,
        avg_e = :avg_e,
        avg_r = :avg_r,
        avg_turretPlates = :avg_turretPlates,
        avg_turretTakedowns = :avg_turretTakedowns,
        avg_EnemyCC = :avg_EnemyCC,
        avg_knockTeam = :avg_knockTeam,
        avg_minions10Min = :avg_minions10Min,
        avg_skillShotsEarly = :avg_skillShotsEarly,
        avg_dodge = :avg_dodge,
        avg_SkillShots = :avg_SkillShots,
        avg_champExp = :avg_champExp,
        avg_champExpPerMin = :avg_champExpPerMin,
        avg_gold = :avg_gold,
        avg_timeCC = :avg_timeCC
    WHERE player_id = :player_id 
    AND champ_name = :champ_name
    """
    
    insert_sql = """
    INSERT INTO champions (
        player_id, champ_name, total_games, champ_wins, champ_losses, champ_wr, bot_count, bot_playrate, bot_win, bot_loss, bot_wr, mid_count, mid_playrate, mid_win, mid_loss, mid_wr, top_count, top_playrate, top_win, top_loss, top_wr, jg_count, jg_playrate, jg_win, jg_loss, jg_wr, support_count, support_playrate, support_win, support_loss, support_wr, avg_kills, avg_deaths,
        avg_assists, avg_kda, avg_kp, avg_champlvl, avg_goldPerMin,
        avg_control_wards, avg_stealth_wards, avg_magic_dmg, avg_physical_dmg,
        avg_total_dmg, avg_minions, avg_minionsPerMin, avg_obj_dmg,
        avg_turret_dmg, avg_dmgPerMin, avg_team_dmg_percent, avg_damage_receive, avg_dodge_close,
        avg_soloKill, avg_q, avg_w, avg_e, avg_r, avg_turretPlates,
        avg_turretTakedowns, avg_EnemyCC, avg_knockTeam, avg_minions10Min,
        avg_skillShotsEarly, avg_dodge, avg_SkillShots, avg_champExp,
        avg_champExpPerMin, avg_gold, avg_timeCC
    ) VALUES (
        :player_id, :champ_name, :total_games, :champ_wins, :champ_losses, :champ_wr, :bot_count, :bot_playrate, :bot_win, :bot_loss, :bot_wr, :mid_count, :mid_playrate, :mid_win, :mid_loss, :mid_wr, :top_count, :top_playrate, :top_win, :top_loss, :top_wr, :jg_count, :jg_playrate, :jg_win, :jg_loss, :jg_wr, :support_count, :support_playrate, :support_win, :support_loss, :support_wr, :avg_kills, :avg_deaths,
        :avg_assists, :avg_kda, :avg_kp, :avg_champlvl, :avg_goldPerMin,
        :avg_control_wards, :avg_stealth_wards, :avg_magic_dmg, :avg_physical_dmg,
        :avg_total_dmg, :avg_minions, :avg_minionsPerMin, :avg_obj_dmg,
        :avg_turret_dmg, :avg_dmgPerMin, :avg_team_dmg_percent, :avg_damage_receive, :avg_dodge_close,
        :avg_soloKill, :avg_q, :avg_w, :avg_e, :avg_r, :avg_turretPlates,
        :avg_turretTakedowns, :avg_EnemyCC, :avg_knockTeam, :avg_minions10Min,
        :avg_skillShotsEarly, :avg_dodge, :avg_SkillShots, :avg_champExp,
        :avg_champExpPerMin, :avg_gold, :avg_timeCC
    )
    """
    
    with engine.connect() as connection:
        transaction = connection.begin()
        try:

            result = connection.execute(text(check_sql), {
                "player_id": player_id,
                "champ_name": champ_name
            })
            

            count = result.scalar()
            print(f"Check count: {count}")
            
            if count > 0:

                connection.execute(text(update_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "total_games": total_games,
                    "champ_wins": champ_wins,
                    "champ_losses": champ_losses,
                    "champ_wr": champ_wr,
                    "bot_count": bot_count,
                    "bot_playrate": bot_playrate,
                    "bot_win": bot_win,
                    "bot_loss": bot_loss,
                    "bot_wr": bot_wr,
                    "mid_count": mid_count,
                    "mid_playrate": mid_playrate,
                    "mid_win": mid_win,
                    "mid_loss": mid_loss,
                    "mid_wr": mid_wr,
                    "top_count": top_count,
                    "top_playrate": top_playrate,
                    "top_win": top_win,
                    "top_loss": top_loss,
                    "top_wr": top_wr,
                    "jg_count": jg_count,
                    "jg_playrate": jg_playrate,
                    "jg_win": jg_win,
                    "jg_loss": jg_loss,
                    "jg_wr": jg_wr,
                    "support_count": support_count,
                    "support_playrate": support_playrate,
                    "support_win": support_win,
                    "support_loss": support_loss,
                    "support_wr": support_wr,
                    "avg_kills": avg_kills,
                    "avg_deaths": avg_deaths,
                    "avg_assists": avg_assists,
                    "avg_kda": avg_kda,
                    "avg_kp": avg_kp,
                    "avg_champlvl": avg_champlvl,
                    "avg_goldPerMin": avg_goldPerMin,
                    "avg_control_wards": avg_control_wards,
                    "avg_stealth_wards": avg_stealth_wards,
                    "avg_magic_dmg": avg_magic_dmg,
                    "avg_physical_dmg": avg_physical_dmg,
                    "avg_total_dmg": avg_total_dmg,
                    "avg_minions": avg_minions,
                    "avg_minionsPerMin": avg_minionsPerMin,
                    "avg_obj_dmg": avg_obj_dmg,
                    "avg_turret_dmg": avg_turret_dmg,
                    "avg_dmgPerMin": avg_dmgPerMin,
                    "avg_team_dmg_percent": avg_team_dmg_percent,
                    "avg_damage_receive": avg_damage_receive,
                    "avg_dodge_close": avg_dodge_close,
                    "avg_soloKill": avg_soloKill,
                    "avg_q": avg_q,
                    "avg_w": avg_w,
                    "avg_e": avg_e,
                    "avg_r": avg_r,
                    "avg_turretPlates": avg_turretPlates,
                    "avg_turretTakedowns": avg_turretTakedowns,
                    "avg_EnemyCC": avg_EnemyCC,
                    "avg_knockTeam": avg_knockTeam,
                    "avg_minions10Min": avg_minions10Min,
                    "avg_skillShotsEarly": avg_skillShotsEarly,
                    "avg_dodge": avg_dodge,
                    "avg_SkillShots": avg_SkillShots,
                    "avg_champExp": avg_champExp,
                    "avg_champExpPerMin": avg_champExpPerMin,
                    "avg_gold": avg_gold,
                    "avg_timeCC": avg_timeCC
                })
            else:

                connection.execute(text(insert_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "total_games": total_games,
                    "champ_wins": champ_wins,
                    "champ_losses": champ_losses,
                    "champ_wr": champ_wr,
                    "bot_count": bot_count,
                    "bot_playrate": bot_playrate,
                    "bot_win": bot_win,
                    "bot_loss": bot_loss,
                    "bot_wr": bot_wr,
                    "mid_count": mid_count,
                    "mid_playrate": mid_playrate,
                    "mid_win": mid_win,
                    "mid_loss": mid_loss,
                    "mid_wr": mid_wr,
                    "top_count": top_count,
                    "top_playrate": top_playrate,
                    "top_win": top_win,
                    "top_loss": top_loss,
                    "top_wr": top_wr,
                    "jg_count": jg_count,
                    "jg_playrate": jg_playrate,
                    "jg_win": jg_win,
                    "jg_loss": jg_loss,
                    "jg_wr": jg_wr,
                    "support_count": support_count,
                    "support_playrate": support_playrate,
                    "support_win": support_win,
                    "support_loss": support_loss,
                    "support_wr": support_wr,
                    "avg_kills": avg_kills,
                    "avg_deaths": avg_deaths,
                    "avg_assists": avg_assists,
                    "avg_kda": avg_kda,
                    "avg_kp": avg_kp,
                    "avg_champlvl": avg_champlvl,
                    "avg_goldPerMin": avg_goldPerMin,
                    "avg_control_wards": avg_control_wards,
                    "avg_stealth_wards": avg_stealth_wards,
                    "avg_magic_dmg": avg_magic_dmg,
                    "avg_physical_dmg": avg_physical_dmg,
                    "avg_total_dmg": avg_total_dmg,
                    "avg_minions": avg_minions,
                    "avg_minionsPerMin": avg_minionsPerMin,
                    "avg_obj_dmg": avg_obj_dmg,
                    "avg_turret_dmg": avg_turret_dmg,
                    "avg_dmgPerMin": avg_dmgPerMin,
                    "avg_team_dmg_percent": avg_team_dmg_percent,
                    "avg_damage_receive": avg_damage_receive,
                    "avg_dodge_close": avg_dodge_close,
                    "avg_soloKill": avg_soloKill,
                    "avg_q": avg_q,
                    "avg_w": avg_w,
                    "avg_e": avg_e,
                    "avg_r": avg_r,
                    "avg_turretPlates": avg_turretPlates,
                    "avg_turretTakedowns": avg_turretTakedowns,
                    "avg_EnemyCC": avg_EnemyCC,
                    "avg_knockTeam": avg_knockTeam,
                    "avg_minions10Min": avg_minions10Min,
                    "avg_skillShotsEarly": avg_skillShotsEarly,
                    "avg_dodge": avg_dodge,
                    "avg_SkillShots": avg_SkillShots,
                    "avg_champExp": avg_champExp,
                    "avg_champExpPerMin": avg_champExpPerMin,
                    "avg_gold": avg_gold,
                    "avg_timeCC": avg_timeCC
                })
            

            transaction.commit()
        except Exception as e:

            transaction.rollback()
            raise e
def check_rune(player_id, champ_name, total_games, rune_list):
  
    engine = establish_connection()

    base_query = """
    SELECT * FROM matches 
    WHERE player_id = :player_id 
    AND championName = :champ_name 
    AND (
        PRune_1_0 = :rune 
        OR PRune_2_0 = :rune 
        OR PRune_3_0 = :rune 
        OR PRune_4_0 = :rune 
        OR SRune_1_0 = :rune 
        OR SRune_2_0 = :rune
    )
    """
    
    with engine.connect() as connection:
        for rune in rune_list:
            query = text(base_query)
            result = connection.execute(query, {"player_id": player_id, "champ_name": champ_name, "rune": rune})
            rows = result.fetchall()
            rune_count = len(rows)
            if rune_count == 0:
                continue
            avg_var1 = 0
            avg_var2 = 0
            avg_var3 = 0
            rune_win = 0
            rune_loss = 0
            for row in rows:
                if row[5] == 'Win':
                    rune_win += 1
                else:
                    rune_loss += 1
                for x in range(6):
                    if row[51+4*x] == rune:
                        avg_var1 += row[52 + 4 * x]
                        avg_var2 += row[53 + 4 * x]
                        avg_var3 += row[54 + 4 * x]
            avg_var1 = avg_var1 / rune_count
            avg_var2 = avg_var2 / rune_count
            avg_var3 = avg_var3 / rune_count
            rune_wr = rune_win / rune_count
            rune_pickrate = rune_count / total_games
            insert_rune(player_id, champ_name, rune, rune_count, rune_win, rune_loss, round(rune_wr,2), round(rune_pickrate,2), avg_var1, avg_var2, avg_var3)
def insert_rune(player_id, champ_name, rune_name, rune_count, rune_win, rune_loss, rune_wr, rune_pickrate, avg_rune_var1, avg_rune_var2, avg_rune_var3):
    engine = establish_connection()
    

    check_sql = """
    SELECT COUNT(*) FROM runes 
    WHERE player_id = :player_id 
    AND champ_name = :champ_name 
    AND rune_name = :rune_name
    """
    

    update_sql = """
    UPDATE runes 
    SET 
        rune_count = :rune_count,
        rune_win = :rune_win,
        rune_loss = :rune_loss,
        rune_wr = :rune_wr,
        rune_pickrate = :rune_pickrate,
        avg_rune_var1 = :avg_rune_var1,
        avg_rune_var2 = :avg_rune_var2,
        avg_rune_var3 = :avg_rune_var3
    WHERE player_id = :player_id 
    AND champ_name = :champ_name 
    AND rune_name = :rune_name
    """
    

    insert_sql = """
    INSERT INTO runes (
        player_id, champ_name, rune_name, rune_count, rune_win, rune_loss, rune_wr, rune_pickrate, avg_rune_var1, avg_rune_var2, avg_rune_var3
    ) VALUES (
        :player_id, :champ_name, :rune_name, :rune_count, :rune_win, :rune_loss, :rune_wr, :rune_pickrate, :avg_rune_var1, :avg_rune_var2, :avg_rune_var3
    )
    """
    
    with engine.connect() as connection:
        transaction = connection.begin()
        try:

            result = connection.execute(text(check_sql), {
                "player_id": player_id,
                "champ_name": champ_name,
                "rune_name": rune_name
            })
            

            count = result.scalar()
            print(f"Check count: {count}")
            
            if count > 0:

                connection.execute(text(update_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "rune_name": rune_name,
                    "rune_count": rune_count,
                    "rune_win": rune_win,
                    "rune_loss": rune_loss,
                    "rune_wr": rune_wr,
                    "rune_pickrate": rune_pickrate,
                    "avg_rune_var1": avg_rune_var1,
                    "avg_rune_var2": avg_rune_var2,
                    "avg_rune_var3": avg_rune_var3
                })
                print(f"Updated record for player_id: {player_id}, champ_name: {champ_name}, rune_name: {rune_name}")
            else:

                connection.execute(text(insert_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "rune_name": rune_name,
                    "rune_count": rune_count,
                    "rune_win": rune_win,
                    "rune_loss": rune_loss,
                    "rune_wr": rune_wr,
                    "rune_pickrate": rune_pickrate,
                    "avg_rune_var1": avg_rune_var1,
                    "avg_rune_var2": avg_rune_var2,
                    "avg_rune_var3": avg_rune_var3
                })
                print(f"Inserted new record for player_id: {player_id}, champ_name: {champ_name}, rune_name: {rune_name}")
            
            transaction.commit()
        except Exception as e:
            print(f"Error: {e}")
            transaction.rollback() 
def check_champ(player_id, champ_name, total_games, item_list):
    
    engine = establish_connection()
    

    base_query = """
    SELECT * FROM matches 
    WHERE player_id = :player_id 
    AND championName = :champ_name 
    AND (
        item0 = :item
        OR item1 = :item
        OR item2 = :item
        OR item3 = :item
        OR item4 = :item
        OR item5 = :item
        OR item6 = :item
    )
    """
    
    with engine.connect() as connection:
        for item in item_list:
            query = text(base_query)
            result = connection.execute(query, {"player_id": player_id, "champ_name": champ_name, "item": item})
            rows = result.fetchall()
            item_count = len(rows)
            if item_count == 0:
                continue
            item_win = 0
            item_loss = 0
            for row in rows:
                if row[5] == 'Win':
                    item_win += 1
                else:
                    item_loss += 1
            item_wr = item_win / item_count
            item_pickrate = item_count / total_games
            insert_item(player_id, champ_name, item, item_count, item_win, item_loss, round(item_wr,2), round(item_pickrate,2))

def insert_item(player_id, champ_name, item_name, item_count, item_win, item_loss, item_wr, item_pickrate):
    engine = establish_connection()
    

    check_sql = """
    SELECT COUNT(*) FROM items 
    WHERE player_id = :player_id 
    AND champ_name = :champ_name 
    AND item_name = :item_name
    """

    update_sql = """
    UPDATE items 
    SET 
        item_count = :item_count,
        item_win = :item_win,
        item_loss = :item_loss,
        item_wr = :item_wr,
        item_pickrate = :item_pickrate
    WHERE player_id = :player_id 
    AND champ_name = :champ_name 
    AND item_name = :item_name
    """

    insert_sql = """
    INSERT INTO items (
        player_id, champ_name, item_name, item_count, item_win, item_loss, item_wr, item_pickrate
    ) VALUES (
        :player_id, :champ_name, :item_name, :item_count, :item_win, :item_loss, :item_wr, :item_pickrate
    )
    """
    
    with engine.connect() as connection:
        transaction = connection.begin()
        try:

            result = connection.execute(text(check_sql), {
                "player_id": player_id,
                "champ_name": champ_name,
                "item_name": item_name
            })
            

            count = result.scalar()
            print(f"Check count: {count}") 
            
            if count > 0:

                connection.execute(text(update_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "item_name": item_name,
                    "item_count": item_count,
                    "item_win": item_win,
                    "item_loss": item_loss,
                    "item_wr": item_wr,
                    "item_pickrate": item_pickrate,

                })
                print(f"Updated record for player_id: {player_id}, champ_name: {champ_name}, item_name: {item_name}")
            else:

                connection.execute(text(insert_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "item_name": item_name,
                    "item_count": item_count,
                    "item_win": item_win,
                    "item_loss": item_loss,
                    "item_wr": item_wr,
                    "item_pickrate": item_pickrate,
                })
                print(f"Inserted new record for player_id: {player_id}, champ_name: {champ_name}, item_name: {item_name}")
            
            transaction.commit() 
        except Exception as e:
            print(f"Error: {e}")
            transaction.rollback()



def match_already_exists(match_id):
    engine = establish_connection()
    with engine.connect() as connection:
        query = text("SELECT COUNT(*) FROM matches WHERE match_code = :match_id")
        result = connection.execute(query, {"match_id": match_id})
        return result.fetchone()[0] > 0

def insert_game(match_code, player_id, championName, gameDuration, result, lane, kills, deaths, assists, kda, killParticipation, champLevel, item0, item1, item2, item3, item4, item5, item6, goldPerMinute, controlWardsPlaced, stealthWardsPlaced, magicDamageDealtToChampions, physicalDamageDealtToChampions, totalDamageDealtToChampions, totalMinionsKilled, minionsPerMinute, damageDealtToObjectives, damageDealtToTurrets, damagePerMinute, teamDamagePercentage, damageTakenOnTeamPercentage, dodgeSkillShotsSmallWindow, soloKills, q_cast, w_cast, e_cast, r_cast, turretPlatesTaken, turretTakedowns, enemyChampionImmobilizations, knockEnemyIntoTeamAndKill, laneMinionsFirst10Minutes, landSkillShotsEarlyGame, skillshotsDodged, skillshotsHit, champExperience, champExpPerMin, goldEarned, totalTimeCCDealt, PRune_1_0, PRune_1_1, PRune_1_2, PRune_1_3, PRune_2_0, PRune_2_1, PRune_2_2, PRune_2_3, PRune_3_0, PRune_3_1, PRune_3_2, PRune_3_3, PRune_4_0, PRune_4_1, PRune_4_2, PRune_4_3, SRune_1_0, SRune_1_1, SRune_1_2, SRune_1_3, SRune_2_0, SRune_2_1, SRune_2_2, SRune_2_3, opponent, date):
    engine = establish_connection()
    sql = """
    INSERT INTO matches (match_code, player_id, championName, gameDuration, result, lane, kills, deaths, assists, kda,
                         killParticipation, champLevel, item0, item1, item2, item3, item4, item5, item6, goldPerMinute,
                         controlWardsPlaced, stealthWardsPlaced, magicDamageDealtToChampions, physicalDamageDealtToChampions,
                         totalDamageDealtToChampions, totalMinionsKilled, minionsPerMinute, damageDealtToObjectives,
                         damageDealtToTurrets, damagePerMinute, teamDamagePercentage, damageTakenOnTeamPercentage,
                         dodgeSkillShotsSmallWindow, soloKills, q_cast, w_cast, e_cast, r_cast, turretPlatesTaken,
                         turretTakedowns, enemyChampionImmobilizations, knockEnemyIntoTeamAndKill, laneMinionsFirst10Minutes,
                         landSkillShotsEarlyGame, skillshotsDodged, skillshotsHit, champExperience, champExpPerMin, goldEarned,
                         totalTimeCCDealt, PRune_1_0, PRune_1_1, PRune_1_2, PRune_1_3, PRune_2_0, PRune_2_1, PRune_2_2,
                         PRune_2_3, PRune_3_0, PRune_3_1, PRune_3_2, PRune_3_3, PRune_4_0, PRune_4_1, PRune_4_2,
                         PRune_4_3, SRune_1_0, SRune_1_1, SRune_1_2, SRune_1_3, SRune_2_0, SRune_2_1, SRune_2_2, SRune_2_3, opponent, date)
    VALUES (:match_code, :player_id, :championName, :gameDuration, :result, :lane, :kills, :deaths, :assists, :kda,
            :killParticipation, :champLevel, :item0, :item1, :item2, :item3, :item4, :item5, :item6, :goldPerMinute,
            :controlWardsPlaced, :stealthWardsPlaced, :magicDamageDealtToChampions, :physicalDamageDealtToChampions,
            :totalDamageDealtToChampions, :totalMinionsKilled, :minionsPerMinute, :damageDealtToObjectives,
            :damageDealtToTurrets, :damagePerMinute, :teamDamagePercentage, :damageTakenOnTeamPercentage,
            :dodgeSkillShotsSmallWindow, :soloKills, :q_cast, :w_cast, :e_cast, :r_cast, :turretPlatesTaken,
            :turretTakedowns, :enemyChampionImmobilizations, :knockEnemyIntoTeamAndKill, :laneMinionsFirst10Minutes,
            :landSkillShotsEarlyGame, :skillshotsDodged, :skillshotsHit, :champExperience, :champExpPerMin, :goldEarned,
            :totalTimeCCDealt, :PRune_1_0, :PRune_1_1, :PRune_1_2, :PRune_1_3, :PRune_2_0, :PRune_2_1, :PRune_2_2,
            :PRune_2_3, :PRune_3_0, :PRune_3_1, :PRune_3_2, :PRune_3_3, :PRune_4_0, :PRune_4_1, :PRune_4_2,
            :PRune_4_3, :SRune_1_0, :SRune_1_1, :SRune_1_2, :SRune_1_3, :SRune_2_0, :SRune_2_1, :SRune_2_2, :SRune_2_3, :opponent, :date)
    """

    with engine.begin() as connection:
        connection.execute(text(sql), {
            "match_code": match_code,
            "player_id": player_id,
            "championName": championName,
            "gameDuration": gameDuration,
            "result": result,
            "lane": lane,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda": kda,
            "killParticipation": killParticipation,
            "champLevel": champLevel,
            "item0": item0,
            "item1": item1,
            "item2": item2,
            "item3": item3,
            "item4": item4,
            "item5": item5,
            "item6": item6,
            "goldPerMinute": goldPerMinute,
            "controlWardsPlaced": controlWardsPlaced,
            "stealthWardsPlaced": stealthWardsPlaced,
            "magicDamageDealtToChampions": magicDamageDealtToChampions,
            "physicalDamageDealtToChampions": physicalDamageDealtToChampions,
            "totalDamageDealtToChampions": totalDamageDealtToChampions,
            "totalMinionsKilled": totalMinionsKilled,
            "minionsPerMinute": minionsPerMinute,
            "damageDealtToObjectives": damageDealtToObjectives,
            "damageDealtToTurrets": damageDealtToTurrets,
            "damagePerMinute": damagePerMinute,
            "teamDamagePercentage": teamDamagePercentage,
            "damageTakenOnTeamPercentage": damageTakenOnTeamPercentage,
            "dodgeSkillShotsSmallWindow": dodgeSkillShotsSmallWindow,
            "soloKills": soloKills,
            "q_cast": q_cast,
            "w_cast": w_cast,
            "e_cast": e_cast,
            "r_cast": r_cast,
            "turretPlatesTaken": turretPlatesTaken,
            "turretTakedowns": turretTakedowns,
            "enemyChampionImmobilizations": enemyChampionImmobilizations,
            "knockEnemyIntoTeamAndKill": knockEnemyIntoTeamAndKill,
            "laneMinionsFirst10Minutes": laneMinionsFirst10Minutes,
            "landSkillShotsEarlyGame": landSkillShotsEarlyGame,
            "skillshotsDodged": skillshotsDodged,
            "skillshotsHit": skillshotsHit,
            "champExperience": champExperience,
            "champExpPerMin": champExpPerMin,
            "goldEarned": goldEarned,
            "totalTimeCCDealt": totalTimeCCDealt,
            "PRune_1_0": PRune_1_0,
            "PRune_1_1": PRune_1_1,
            "PRune_1_2": PRune_1_2,
            "PRune_1_3": PRune_1_3,
            "PRune_2_0": PRune_2_0,
            "PRune_2_1": PRune_2_1,
            "PRune_2_2": PRune_2_2,
            "PRune_2_3": PRune_2_3,
            "PRune_3_0": PRune_3_0,
            "PRune_3_1": PRune_3_1,
            "PRune_3_2": PRune_3_2,
            "PRune_3_3": PRune_3_3,
            "PRune_4_0": PRune_4_0,
            "PRune_4_1": PRune_4_1,
            "PRune_4_2": PRune_4_2,
            "PRune_4_3": PRune_4_3,
            "SRune_1_0": SRune_1_0,
            "SRune_1_1": SRune_1_1,
            "SRune_1_2": SRune_1_2,
            "SRune_1_3": SRune_1_3,
            "SRune_2_0": SRune_2_0,
            "SRune_2_1": SRune_2_1,
            "SRune_2_2": SRune_2_2,
            "SRune_2_3": SRune_2_3,
            "opponent": opponent,
            "date": date
        })
    return


def check_opponent(player_id, champ_name, total_games):
    champ_list = fetch_database.fetch_unique_opponents(player_id)
    engine = establish_connection()
    lane_list = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]

    base_query = """
    SELECT * FROM matches 
    WHERE player_id = :player_id 
    AND championName = :champ_name
    AND lane = :lane
    AND opponent = :opponent
    """
    
    with engine.connect() as connection:
        for lane in lane_list:
            for champ in champ_list:
                query = text(base_query)
                result = connection.execute(query, {"player_id": player_id, "champ_name": champ_name, "lane": lane, "opponent": champ})
                rows = result.fetchall()
                opponent_count = len(rows)
                if opponent_count == 0:
                    continue
                opponent_win = 0
                opponent_loss = 0
                for row in rows:
                    if row[5] == 'Win':
                        opponent_win += 1
                    else:
                        opponent_loss += 1
                opponent_wr = opponent_win / opponent_count
                opponent_pickrate = opponent_count / total_games
                insert_opponent(player_id, champ_name, champ, lane, opponent_count, opponent_win, opponent_loss, round(opponent_wr,2), round(opponent_pickrate,2))

def insert_opponent(player_id, champ_name, opponent_name, lane, matchup_count, matchup_win, matchup_loss, matchup_wr, matchup_playrate):
    engine = establish_connection()
    

    check_sql = """
    SELECT COUNT(*) FROM matchups 
    WHERE player_id = :player_id 
    AND champ_name = :champ_name 
    AND opponent_name = :opponent_name
    AND lane = :lane
    """
    

    update_sql = """
    UPDATE matchups 
    SET 
        matchup_count = :matchup_count,
        matchup_win = :matchup_win,
        matchup_loss = :matchup_loss,
        matchup_wr = :matchup_wr,
        matchup_playrate = :matchup_playrate
    WHERE player_id = :player_id 
    AND champ_name = :champ_name 
    AND opponent_name = :opponent_name
    AND lane = :lane
    """
    

    insert_sql = """
    INSERT INTO matchups (
        player_id, champ_name, opponent_name, lane, matchup_count, matchup_win, matchup_loss, matchup_wr, matchup_playrate
    ) VALUES (
        :player_id, :champ_name, :opponent_name, :lane, :matchup_count, :matchup_win, :matchup_loss, :matchup_wr, :matchup_playrate
    )
    """
    
    with engine.connect() as connection:
        transaction = connection.begin()
        try:

            result = connection.execute(text(check_sql), {
                "player_id": player_id,
                "champ_name": champ_name,
                "opponent_name": opponent_name,
                "lane": lane
            })
            

            count = result.scalar()
            print(f"Check count: {count}")
            
            if count > 0:

                connection.execute(text(update_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "opponent_name": opponent_name,
                    "lane": lane,
                    "matchup_count": matchup_count,
                    "matchup_win": matchup_win,
                    "matchup_loss": matchup_loss,
                    "matchup_wr": matchup_wr,
                    "matchup_playrate": matchup_playrate,
                })
                print(f"Updated record for player_id: {player_id}, champ_name: {champ_name}, opponent_name: {opponent_name}")
            else:

                connection.execute(text(insert_sql), {
                    "player_id": player_id,
                    "champ_name": champ_name,
                    "opponent_name": opponent_name,
                    "lane": lane,
                    "matchup_count": matchup_count,
                    "matchup_win": matchup_win,
                    "matchup_loss": matchup_loss,
                    "matchup_wr": matchup_wr,
                    "matchup_playrate": matchup_playrate,
                })
                print(f"Inserted new record for player_id: {player_id}, champ_name: {champ_name}, opponent_name: {opponent_name}")
            
            transaction.commit() 
        except Exception as e:
            print(f"Error: {e}")
            transaction.rollback()