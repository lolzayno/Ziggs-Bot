from discord import Embed
import textwrap
ahri_matchup = f"""
- Early game, she will poke using her W, walking up and activiting electrecute
- Ahri's movement speed she gains from her W makes her difficult to hit
- Dodge left to right since Ahri's abilities all go straight
- Really slippery with her ult and movement enhancement from her W, will be difficult to land abilities
- Consider holding onto your ult for a finisher since Ahri can easily Dash out of it using her R
- If you dodge her E (Charm), she won't do nearly as much damage
- If she uses R, you have very small windows to land abilities since theres a small cooldown in between dashes
- Most likely, she will through her charm after completing her first dash, be ready
- Probably look to satchel away once she ults
- If she misses her E (charm), you can walk up and be aggresive
"""

akali_matchup = f"""
- Early game (Before level 6), look to be aggresive and throw Q's and auto attacks everytime she walks to farm
- When she uses her W (Shroud), look to back up back towards your turret, the invisibility makes it impossible to trade with her
- Move left to right when dodging her E (Shuriken), she won't do nearly as much damage if you manage to side step it
- If she lands E (Shuriken), you can satchel her away as shes dashing in to negate the damage
- If she misses her E, you can look to walk up and be aggresive
- If you are low, be careful of her all in, she can E in the direction towards you and ult in, closing the gap
- Beware of her flashing in to gap close and ult you to execute
"""

akshan_matchup = f"""
- Don't let him auto attack you freely in lane
- Since his autoattacks typically shoot 2 in a row, you have a chance to poke him in that small window of time
- Save W (Satchel) for Akshan's E (Grapple), you should be satcheling yourself and him at the sametime (pushing you to safety and him backwards)
- Only use W (Satchel) offensively if you know you can kill him
- Don't line up behind the minions, Akshan's Q (Boomarang) will make you an easy target to hit, put yourself at an angle where it can't hit you if he decides to use it on the minions
- Be careful for his invisibility, always assume he's nearby unless you saw him recall back to base
- You can dodge his ult by standing behind minions, monsters, or your turret
"""

anivia_matchup = f"""
- Look to be aggresive with your Q's in lane, she has poor mobility and short range
- Take advantage of the range difference
- Dodge side to side when avoiding Anivia's Q
- You can use your W (Satchel) to hop over Anivia's W (Wall)
- Your W (Satchel) can cancel her ult if you knock her up with it
- If she W's (walls) you into her ult, you can satchel over the wall to safety
- It's possible for her to W (wall) you mid satchel, canceling your jump
"""

annie_matchup = f"""
- Look to be aggresive with your Q's in lane, you out range her
- Watch if she has her stun, play more safe when her stun is available
- If you are low, she will always look to flash ult you
- Careful for her movement speed boost from her E (shield)
"""

aurelionsol_matchup = f"""
- Look to Q him when he is using his Q (Breath) because he's stationary
- Take advantage of the range difference
- Save W (satchel) for Aurelion Sol's W (Flight), satchel him away when he's flying towards you
- Primarily poke in this lane, you shouldn't take extended trades since Asol's breath will shred your HP
- Don't go first strike in this match up!
"""

azir_matchup = f"""
- Look to be aggresive with your Q's in lane, he has poor mobility and short range
- Take advantage of the range difference
- Stay out of auto attack range of his soliders
- At level 6, don't be too aggresive towards his turret, he can push you in if over extended
- Time your Q with Azir's solider auto attacks
"""

brand_matchup = f"""
- Look to be aggressive with your Q's in lane, he has poor mobility
- Take advantage of the range difference
- Stay far away from minions when he uses abilities on minions, it will deal damage to you
- If you get hit by one of his abilities, look to side step his Q because it stuns you
"""

cassiopeia_matchup = f"""
- Look to be aggressive with your Q's in lane, she has poor mobility and short range
- Take advantage of the range difference
- Dodge side to side to avoid her Q, once she lands one, she will E (twin fang) you to death
- If you can, satchel away if she chases you (only if you aren't stuck in her W)
- Her W grounds you so you're W (satchel) won't propell yourself to safety
- If you are chasing her, be careful for her ult because she can turn around and ult you
"""

corki_matchup = f"""
- Stay at a relatively far range, corki destroys you close range
- Take advantage of the range difference
- Avoid all close range combat, you will most likely lose because of his E (Gattling Gun)
- Hold onto your Ult until he uses his W
- Dodge side to side to avoid his R (Rockets)
- Satchel away if he decides to jump you with his W
"""

diana_matchup = f"""
- Early game, look to be aggresive when she walks up to farm by using Q and auto attacking her
- She has two dashes if she lands Q on you or minions, refrain from flashing if this happens
- You can cancel her dash if you anticipate it with your satchel
"""

ekko_matchup = f"""
- Look to be aggresive when he walks up to farm by using Q and auto attacking him
- Be careful if he goes missing, he could use W to surprise you and stun and kill you
- His E + Q combo does extreme amount of damage and gets him back to safety, poke from a safe range
- Hold your ult until he uses his ult
- Enemy Ekko will look to constantly shove in the wave with his Q and look to surprise you with W to kill you out of vision
- To counter his push, look to be aggresive on enemy minions if he is shoving
"""

fizz_matchup = f"""
- Look to be aggresive when he walks up to farm by using Q and auto attacking him
- He can dodge all your abilities using E (Playful Trickster)
- If you time it right, you can cancel his Q using satchel (typically place satchel down while your ulted, fizz typically ults you and walks up to Q you. Here you can cancel his Q with your satchel)
- Need to respect him once he gets ult, he will 100 to 0 you if you don't respect him
- Hold your ult until he uses E (Playful Trickster)
- Good Fizz players will Q the minions and hide his ult animation by casting it mid Q, be aware
"""

galio_matchup = f"""
- Look to be aggresive when he walks up to farm by using Q and auto attacking him
- If he walks up to you to taunt, you can satchel him away
- If he's going in, most likely you are getting ganked
- If he ults away, push and hit tower if the fight is too far away to impact
"""

hwei_matchup = f"""
- Look to be aggresive with your Q's since he has poor mobility
- Dodge his pull/grab by moving up and down
- Dodge his missles by moving left to right
- You can satchel away if you are rooted
- If you are low, be aware of his long range ability
"""

irelia_matchup = f"""
- Look to be aggresive when she walks up to farm by using Q and auto attacking her
- You must dodge her E, or else you will probably die (side to side or up and down)
- You can cancel her Q if you time it well using W (Satchel)
- Be aware of low health minions, she can dash to it to get resets to close gap between you and her
"""

kassadin_matchup = f"""
- Look to be EXTREMELY aggresive in the early game by poking him using Q and auto attacks while he farms
- Once he hits level 6, the lane becomes a lot more difficult, must respect him once he gets ult
- His passive gives him extra resistance to AP damage, so its essential you auto attack him as much as you can before he's level 6
- If he ults on you, you can W (Satchel) away
"""

katarina_matchup = f"""
- Look to be aggresive in the early game by poking her using Q and auto attacks while she farms
- If she throws a dagger, assume most times she will dash to it
- Stay away from daggers on the ground
- If she dashes on you, you can always W (Satchel) away
"""

leblanc_matchup = f"""
- Primarily look to just focus on farming in this lane, you will most likely not solo kill her
- Extremely slippery so its hard to land abilities and kill her
- Hold your ult until she uses her W (Dash) if you are looking to finish her
- If she W's (Dashes) in, she will most likely throw her chain right after she Q's
- Dodge side to side to avoid getting hit by her chain
- You can either satchel away instantly when she W's (Dashes) towards you, or if you get hit by chain, satchel away while you're rooted or before you get rooted
- If you want to trade with her when she W's (dashes) in, Q her right away
- She has crazy gap closers, so you aren't safe at any distance
- If she walks up to Q you, she will most likely W right after, you can anticipate this by throwing satchel as she throws Q to cancel her W (Dash)
- Once she uses her W and misses, you can walk up and be aggresive
"""

lissandra_matchup = f"""
- Look to be aggresive with your Q since she has low mobility and short range
- Take advantage of the range difference
- Don't stand behind minions because her Q will deal damage to use
- You can satchel away if she roots you with her W
- If she's escaping with her E, if you time it right you can cancel it using W (satchel) by knocking her up
"""

lucian_matchup = f"""
- Primarily look to just focus on farming in this lane, you will most likely not solo kill him
- Avoid taking trades in short distances, he will out damage you everytime
- Use your W (satchel) to escape if he dashes close to you
- Don't stand behind minions as he can Q you through the minions
"""
lux_matchup = f"""
- This matchup is pretty difficult since lux kind of out ranges you with her E
- You can bait her E by moving towards her and away rapidly
- Just safely farm, she will always out trade you
- There is a small window where you can throw all your abilities on lux if she ults you close range (she stands still)
- You can look to poke since she has poor mobility
- If you get snared by her from her Q, you can stachel away and avoid her whole combo
"""

malphite_matchup = f"""
- Poke with your Q and auto everytime he walks up
- Pretty much malphite's goal is to poke you down with Q then flash and ult you (all in combo) which is hard to react to
- Before level 6, you should be super aggresive and poke him down and chance you get
- Once he gets 6, you might have to respect his poke if he decides to build AP
- Maybe look to hover your flash to always anticipate his ult
"""

malzahar_matchup = f"""
- Look to be aggresive with your Q since he has extremely low mobility
- Take advantage of the range difference
- Stand away from minions that has his E on it, it can spread to you
- Be aware that he can flash Ult you at any moment
- To prevent his pushing power, throw Q on his W (Voidlings)
"""

naafiri_matchup = f"""
- Look to be aggresive with your Q and auto attacks when she goes to farm
- You can throw your Q off her wolves, exploding onto her dealing damage
- You can cancel her W (dash) using your W (Satchel)
- Dodge left to right when avoiding her Q (Projectiles)
- Should honestly never die since you can cancel her all in
"""

neeko_matchup = f"""
- Look to be aggresive with your Q since she has low mobility
- Take advantage of the range difference
- Make it a habit to count minions(3 melee, 3 caster) as she can disguise as a minion to surprise you and kill you
- Dodge side to side to avoid her E (root)
- If you get hit by her E, you can satchel away
- If you get hit by her Q, walk out of the radius to avoid damage
- If she ults you, you can still satchel away since it's a root
- If she misses her E (root), you can walk up and be aggresive
"""

orianna_matchup = f"""
- Look to be aggresive with your Q since she has relatively low mobility
- Take advantage of the range difference
- Poke at a safe distance, her abilities are extremely easy to land so she will beat you in close range
"""

qiyana_matchup = f"""
- Look to be aggresive in the early game (Before level 6) by poking her with Q and auto attacks
- Dodge left and right to avoid her Q (2 projectiles)
- She can dash through minions to ult you into a wall, stay at a relatively safe distance
- You can satchel away if she roots you
- If she misses her 2 projectile combo, you can walk up and be aggresive
"""

ryze_matchup = f"""
- Look to be aggresive with your Q because he has poor mobility
- Take advantage of the range difference
- Avoid close range trades, he out trades you since he thrives in short range
- You can satchel away if he roots you
- Don't stand too close to minions since he can deal damage to you if his E spreads to you and he Q's
"""

seraphine_matchup = f"""
- Look to be aggresive with your Q since she has poor mobility
- If she roots you, you can W (Satchel) away
"""

swain_matchup = f"""
- Look to be aggresive with your Q because he has poor mobility
- Take advantage of the range difference
- Avoid close range trades, he out trades you since he thrives in short range
- Don't stand behind minions since he can grab you through minions with his E
- If he roots you, you can satchel away
- If he ults, just satchel you and him away, wait for his ult to expire
"""

sylas_matchup = f"""
- Look to be aggresive with your Q and auto attacks when he goes to farm
- Make sure to dodge side to side to avoid his E (chain), lots of his damage comes from his E
- Satchel him away if he decides to dash into you
- If you time it correctly, you can cancel his W with your satchel
- Good Sylas players will dash to you, then W before throwing his chain
- If sylas uses his E and misses, you can play aggresive and walk up
"""

syndra_matchup = f"""
- Look to be aggresive with your Q because she has poor mobility
- Take advantage of the range difference
- Don't stand behind her Q (Balls) as she can stun you using her E
- Dodge side to side to avoid her stun from her Q + E
- You can bait her Q in lane by walking forward then quickly walking backward
- When she uses her E (stun), you should walk up
"""

taliyah_matchup = f"""
- Look to be aggresive with your Q since she has relatively low mobility
- Take advantage of the range difference
- If you are stuck in her E (minefield), you can't satchel away because it will stun you and deal damage
- If she throws her E (minefield), she will most likely use W (seismic shove), so make sure to be unpredictable with your movement by moving side to side or up and down
- She has strong pushing power with her Q, so you should look to actively hit the wave if needed
- If she misses her E and W combo, you can walk up and be aggresive
"""

talon_matchup = f"""
- Look to be aggresive with your Q and auto attacks if he goes up to farm
- Stay at a relatively close range to avoid poke from his W and an all in with his Q
- If you time it properly, you can cancel his Q (dash) with your W (Satchel)
- Once he hits level 6, you must respect him because his all in will kill you
"""

tristana_matchup = f"""
- Look to be aggresive with your Q since she has poor mobility
- Take advantage of the range difference
- Stay away from low minions since it will explode and deal small damage to you
- Save your W (satchel) when she W's (Rocket jumps) in
- If you have enough damage, you can soak her W (rocket jump), and all in her since she has no escape (only if you are healthy enough)
- Be careful of her jumping onto you from fog of war
- If you time it correctly, you can cancel her W (rocket jump) using your satchel
"""

twistedfate_matchup = f"""
- Look to be aggresive with your Q since he has low mobility
- Take advantage of the range difference
- Dodge left to right to avoid his Q (Projectile)
- If he has a gold (stun) card, run away if possible
- Once he hits level 6, you must communicate with your team that he can roam
- Must hit minion wave and clear fast if he decides to shove because he will ult into another lanes if you are still clearing minions
"""

veigar_matchup = f"""
- Look to be aggresive with your Q since he has poor mobility
- Take advantage of the range difference
- Don't get caught in his cage if you are trying to satchel away, if you satchel too late you will get stunned
- Move side to side to dodge his Q (Projectile)
- Be unpredictable with your movement to avoid his W
"""

velkoz_matchup = f"""
- Look to be aggresive with your Q since he has EXTREMELY poor mobility
- Move up and down to dodge his Q
- Move side to side to dodge his W
- Be unpredictable with movement to avoid his E
- If in range, you can cancel his Ult with your satchel
- You can look to throw your ult at him anytime he uses ult in the late game because he's stationary
"""

vex_matchup = f"""
- Look to be aggresive with your Q since she has poor mobility
- Take advantage of the range difference
- Dodge side to side to avoid her Q and R
- Be unpredictable with your movement to avoid her E
"""

viktor_matchup = f"""
- Look to be aggresive with your Q since he has poor mobility
- Take advantage of the range difference
- If stuck in his W, W (Satchel) away, don't do it too late or else you'll get stunned
- Dodge side to side to avoid his E
- Avoid close range trades since he thrives in close combat
"""

vladimir_matchup = f"""
- Look to be aggresive with your Q since he has poor mobility
- Take advantage of the range difference
- Poke at a safe range, avoid close range combat since he will most likely out trade you since he thrives in close range combat
- Hold your ult until he uses his W, he can easily dodge it using his W
- If you are low hp and he is chasing you, once you see him channeling his E, he will most likely flash on top of you and kill you
- Should buy anti-heal mid to late game, only buy oblivion orb and finish morellonomicon as the last item
"""

xerath_matchup = f"""
- Look to be aggresive with your Q since he has EXTREMELY poor mobility
- Dodge left to right to avoid his Q + E
- You can look to throw your Q when he channels his Q since it slows him down making him an easier target to hit
- Be unpredictable with your movement to dodge his W + R
- If in range, you can cancel his ult with your satchel
- You can look to throw your ult at him anytime he uses ult in the late game because he's stationary
"""

yasuo_matchup = f"""
- Look to be aggresive with your Q and auto attacks when he goes up to farm
- Be careful since he can dash through minions, he has extremely high mobility making him a hard target to hit
- Dodge side to side to avoid his knock up
- If you get caught by his knock up, look to satchel away right after he finishes ulting you
- W (Satchel) him away if he dashes onto you, if you time it right you can cancel it
- Must time your W (Satchel) properly since he can use his W (Windwall) to destroy it (be unpredictable with the timing)
- If you satcheling yourself away from him, make sure you throw it right on top of him so its hard for him to react with wind wall
- Be aware where his windwall is, don't waste and throw abilities into it
- If he dashes onto you close to turret and over extends, look to satchel him into the turret so he takes tower shots
"""

yone_matchup = f"""
- Look to be aggresive with your Q and auto attacks when he goes up to farm
- W (Satchel) him away if he dashes towards you
- Dodge side to side to avoid his knock up
- If he dashes onto you close to turret and over extends, look to satchel him into the turret so he takes tower shots
- If you get him low enough when he dashes onto you, you can look to ult him when he returns to his spot to kill him
"""

zed_matchup = f"""
- Look to be aggresive with your Q and auto attacks when he goes up to farm
- Move side to side to dodge his whole combo but mainly his Q (Shurikens)
- Once he uses his W (shadow), you can look to be more aggresive and walk up
- Enemy Zed's will look to poke you down in lane and all in you by W'ing (Shadowing) in and ulting you
- When Zed ults you, he will always appear behind you
- Look to buy Zhonya's 2nd or 3rd, you can avoid his after burst damage from his R or even cancel his R using Zhonya's
"""

zoe_matchup = f"""
- Look to be aggresive with your Q since she has poor mobility
- Take advantage of the range difference
- You can look to throw abilities at Zoe when she goes to pick up a bubble from a minion
- When Zoe throws her Q, she always walks in a straight line to deal damage to either you or a minion, you can look to throw a Q in the direction shes walking in
- Don't stand too close to minions as the Q splash can hit you
- To avoid her E (bubble), dodge side to side so you dont get slept
- If she ults in, she will likely look to bubble you in the middle of her ult so you need to be unpredictable moving side to side
- If you get hit by her bubble, you can look to W (Satchel) away in hopes of getting out of range of her Q
- If you flash, be careful since she can pick it up and use it on you
"""


def match_up_output(champion):

    var_name = f"{champion}_matchup"

    matchup_feedback = globals().get(var_name, "Matchup not found, try typing in all lowercase and no punctuation")
    embed = Embed(
        title=f"{champion.capitalize()} Match Up Key Points:",
        description=matchup_feedback,
        color=0x4CAF50
    )
    return embed


def match_up_list():
    list_matchups = textwrap.dedent(f"""
        - ahri
        - akali
        - akshan
        - anivia
        - annie
        - aurelionsol
        - azir
        - brand
        - cassiopeia
        - corki
        - diana
        - ekko
        - fizz
        - galio
        - hwei
        - irelia
        - kassadin
        - katarina
        - leblanc
        - lissandra
        - lucian
        - lux
        - malphite
        - malzahar
        - naafiri
        - neeko 
        - orianna
        - qiyana
        - ryze
        - seraphine
        - swain
        - sylas
        - syndra
        - taliyah
        - talon
        - tristana
        - twistedfate
        - veigar
        - velkoz
        - vex
        - viktor
        - vladimir
        - xerath
        - yasuo
        - yone
        - zed
        - zoe
        """)
    embed = Embed(
            title=f"**List of Available Champions for Tips as Ziggs:**",
            description=list_matchups,
            color=0xC8A2C8
            )
    return embed