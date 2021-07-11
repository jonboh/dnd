import numpy as np
from itertools import product


def damage_roll_great_weapon_fighting(damage_dice):
    return sum([
        np.mean([result if result not in (1, 2) else (dice+1)/2
                 for result in range(1, dice+1)])
        for dice in damage_dice])


def damage_roll(damage_dice):
    return sum([(dice+1)/2 for dice in damage_dice])


def damage_bonif(strenght, weapon_bonus, weapon_master=False):
    damage = (strenght
              + weapon_bonus
              + (10 if weapon_master else 0))
    return damage


def p_hit(target_ac, hit_dc, advantage,
          charisma=0, sacred_weapon=False, blessed=False,
          weapon_master=False):
    d20_rolls = np.arange(1, 20+1, dtype=int)
    d20_advantage_rolls = np.array(list(map(lambda roll: max(roll),
                                            product(d20_rolls, d20_rolls))))
    criticals = (sum(d20_rolls == 20) if not advantage
                 else sum(d20_advantage_rolls == 20))
    noncrit_rolls = (d20_rolls[d20_rolls != 20] if not advantage
                     else d20_advantage_rolls[d20_advantage_rolls != 20])
    hit_roll = (noncrit_rolls
                + hit_dc
                + ((4+1)/2 if blessed else 0)
                + (charisma if sacred_weapon else 0)
                + (-5 if weapon_master else 0))
    prob_hit = (np.sum(target_ac <= hit_roll)
                / (len(hit_roll) + criticals))
    prob_crit = criticals / (len(hit_roll) + criticals)
    return prob_hit, prob_crit


if __name__ == '__main__':
    # Target
    target_ac = 11
    # Character
    strenght = +3
    charisma = +3
    proficiency = +3
    # State
    bonus_action_available = True
    sacred_weapon = False
    blessed = False
    advantage = True
    # Skills
    divine_smite = [8, 8]
    weapon_master = False  # not generally helpful
    hunter_mark = False
    # Weapon
    weapon_bonus = 1
    weapon_dice = [6, 6]  # Greatsword
    # weapon_dice = [12] # Greataxe

    hit_dc = proficiency + strenght + weapon_bonus

    prob_hit, prob_crit = p_hit(target_ac, hit_dc, advantage,
                                charisma, sacred_weapon, blessed,
                                weapon_master)
    damage_dice = (damage_roll_great_weapon_fighting(weapon_dice)
                   + damage_roll(divine_smite)
                   + (damage_roll([6]) if hunter_mark else 0))
    damage_extra = damage_bonif(strenght, weapon_bonus, weapon_master)
    damage_attack = (prob_hit * (damage_dice + damage_extra)
                     + prob_crit * (2*damage_dice + damage_extra))
    if weapon_master and bonus_action_available:
        damage_attack += prob_crit * damage_attack

    print(f'Target AC:        {target_ac}')
    print(f'HIT/DC:           {hit_dc}')
    print('Normal Strike')
    print(f'  P(hit)|P(crit): {prob_hit*100:.2f}%|{prob_crit*100:.2f}%')
    print(f'  Damage/attack:  {damage_attack:.2f}')
