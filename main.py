import json

class Character:
    def __init__(self, name, health, damage, xp, level, max_health):
        self.name = name
        self.health = health
        self.damage = damage
        self.xp = xp
        self.level = level
        self.max_health = max_health

    def attack(self, target):
        pass

    def take_damage(self, damage):
        if damage >= self.health:
            self.health = 0
        else:
            self.health -= damage

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def gain_xp(self, xp=0):
        max_health = 10
        max_damage = 5
        self.xp += xp
        while self.xp >= self.level * 100:
            self.level += 1
            self.damage += max_damage
            self.health += max_health
            self.max_health = self.max_health + max_health

    def heal(self):
        if self.health < self.max_health:
            self.health = self.health + 20
            if self.health > self.max_health:
                self.health = self.max_health
        else:
            print("character health is full")

    def to_dict(self):
        character_dict = {
            "class": self.__class__.__name__,
            "name": self.name,
            "health": self.health,
            "damage": self.damage,
            "xp": self.xp,
            "level": self.level,
            "max_health": self.max_health,
        }
        return character_dict

class Warrior(Character):
    def attack(self, target):
        target.take_damage(self.damage)
        print("Warrior attacks with sword")

warrior = Warrior("Warrior", 120, 25, 0, 1, 120)

class Mage(Character):
    def attack(self, target):
        target.take_damage(self.damage)
        print("Mage casts a spell!")

mage = Mage("Mage", 140, 30, 0, 1, 140)

class Archer(Character):
    def attack(self, target,):
        target.take_damage(self.damage)
        print("Archer shoots an arrow!")

archer = Archer("Archer", 160, 20, 0, 1, 160)


class Game:
    def __init__(self):
        self.characters = []
        self.battle_log = []

    def save_game(self):
        characters_data = []
        characters = self.characters

        for character in characters:
            characters_data.append(character.to_dict())

        with open("characters.json", "w") as file:
            json.dump(characters_data, file)

    def load_game(self):
        try:
            with open("characters.json", "r") as file:
                characters_data = json.load(file)

            self.characters.clear()

        except FileNotFoundError:
            print("file not found!")
            return

        except json.JSONDecodeError:
            print("Save file is corrupted!")
            return

        for character_data in characters_data:
            if character_data["class"] == "Warrior":
                character = Warrior(
                    character_data["name"],
                    character_data["health"],
                    character_data["damage"],
                    character_data["xp"],
                    character_data["level"],
                    character_data["max_health"]
                )
                self.characters.append(character)

            elif character_data["class"] == "Mage":
                character = Mage(
                    character_data["name"],
                    character_data["health"],
                    character_data["damage"],
                    character_data["xp"],
                    character_data["level"],
                    character_data["max_health"]
                )
                self.characters.append(character)

            elif character_data["class"] == "Archer":
                character = Archer(
                    character_data["name"],
                    character_data["health"],
                    character_data["damage"],
                    character_data["xp"],
                    character_data["level"],
                    character_data["max_health"]
                )
                self.characters.append(character)

    def show_battle_log(self):
        if not self.battle_log:
           print("No battle history yet!")
           return

        for battle_log in self.battle_log:
            print(battle_log)

    def show_characters(self):
        for character in self.characters:
            print(character.name, "-", character.health, "HP")

    def find_character(self, name):
        for character in self.characters:
            if character.name == name:
                return character
        return None

    def add_character(self,):
        charname = (input("enter character name: "))
        char_health = (int(input("enter character health: ")))
        char_damage = (int(input("enter character damage: ")))
        char_max_health = (int(input("enter character max_health: ")))
        char_xp = 0
        char_lvl = 1
        character = Character(charname, char_health, char_max_health, char_xp, char_lvl, char_damage)

        self.characters.append(character)

    def remove_character(self):
        name = input("Enter character name: ")

        for character in self.characters:
            if character.name == name:
                self.characters.remove(character)
                print("Removed character", character.name)
                return

        print("Character doesn't exist")

    def battle(self, ):
        attacker = (input("enter attacker name: "))
        defender = (input("enter defender name: "))

        attacker = self.find_character(attacker)
        defender = self.find_character(defender)

        if not attacker or not defender:
            print("Character doesn't exist")
            return

        if attacker == defender:
            print("Attacker and defender are the same, please choose different characters!")
            return

        current_attacker = attacker

        if not attacker.is_alive() or not defender.is_alive():
            print("character you picked is dead, try different characters!")
            return

        while defender.is_alive() and attacker.is_alive():
            if current_attacker == attacker:
                self.battle_log.append(f"{attacker.name} attacked {defender.name} and dealt {attacker.damage} damage!")
                print(attacker.name + " attacks " + defender.name + "!")
                defender.take_damage(attacker.damage)
                print(f"{defender.name} is now  {defender.health}!")

                current_attacker = defender

            else:
                self.battle_log.append(f"{defender.name} attacked {attacker.name} and dealt {defender.damage} damage!")
                print(defender.name + " attacks " + attacker.name + "!")
                attacker.take_damage(defender.damage)
                print(f"{attacker.name} is now  {attacker.health}")

                current_attacker = attacker

        if not defender.is_alive():
            attacker_level = attacker.level
            print(defender.name + " is dead")
            print(attacker.name + " wins!")
            old_xp = attacker.xp

            attacker.gain_xp(50)

            gained_xp = attacker.xp - old_xp
            print(f"{attacker.name} gained {gained_xp} XP and now has {attacker.xp} XP!")

            if attacker.level > attacker_level:
                print(f"{attacker.name} leveled up to {attacker.level}")

        elif not attacker.is_alive():
            defender_level = defender.level
            print(attacker.name + " is dead")
            print(defender.name + " wins!")
            old_xp = defender.xp

            defender.gain_xp(50)

            gained_xp = defender.xp - old_xp
            print(f"{defender.name} gained {gained_xp} XP and now has {defender.xp} XP!")

            if defender.level > defender_level:
                print(f"{defender.name} leveled up to {defender.level}")

        print("damage: " + str(attacker.damage))
        print(f"{defender.name} is now {defender.health}!")

    def heal_character(self,):
        character_name = (input("enter character name u want to heal : "))
        character_name = self.find_character(character_name)
        if character_name:
            character_name.heal()
        else:
            print("Character doesn't exist")

game = Game()

game.characters.append(warrior)
game.characters.append(mage)
game.characters.append(archer)


while True:
    print("======BATTLE GAME======")
    print("1.Show characters")
    print("2.Add character")
    print("3.Remove character")
    print("4.Battle")
    print("5.heal_character")
    print("6.battle history")
    print("7.load game")
    print("8.save game")
    print("9.Exit")

    try:
        choose = int(input("enter your choice: "))
    except ValueError:
        print("invalid input, please enter a number")
        continue

    if choose == 1:
        game.show_characters()
        print("characters showed!")
    elif choose == 2:
        game.add_character()
        print("Character added!")
    elif choose == 3:
        game.remove_character()
        print("Character removed!")
    elif choose == 4:
        game.battle()
        print("Characters battle ended!")
    elif choose == 5:
        game.heal_character()
        print("healing character is done!")
    elif choose == 6:
        game.show_battle_log()
        print("battle history showed!")
    elif choose == 7:
        game.load_game()
        print("Game loaded successfully!")
    elif choose == 8:
        game.save_game()
        print("Game saved successfully!")
    elif choose == 9:
        break


