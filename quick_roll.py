import os
from collections import defaultdict

import numpy as np


COLOR_WHITE_DEFAULT = '\033[0m'  # white (normal)
COLOR_RED = '\033[31m'  # red
COLOR_GREEN = '\033[32m'  # green
COLOR_ORANGE = '\033[33m'  # orange
COLOR_BLUE = '\033[34m'  # blue
COLOR_PURPLE = '\033[35m'  # purple


def roll(dice, critical, return_rolled_dice=False):
    rolled_dice = np.array(dice)
    if critical:
        rolled_dice = np.concatenate([dice, dice], axis=0)
    rolled = np.random.randint(1, rolled_dice)
    if return_rolled_dice:
        return rolled, rolled_dice
    else:
        return rolled


def hit_roll(hit_dc, advantage):
    roll_hit = max(roll([20], advantage))
    total_roll = roll_hit + hit_dc
    print(f'Hit Dice: [{roll_hit}] + {hit_dc} = {total_roll}')
    if critical := (roll_hit == 20):
        print(COLOR_RED+'Critical!'+COLOR_WHITE_DEFAULT)
        hit = 'y'
    else:
        while (hit := input('Hit? ')) not in ('y', 'n'):
            pass
    return hit, critical


def smite_dice():
    dice = [8, 8]
    while (undead := input('  Undead/Fiend? ').lower()) not in ('y', 'n'):
        pass
    while (smite_level := input('  Smite Level? ')) not in ('1', '2', '3'):
        pass
    smite_level = int(smite_level)
    dice += (smite_level-1)*[8]
    if undead == 'y':
        dice += [8]
    return {'Dice': np.array(dice),
            'Bonus': 0,
            'Type': 'Radiant'}


def print_damage_report(damage_report):
    print('\n')
    print('Damage Report:')
    damage_summary = defaultdict(lambda: 0)
    for type_, rolls in damage_report.items():
        print(f'  {type_}:')
        for roll_ in rolls:
            print(f'    {roll_[0]} + {roll_[1]}')
            damage_summary[type_] += sum(roll_[0]) + roll_[1]
    print('\n')
    print('Damage Summary')
    for type_, damage in damage_summary.items():
        print(f'  {type_:<10}: {damage}')


def roll_regis_greatsword(advantage, hunters_mark, divine_favor):
    great_weapon_fighting = True
    hit_dc = 8
    weapon_damage = {'Dice': [6, 6],
                     'Bonus': 5,
                     'Type': 'Slashing'}
    # extra_damage = [] # for Improved Smite
    # Preprocess
    damage_report = defaultdict(lambda: [])
    if hunters_mark:
        weapon_damage['Dice'].append(6)
    weapon_damage['Dice'] = np.array(weapon_damage['Dice'])

    hit, critical = hit_roll(hit_dc, advantage)
    if hit == 'y':
        # Damage Roll
        roll_damage, rolled = roll(weapon_damage['Dice'], critical,
                                   return_rolled_dice=True)
        # refactor
        if great_weapon_fighting and not critical:
            rerolls = roll_damage < 3
            roll_damage[rerolls] = roll(rolled[rerolls], False)
        damage_report[weapon_damage['Type']].append((
            roll_damage, weapon_damage['Bonus']))
        if divine_favor:
            damage_report['Radiant'].append((roll([4], critical), 0))
        while (smite := input('Smite? ').lower()) not in ('y', 'n'):
            pass
        if smite == 'y':
            smite_dice_ = smite_dice()
            damage_report[smite_dice_['Type']].append(
                (roll(smite_dice_['Dice'], critical), smite_dice_['Bonus']))
        print_damage_report(damage_report)


def roll_regis_longsword(advantage, hunters_mark, divine_favor):
    hit_dc = 8
    weapon_damage = {'Dice': [8],
                     'Bonus': 7,
                     'Type': 'Slashing'}
    # extra_damage = [] # for Improved Smite
    # Preprocess
    damage_report = defaultdict(lambda: [])
    if hunters_mark:
        weapon_damage['Dice'].append(6)
    weapon_damage['Dice'] = np.array(weapon_damage['Dice'])

    hit, critical = hit_roll(hit_dc, advantage)
    if hit == 'y':
        # Damage Roll
        roll_damage = roll(weapon_damage['Dice'], critical)
        damage_report[weapon_damage['Type']].append((
            roll_damage, weapon_damage['Bonus']))
        if divine_favor:
            damage_report['Radiant'].append((roll([4], critical), 0))
        while (smite := input('Smite? ').lower()) not in ('y', 'n'):
            pass
        if smite == 'y':
            smite_dice_ = smite_dice()
            damage_report[smite_dice_['Type']].append(
                (roll(smite_dice_['Dice'], critical), smite_dice_['Bonus']))
        print_damage_report(damage_report)


def roll_arastos_trampling(advantage):
    hit_dc = 6
    weapon_damage = {'Dice': [6, 6],
                     'Bonus': 4,
                     'Type': 'Bludgeoning'}
    # Preprocess
    damage_report = defaultdict(lambda: [])
    # Hit Roll
    hit, critical = hit_roll(hit_dc, advantage)
    if hit == 'y':
        # Damage Roll
        damage_report[weapon_damage['Type']].append((
            roll(weapon_damage['Dice'], critical), weapon_damage['Bonus']))
        while (trampling := input('Trampling (STR 14)? ').lower()) not in ('y', 'n'):
            pass
        if trampling == 'y':
            hit, critical = hit_roll(hit_dc, advantage)
            if hit == 'y':
                # Damage Roll
                damage_report[weapon_damage['Type']].append((
                    roll(weapon_damage['Dice'], critical), weapon_damage['Bonus']))
        print_damage_report(damage_report)


if __name__ == '__main__':
    os.system('cls')
    regis_advantage = True
    hunters_mark = True
    divine_favor = False
    arastos_advantage = False

    print('Arastos Attack')
    roll_arastos_trampling(advantage=arastos_advantage)

    # print('\n')
    # print('Regis Attack')
    # roll_regis_greatsword(advantage=regis_advantage,
    #                       hunters_mark=hunters_mark,
    #                       divine_favor=divine_favor)

    # print('\n')
    # print('Regis Attack 2')
    # roll_regis_greatsword(advantage=regis_advantage,
    #                       hunters_mark=hunters_mark,
    #                       divine_favor=divine_favor)

    print('\n')
    print('Regis Attack')
    roll_regis_longsword(advantage=regis_advantage,
                         hunters_mark=hunters_mark,
                         divine_favor=divine_favor)

    print('\n')
    print('Regis Attack 2')
    roll_regis_longsword(advantage=regis_advantage,
                         hunters_mark=hunters_mark,
                         divine_favor=divine_favor)
