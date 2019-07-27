from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item


# Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 300)

elixir = Item("Elixir", "elixir", "Fully replenishes HP/MP of one party member", 9999)
hielixir = Item("Hi-Elixir", "elixir", "Fully replenishes HP/MP of all party members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 Dmg", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [potion, hipotion, superpotion, elixir, hielixir, grenade]
player = Person(460, 65,60,34, player_spells, player_items)
enemy = Person(1200, 65, 45, 25, [], [])

running = True

print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks!" + bcolors.ENDC)

while running:
    print("====================")
    player.choose_action()
    choice = input("Choose the action: ")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_dmg()
        enemy.take_dmg(dmg)
        print("You attacked for", dmg, "points of damage.")

    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose the Spell to Use: ")) - 1

        if magic_choice == -1:
            continue

        '''magic_dmg = player.generate_spell_dmg(magic_choice)
        spell = player.get_spell_name(magic_choice)
        cost = player.get_spell_mp_cost(magic_choice)'''

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_dmg()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP to cast The Spell!\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + "heals for",str(magic_dmg),"HP." + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_dmg(magic_dmg)
            print(bcolors.OKBLUE + "Player cast", spell.name, "dealing", str(magic_dmg), "damage" + bcolors.ENDC)

    elif index == 2:
        player.choose_item()
        item_choice = int(input("Chose The Item to be Used: ")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]
        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n", item.name + "heals for", item.prop + "HP" + bcolors.ENDC)


    enemy_choice = 1
    enemy_dmg = enemy.generate_dmg()
    player.take_dmg(enemy_dmg)
    print("Enemy attacked for", enemy_dmg, "points of damage.")

    print("----------------------------------------------")
    print("Enemy Hp:",bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_maxhp()) + bcolors.ENDC + "\n")
    print("Player's Hp:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_maxhp()) + bcolors.ENDC)
    print("Player's Mp:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_maxmp()) + bcolors.ENDC + "\n")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN+"You WIN!!"+bcolors.ENDC)
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You Lose!!" + bcolors.ENDC)
        running = False;
