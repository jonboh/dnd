from great_weapon_fighting import damage_roll_great_weapon_fighting
from great_weapon_fighting import damage_roll
from great_weapon_fighting import p_hit, damage_bonif


def rounds_onhp(hp, ac):
    phit, pcrit = p_hit(ac, attacker_dc, attacker_advantage)
    damage_dice = damage_roll(attacker_dice)
    damage_extra = damage_bonif(attacker_strenght, weapon_bonus)
    damage_attack = (phit * (damage_dice + damage_extra)
                     + pcrit * (2*damage_dice + damage_extra))

    damage = damage_attack
    # print(f'P(Enemy Hit):  {phit}')
    # print(f'Damage/attack: {damage_attack:.2f}')
    # print(f'Round: {0} - Damage: {damage:.2f}')
    rounds = hp / damage
    return rounds


def hasted_rounds(hp, ac):
    hasted_keepcon = p_notbreak(ac+2, attacker_dc)
    t = 0
    keep_rounds = rounds_onhp(hp, ac+2)
    nokeep_rounds = rounds_onhp(hp, ac)
    rounds = 0
    while t < keep_rounds:
        rounds += (hasted_keepcon * keep_rounds
                   + (1-hasted_keepcon)*nokeep_rounds)
        t += 1
    return rounds / keep_rounds


def p_notbreak(ac, enemy_hitdc):
    phit_enemy, pcrit_enemy = p_hit(ac, enemy_hitdc, False)
    phit_enemy += pcrit_enemy
    psave, pcrit = p_hit(10, 5, False)
    psave += pcrit
    pnotbreak = 1-phit_enemy * (1-psave)
    return pnotbreak


multiplier = 100
hp = 83 * multiplier
con_save = 5
hit_dc = 8
attacks_round = 2

enemy_ac = 16
attacker_dice = [12, 12, 12]
attacker_advantage = False
attacker_proficiency = 3
attacker_strenght = 3
weapon_bonus = 3
attacker_dc = attacker_strenght+weapon_bonus+attacker_proficiency

phit, pcrit = p_hit(enemy_ac, hit_dc, False)

great_ac = 18
great_bonus = 5
great_keepcon = p_notbreak(great_ac, attacker_dc)
great_avgdamage = (phit * damage_roll_great_weapon_fighting([6, 6])
                   + pcrit * damage_roll_great_weapon_fighting([6, 6, 6, 6])
                   + great_bonus)
great_rounds = rounds_onhp(hp, great_ac)
great_simple_damage = attacks_round * great_rounds * great_avgdamage / multiplier
# Hunters Mark
great_hunters_avgdamage = (phit * damage_roll_great_weapon_fighting([6])
                           + pcrit * damage_roll_great_weapon_fighting([6, 6]))
great_hunters_damage = 0
great_pkeepcon_rounds = 1
con_counter = 0
for t in range(int(great_rounds)):
    great_hunters_damage += attacks_round * great_avgdamage
    great_hunters_damage += (attacks_round * great_pkeepcon_rounds
                             * great_hunters_avgdamage)
    great_pkeepcon_rounds *= great_keepcon
    if con_counter == 10:
        con_counter = 0
        great_pkeepcon_rounds = 1
great_hunters_damage /= multiplier

# Hasted
great_hasted_rounds = hasted_rounds(hp, great_ac)
great_keepcon_hasted = p_notbreak(great_ac+2, attacker_dc)
great_hasted_damage = 0
great_pkeepcon_rounds = 1
con_counter = 0
for t in range(int(great_hasted_rounds)):
    great_hasted_damage += attacks_round * great_avgdamage
    great_hasted_damage += (great_pkeepcon_rounds
                            * attacks_round * great_avgdamage
                            - (1-great_keepcon_hasted)
                            * attacks_round * great_avgdamage)
    great_pkeepcon_rounds *= great_keepcon_hasted
    if con_counter == 10:
        con_counter = 0
        great_pkeepcon_rounds = 1
great_hasted_damage /= multiplier


long_ac = 18 + 2
long_bonus = 5 + 2
long_keepcon = p_notbreak(long_ac, attacker_dc)
long_avgdamage = (phit * damage_roll([8])
                  + pcrit * damage_roll([8, 8])
                  + long_bonus)
long_rounds = rounds_onhp(hp, long_ac)
long_simple_damage = attacks_round*long_rounds * long_avgdamage / multiplier
# Hunters Mark
long_hunters_avgdamage = (phit * damage_roll([6])
                          + pcrit * damage_roll([6, 6]))
long_hunters_damage = 0
long_pkeepcon_rounds = 1
con_counter = 0
for t in range(int(long_rounds)):
    long_hunters_damage += attacks_round * (long_avgdamage +
                                            long_pkeepcon_rounds *
                                            long_hunters_avgdamage)
    long_pkeepcon_rounds *= long_keepcon
    if con_counter == 10:
        con_counter = 0
        long_pkeepcon_rounds = 1
long_hunters_damage /= multiplier

# Hasted
long_hasted_rounds = hasted_rounds(hp, long_ac)
long_keepcon_hasted = p_notbreak(long_ac+2, attacker_dc)
long_hasted_damage = 0
long_pkeepcon_rounds = 1
con_counter = 0
for t in range(int(long_hasted_rounds)):
    long_hasted_damage += attacks_round * long_avgdamage
    long_hasted_damage += (long_pkeepcon_rounds
                           * attacks_round * long_avgdamage
                           - (1-long_keepcon_hasted)
                           * attacks_round * long_avgdamage)
    long_pkeepcon_rounds *= long_keepcon_hasted
    if con_counter == 10:
        con_counter = 0
        long_pkeepcon_rounds = 1
long_hasted_damage /= multiplier
