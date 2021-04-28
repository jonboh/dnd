from great_weapon_fighting import damage_roll, damage_bonif, p_hit


def p_pounce(dc_save, save_points, advantage=False):
    p_save, p_savecrit = p_hit(dc_save-save_points, 0, advantage)
    p_save += p_savecrit
    return 1 - p_save


def damage_pounce(phit, pcrit, ppounce, attack1, attack2, bonif):
    return (phit * (damage_roll(attack1) + bonif)
            + pcrit * (2*damage_roll(attack1) + bonif)
            + ppounce * (phit * (damage_roll(attack2) + bonif) +
                         pcrit * (2*damage_roll(attack2) + bonif)))


target_ac = 14
target_strenght_save = 0

# Azer
azer_strength = 3
warhammer = [8, 6]
hit_dc = 5
phit, pcrit = p_hit(target_ac, hit_dc, advantage=False)

damage_warhammer = (phit * (damage_roll(warhammer)
                            + damage_bonif(azer_strength))
                    + pcrit * (2*damage_roll(warhammer)
                               + damage_bonif(azer_strength)))
print('Azer')
print(f'  P(hit)|P(crit):            {phit*100:.1f}%|{pcrit*100:.1f}%')
print(f'  Damage/attack:             {damage_warhammer:.2f}')
print(f'  [Damage when attacked:     {damage_roll([10])}]')
print()
# Saber-Tooth Tiger
saber_strenght = 5
bite = [10]
claw = [6, 6]
hit_dc = 6

phit, pcrit = p_hit(target_ac, hit_dc, advantage=False)

# Pouncing
ppounce = p_pounce(14, target_strenght_save, advantage=False)
damage_saber = damage_pounce(
    phit, pcrit, ppounce, claw, bite, damage_bonif(saber_strenght))

print('Saber-Tooth Tiger')
print(
    f'  P(hit)|P(crit)|P(pounce):  {phit*100:.1f}%|{pcrit*100:.1f}%|{ppounce*100:.1f}%')
print(f'  Damage/attack:             {damage_saber:.2f}')
print()

# 2 Lions
hit_dc = 5
# Pack Tactics
lion_strenght = 3
bite = [8]
claw = [6]
# Just Lion
phit, pcrit = p_hit(target_ac, hit_dc, advantage=False)
ppounce = p_pounce(13, target_strenght_save, advantage=False)
damage_lion = damage_pounce(phit, pcrit, ppounce, claw, bite,
                            damage_bonif(lion_strenght))
print('Lion (Normal)')
print(
    f'  P(hit)|P(crit)|P(pounce):  {phit*100:.1f}%|{pcrit*100:.1f}%|{ppounce*100:.1f}%')
print(f'  Damage/attack:             {damage_lion:.2f}')

# Pack Tactics
phit, pcrit = p_hit(target_ac, hit_dc, advantage=True)
damage_lion = damage_pounce(phit, pcrit, ppounce, claw, bite,
                            damage_bonif(lion_strenght))
print('Lion (Pack Tactics)')
print(
    f'  P(hit)|P(crit)|P(pounce):  {phit*100:.1f}%|{pcrit*100:.1f}%|{ppounce*100:.1f}%')
print(f'  Damage/attack:             {damage_lion:.2f}')

# Pair Lions
phit, pcrit = p_hit(target_ac, hit_dc, advantage=True)
damage_lion_trigger = (
    phit * (damage_roll(bite) + damage_bonif(lion_strenght)) + pcrit *
    (2 * damage_roll(bite) + damage_bonif(lion_strenght)))
damage_lion_pounce = damage_pounce(phit, pcrit, ppounce, claw, bite,
                                   damage_bonif(lion_strenght))
damage_lion = damage_lion_trigger + damage_lion_pounce
print('2 Lions - One Trigger, One Pounce')
print(f'  Damage/attack:             {damage_lion:.2f}')

print('2 Lions - Two Pounce')
print(f'  Damage/attack:             {damage_lion_pounce*2:.2f}')
