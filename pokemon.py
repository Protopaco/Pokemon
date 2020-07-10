from os import path
import pickle
import random


class Pokemon():

    def __init__(self, name, type):
        self.name = name
        self.level = 1
        self.type = type
        self.max_health = self.level * 20
        self.current_health = self.max_health
        self.knocked_out = False
        self.attacking = False
        self.xp = 0
        self.trainer = 'None'

    def print_status(self):
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Poke-status:")
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Name: " + self.name)
        print("Type: " + self.type)
        print("Level: " + str(self.level))
        print("Max Health: " + str(self.max_health))
        print("Current Health: " + str(self.current_health))
        print("Knocked Out: " + str(self.knocked_out))
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        input("Press any key...")

    def single_line_stats(self):
        ko = ""
        if self.knocked_out:
            ko = 'KO'
        print("{n} - lvl {l} - {t} - {h} - {k}".format(n=self.name, l=self.level, t=self.type, h=self.current_health,
                                                       k=ko))

    def lose_health(self, damage):
        status = False
        self.current_health -= damage
        if self.current_health < 1:
            self.knocked_out = True
            print("{n} was knocked out!".format(n=self.name))
            status = True
            self.current_health = 0
        else:
            print("{n} now has {c} health!".format(n=self.name, c=self.current_health))
        return status

    def heal(self):
        self.current_health += self.max_health
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        self.knocked_out = False
        print("Healing Potion!")
        print("{n} now has {c} health!".format(n=self.name, c=self.current_health))

    def reset(self):
        self.current_health = self.max_health
        self.knocked_out = False

    def attack(self, other_pokemon):
        get_potion = ""
        # contains attack multipliers for each Pokemon type
        # to be used in .attack() method
        attack_multiplier = [['fire', 'water', .5], ['fire', 'fire', .5], ['fire', 'grass', 2], ['water', 'water', .5],
                             ['water', 'fire', 2], ['water', 'grass', .5], ['grass', 'water', 2], ['grass', 'fire', .5],
                             ['grass', 'grass', .5]]
        multipler = 1
        for i in attack_multiplier:
            if i[0] == self.type and i[1] == other_pokemon.type:
                multiplier = i[2]
                break
        damage = round(self.level * 10 * multiplier)
        self.battle_animation(player, other_pokemon, damage)
        # print("{n} has dealt {d} damage to {o}!".format(n=self.name, d=damage, o=other_pokemon.name))
        ko = other_pokemon.lose_health(damage)
        if ko:
            get_potion = self.gain_xp(other_pokemon.level * 10)
        return other_pokemon, get_potion

    def battle_animation(self, player, other_pokemon, damage):
        print("\n\n/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("{p} VS {o}".format(p=self.name, o=other_pokemon.name))
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("{s} - {t} - lvl {l} - {h} hp".format(s=self.name, t=self.type, l=self.level, h=self.current_health))
        print("attacking:")
        print("{s} - {t} - lvl {l} - {h} hp".format(s=other_pokemon.name, t=other_pokemon.type, l=other_pokemon.level,
                                                    h=other_pokemon.current_health))
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("{d} damage dealt!".format(d=damage))

    def gain_xp(self, xp_gain):
        self.xp += xp_gain
        print("{n} gained {x} xp".format(n=self.name, x=xp_gain))
        print("New xp is: {x}".format(x=self.xp))
        if self.xp > (self.level * 10):
            self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        self.max_health = self.level * 20
        print("Level up!")
        print("{n} is now level {l}".format(n=self.name, l=self.level))
        print("{m} is new max_health".format(m=self.max_health))
        # print("{t} gained {l} health potions!".format(t=self.trainer, l=self.level))
        """
        try:
            self.gain_potions(self.level)
        except:
            print("*ERROR* Pokemon not assigned to a trainer")
        """

    def reset(self):
        self.current_health = self.max_health
        self.knocked_out = False


class Trainer:
    def __init__(self, name, reserve_pokemon):
        self.name = name
        self.potions = 2
        # self.active_pokemon = "None"
        self.reserve_pokemon = reserve_pokemon
        self.opponents = self.create_opponents()
        self.available_pokemon = []

    def print_status(self):
        print('\n\n\n\n\n')
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Trainer-status:")
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Name: " + self.name)
        print("Health Potions: " + str(self.potions))
        # print("Active Pokemon: " +self.active_pokemon)
        print("Reserve Pokemon: ")
        for i in self.reserve_pokemon:
            ko = ""
            if i.knocked_out:
                ko = 'KO'
            print("{n} - lvl {l} - {t} - {h} - {k}".format(n=i.name, l=i.level, t=i.type, h=i.current_health, k=ko))
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        input("Press any key...")

    print('\n\n\n')

    def reset(self):
        for i in self.reserve_pokemon:
            i.reset()

    def gain_potions(self, potions):
        self.potions += potions
        print("{n} now has {p} health potions!".format(n=self.name, p=self.potions))

    def attack(self, other_pokemon):
        print("{a} is going to attack {o}!".format(a=self.active_pokemon.name, o=other_pokemon.name))
        x = input("Continue (y/n): ")
        x = x.lower()
        if x == 'y':
            self.active_pokemon.attack(other_pokemon)
            return True
        elif x == 'n':
            return False
        else:
            print("invalid entry!")
            return False

    def use_potion(self):
        y = 0
        x = ""
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Which Pokemon would you like to heal?")
        for i in self.reserve_pokemon:
            print("({y}) - {n}".format(y=y, n=i.name))
            y += 1
        while x == "":
            try:
                x = int(input("> "))
            except:
                print("Invalid Entry")
                x = ""

        if self.reserve_pokemon[x]:
            self.potions -= 1
            self.reserve_pokemon[x].heal()
            print("You now have {p} healing potions!".format(p=self.potions))

    def create_opponents(self):
        opponent_list = []
        # pulling list of pokemon from file
        pokemon_list = call_pokemon()
        # removing pokemon player is currently using
        for i in self.reserve_pokemon:
            pokemon_list.remove([i.name, i.type])
        # reading file that holds opponent's names & levels
        with open('ai.pok', 'r') as open_file:
            line = open_file.readline()
            while line:
                opponent_reserve = []
                x = 0
                # cleaning up info from file
                line = line.strip()
                opponent_info = line.split(',')
                while x < 3:
                    # choosing one pokemon from list to assign to opponent
                    y = random.randrange(0, len(pokemon_list))
                    chosen_pokemon = Pokemon(pokemon_list[y][0], pokemon_list[y][1])
                    chosen_pokemon.level = int(opponent_info[1])
                    chosen_pokemon.max_health = chosen_pokemon.level * 20
                    chosen_pokemon.current_health = chosen_pokemon.max_health
                    pokemon_list.remove(pokemon_list[y])
                    opponent_reserve.append(chosen_pokemon)
                    x += 1
                final_opponent = Opponent(opponent_info[0], opponent_reserve, opponent_info[1])
                opponent_list.append(final_opponent)
                line = open_file.readline()
        self.available_pokemon = pokemon_list
        return opponent_list


class Opponent(Trainer):
    def __init__(self, name, reserve_pokemon, level):
        self.name = name
        self.level = level
        self.potions = 2
        self.reserve_pokemon = reserve_pokemon
        self.opponents = ""
        self.available_pokemon = ""
        self.defeated = False
        self.losses = 0
        self.wins = 0


def begin_animation():
    x = 0
    print("    ", end="")
    while x < 64:
        print("POKEMON ", end="")
        x += 1
        print("pokemon ", end="")
        x += 1
        if x % 4 == 0:
            print('')
            y = x % 5
            while y < 10:
                print(" ", end="")
                y += 1
    print("\n\n")


def create_trainer():
    pokemon_list = call_pokemon()
    reserved_pokemon = []
    z = 0

    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    print("Create Your Trainer!")
    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    name = input("Enter your name: ")
    while z < 3:
        x = 0
        print("Please pick a Pokemon to enslave:")
        for i in pokemon_list:
            print("({x}) {n} - {t}".format(x=x, n=i[0], t=i[1]))
            x += 1

        try:
            y = int(input("> "))
            print("You chose {n}!".format(n=pokemon_list[y][0]))
            chosen_pokemon = Pokemon(pokemon_list[y][0], pokemon_list[y][1])
            pokemon_list.remove(pokemon_list[y])
            reserved_pokemon.append(chosen_pokemon)
            z += 1
        except:
            print("Invalid entry!")

    player = Trainer(name, reserved_pokemon)
    player.print_status()
    return player


def call_pokemon():
    """
    pulls list of Pokemon names and types from file "pokemon.pokemon"
    :return: pokemon_list[]
    """
    pokemon_list = []
    with open('pokemon.pokemon', 'r') as open_file:
        line = open_file.readline()
        while (line):
            line = line.strip()
            pokemon_list.append(line.split(','))
            line = open_file.readline()
    pokemon_list.sort()
    return pokemon_list


def save_menu(player):
    x = ''
    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    print("Save Game")
    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    while x != 'x':
        print("(n) - New Save")
        print("(o) - Overwrite Save")
        print("(x) - Exit")
        x = input("> ")
        if x == 'n':
            new_save(player)
        elif x == 'o':
            overwrite_save(player)
        else:
            print("Invalid Entry!")


def new_save(player):
    print("Enter Save File Name:")
    file_name = input("> ")
    found = False
    with open('save_dir.pok', 'r') as open_dir:
        line = open_dir.readline()
        line = line.strip()
        while line and found == False:
            if line == file_name:
                found = True
                print("File already exists!")
            else:
                line = open_dir.readline()

    if found == False:
        with open('save_dir.pok', 'a') as open_dir:
            open_dir.write(file_name + '\n')
        open_dir.close()
        file_name += ".pok"

        dbfile = open(file_name, 'ab')
        pickle.dump(player, dbfile)
        dbfile.close()
        print("Save Successful!")


def overwrite_save(player):
    save_file = pull_save_file()
    dbfile = open(save_file, 'wb')
    pickle.dump(player, dbfile)
    dbfile.close()
    print("Save Successful!")


def pull_save_file():
    print("Current Save Files:")
    file_names = []
    save_file = ""
    with open('save_dir.pok', 'r') as save_dir:
        line = save_dir.readline()
        if line != "":
            x = 0
            while line:
                print("({x}) {l}".format(x=x, l=line))
                line = line.strip()
                file_names.append(line)
                x += 1
                line = save_dir.readline()
            y = int(input("> "))
            save_file = file_names[y] + ".pok"
        else:
            print("No Save Files Found!\n")
    save_dir.close()

    return save_file


def load_game():
    player = ""
    save_file = pull_save_file()
    if save_file != "":
        dbfile = open(save_file, 'rb')
        player = pickle.load(dbfile)
        dbfile.close()

    return player


def play_computer():
    pass


def first_menu():
    x = ""
    while x != "x":
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Welcome to Pokemon!")
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("(c) - Create Trainer")
        print("(l) - Load Game")
        print("(x) - Exit")
        x = input("> ")
        x = x.lower()
        if x == "c":
            player = create_trainer()
            return player
        elif x == "l":
            player = load_game()
            if player != "":
                return player
        elif x != "x":
            print("Invalid entry!")


def battle_choose(player):
    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    print("Battlemode!")
    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    opponent = call_opponent(player)
    player = battle_menu(player, opponent)

    return player


def call_opponent(player):
    avg_poke = (player.reserve_pokemon[1].level + player.reserve_pokemon[2].level + player.reserve_pokemon[
        0].level) // 3
    print("Choose Your Opponent!")
    print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
    x = 0
    for i in player.opponents:
        if int(i.level) <= avg_poke or i.defeated:
            print("({x}) - {n} - {w} wins - {l} losses".format(x=x, n=i.name, w=i.wins, l=i.losses))
            x += 1
    y = int(input("> "))
    return player.opponents[y]


def battle_menu(player, opponent):
    x = ''
    while x != 'x':
        print("\n\n/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("{p} VS {o}".format(p=player.name, o=opponent.name))
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("(o) - View Opponent's Stats")
        print("(y) - View Your Stats")
        print("(s) - Start the Battle")
        print("(x) - Run Away!")
        x = input("> ")
        if x == 'o':
            opponent.print_status()
        elif x == 'y':
            player.print_status()
        elif x == 's':
            player = battle_mode(player, opponent)
    return player


def battle_mode(player, opponent):
    is_end = False

    while is_end == False:
        player = battle_options(player, opponent)
        status = continue_battle(player, opponent)
        if status == "":
            input("Press any key...")
            player = computer_choose(player, opponent)
            input("Press any key...")
            opponent.print_status()
            player.print_status()
            status = continue_battle(player, opponent)
        if status != "":
            print("\n\n\n\n\n/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
            print("{n} is the WINNER!".format(n=status.name))
            print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")

            is_end = True
    player.reset()
    opponent.reset()
    return player


def computer_choose(player, opponent):
    attack_multiplier = [['fire', 'water', .5], ['fire', 'fire', .5], ['fire', 'grass', 2], ['water', 'water', .5],
                         ['water', 'fire', 2], ['water', 'grass', .5], ['grass', 'water', 2], ['grass', 'fire', .5],
                         ['grass', 'grass', .5]]
    score = 0
    attacker = []
    victim = []
    multiplier = 1
    for i in opponent.reserve_pokemon:
        i.attacking = False
        if i.knocked_out != True or opponent.potions > 0:
            for j in player.reserve_pokemon:
                if j.knocked_out != True:
                    for k in attack_multiplier:
                        if k[0] == i.type and k[1] == j.type:
                            multiplier = k[2]
                            if j.attacking:
                                multiplier = multiplier * 2
                            temp_score = i.level * multiplier * 10
                            if j.current_health < temp_score:
                                temp_score += 25
                            if i.knocked_out == True:
                                temp_score -= 25
                            if temp_score > score:
                                score = temp_score
                                attacker = i
                                victim = j
    x = opponent.reserve_pokemon.index(attacker)
    y = player.reserve_pokemon.index(victim)
    if opponent.reserve_pokemon[x].knocked_out and opponent.potions > 0:
        opponent.reserve_pokemon[x].heal()
        opponent.potions -= 1
        print("\n\n\n\n\n/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("{n} has been healed!".format(n=opponent.reserve_pokemon[x].name))
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        opponent.reserve_pokemon[x].print_status()
    player.reserve_pokemon[y], get_potion = opponent.reserve_pokemon[x].attack(player.reserve_pokemon[y])
    if get_potion:
        opponent.gain_potions(1)
    return player


def continue_battle(player, opponent):
    is_end = False
    cnt = 0
    for i in player.reserve_pokemon:
        if i.knocked_out == True:
            cnt += 1
        if cnt == 3:
            opponent.wins += 1
            return opponent
    cnt = 0
    for j in opponent.reserve_pokemon:
        if j.knocked_out == True:
            cnt += 1
        if cnt == 3:
            opponent.defeated = True
            opponent.losses += 1
            return player
    return ""


def battle_options(player, opponent):
    x = ""
    while x == "":
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Battle Options!")
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("(p) - Use Potion")
        print("(a) - Attack")
        # print("(x) - Run Away")
        x = input("> ")
        x = x.lower()
        if x == "p":
            player.use_potion()
            x = ""
        elif x == "a":
            player = choose_attacking(player)
            victim_pokemon = choose_victim(player, opponent)
            for i in player.reserve_pokemon:
                if i.attacking == True:
                    victim_pokemon, get_potion = i.attack(victim_pokemon)
                    if get_potion:
                        player.gain_potions(1)
        else:
            print("Invalid Entry!!")
            x = ""

    return player


def choose_attacking(player):
    con = False
    while con == False:
        x = 0
        print("\n\nChoose your attacking Pokemon!")
        print("Be Careful! \nYour attacking Pokemon is more susceptible to damage!")
        for i in player.reserve_pokemon:
            ko = ""
            i.attacking = False
            if i.knocked_out:
                ko = 'KO'
            print(
                "({x}) - {n} - lvl {l} - {t} - {h} - {k}".format(x=x, n=i.name, l=i.level, t=i.type, h=i.current_health,
                                                                 k=ko))
            x += 1
        try:
            y = int(input("> "))
            if player.reserve_pokemon[y].knocked_out:
                print("Pokemon is knocked out!")
                print("You must pick another Pokemon!")
            else:
                player.reserve_pokemon[y].attacking = True
                print("\n")
                player.reserve_pokemon[y].print_status()
                con = True
        except:
            print("Invalid entry!")
    return player


def choose_victim(player, opponent):
    x = 0
    print("\n\nWho shall you attack?")
    y = ""
    for i in opponent.reserve_pokemon:
        ko = ""
        if i.knocked_out:
            ko = 'KO'
        print("({x}) - {n} - lvl {l} - {t} - {h} - {k}".format(x=x, n=i.name, l=i.level, t=i.type, h=i.current_health,
                                                               k=ko))
        x += 1
    while y == "":
        try:
            y = int(input("> "))
            if opponent.reserve_pokemon[y].knocked_out:
                print("Pokemon is knocked out!")
                print("You must pick another Pokemon!")
                y = ""
        except:
            print("invalid entry!")

    return opponent.reserve_pokemon[y]


def new_trainer(player):
    print("By starting a new trainer you will lose any unsaved data.")
    print("Are you sure you want to continue? (y/n)")
    x = input("> ")
    if x == 'y':
        player = create_trainer()

    return player


def main_menu(player):
    x = ""
    while x != "x":
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("Main Menu")
        print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        print("(n) - New Trainer")
        print("(t) - Trainer Status")
        print("(b) - Battle")
        print("(s) - Save Game")
        print("(l) - Load Game")
        print("(x) - Exit")
        x = input("> ")
        x = x.lower()
        if x == "n":
            new_trainer(player)
        elif x == "t":
            player.print_status()
        elif x == "b":
            player = battle_choose(player)
        elif x == "s":
            save_menu(player)
        elif x == 'l':
            player = load_game()
        elif x != 'x':
            print("Invalid entry!")


def check_saves():
    if path.exists('save_dir.pok') == False:
        open('save_dir.pok', 'w+')


if __name__ == "__main__":
    check_saves()
    begin_animation()
    player = first_menu()
    main_menu(player)
