from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 45, 1400, "black")

# White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

# Items
potion = Item("Potion", "potion", "Heals 100 HP", 100)
hipotion = Item("Hi-Potion", "potion", "Heals 300 HP", 300)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)

elixir = Item("Elixir", "elixir", "Fully replenishes HP/MP of one party member", 9999)
hielixir = Item("Hi-Elixir", "elixir", "Fully replenishes HP/MP of all party members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 Dmg", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]

player_items = [{"item": potion, "quantity": 15}, {"item":hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item":hielixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

player1 = Person("Valos", 3260, 130,60,34, player_spells, player_items)
player2 = Person("Nick ", 4160, 180,60,34, player_spells, player_items)
player3 = Person("Robot", 3090, 170,60,34, player_spells, player_items)

enemy = Person("Magus", 11200, 250, 350, 25, [], [])

players = [player1, player2, player3]
running = True

print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks!" + bcolors.ENDC)

while running:
    print("====================================================")
    print("Name                HP                                                   MP")

    for player in players:
        player.get_stats()

    enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose the action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_dmg()
            enemy.take_dmg(dmg)
            print("    "+player.name + " attacked for", dmg, "points of damage.")

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
                print(bcolors.OKBLUE + "\n" + player.name + " casts " + spell.name + " and heals for",str(magic_dmg),"HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_dmg(magic_dmg)
                print(bcolors.OKBLUE + player.name + " casts " + spell.name, "dealing", str(magic_dmg), "damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Chose The Item to be Used: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\nNone Left" + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + player.name + " uses", item.name + " and heals for", str(item.prop) + "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Hi-Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                        print(bcolors.OKGREEN + player.name + " uses",
                              item.name + " fully restores HP/MP of all party members." + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + player.name + " uses", item.name + " fully restores HP/MP."+bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_dmg(item.prop)
                print(bcolors.FAIL + player.name + " uses", item.name + " dealing", str(item.prop) + "dmg to Enemy" + bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemy.generate_dmg()
    players[target].take_dmg(enemy_dmg)
    print("\n" + enemy.name, "attacked " + players[target].name + " for", enemy_dmg, "points of damage. \n")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN+"You WIN!!"+bcolors.ENDC)
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You Lose!!" + bcolors.ENDC)
        running = False;
