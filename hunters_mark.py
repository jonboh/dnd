from great_weapon_fighting import p_hit, damage_roll, damage_bonif

# Target
rounds = 4
target_ac = 15
# Character
strenght = +3
proficiency = +3
attacked_round = 3
# State
advantage = False

divine_smite = [8, 8]

armor_ac = 18
enemy_hitdc = 6

phit_enemy, pcrit_enemy = p_hit(armor_ac, enemy_hitdc, False)
phit_enemy += pcrit_enemy
psave, pcrit = p_hit(10, 5, False)
psave += pcrit
pnotbreak = 1-phit_enemy * (1-psave)

hit_dc = proficiency + strenght

prob_hit, prob_crit = p_hit(target_ac, hit_dc, advantage)
damage_dice = damage_roll([6])
damage_extra = damage_bonif(0)
damage_attack = (prob_hit * (damage_dice + damage_extra)
                 + prob_crit * (2*damage_dice + damage_extra))

# two attacks
damage_hunter = 2*damage_attack  # 2 attacks
print(f'P(Enemy Hit): {phit_enemy} - P(Keep Con): {psave}', end='')
print(' - P(Enemy Hit AND Keep Con): {pnotbreak}')
print(f'Round: {0} - Damage: {damage_hunter:.2f}')
for i in range(1, rounds):
    damage_hunter += pnotbreak**(i*attacked_round) * 2 * damage_attack
    print(f'Round: {i} - Damage: {pnotbreak**i * 2*damage_attack:.2f}', end='')
    print(f'|{damage_hunter:.2f}')

print(f'Hunter Total Damage: {damage_hunter:.2f}')

# 1st Level Divine Smite
prob_hit, prob_crit = p_hit(target_ac, hit_dc, advantage)
damage_dice = damage_roll(divine_smite)
damage_smite = damage_dice + prob_crit * 2*damage_dice
print(f'Divine Smite Damage: {damage_smite:.2f}')

# Here we compare the damage output per spellslot.
# Spent in hunter's mark or divine smite
