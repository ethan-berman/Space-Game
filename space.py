import random
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class ship(object):
    def __init__(self, captain):
        self.captain = captain
        self.engines = random.randint(2,10)
        self.fuel = random.randint(10,50)
        self.shields = random.randint(0,20)
        self.weapons = random.randint(0,15)
        self.funds = 10
        self.counter = 0
        self.health = 100
        self.score = 0
class enemy(object):
    def __init__(self, level):
        self.attack = level*random.randint(2,5)
        self.shields = (level*random.randint(2,4))-(level+random.randint(2,4))
        self.health = 30+(level*random.randint(2,4))
def time_effect(vessel):
    vessel.counter += 1
    #call this function every time you advance the campaign and it will wear away at the vitals
    vessel.fuel -= 2
    if(vessel.counter % 2 == 0):
        vessel.engines -= 1
    vessel.shields += 1 
print("Welcome to space! You are the new captain of the U.S.S Owens!")
running = True
name = input("What is your name, Captain? ")
owens = ship(name)
def battle(vessel, difficulty):
    opponent = enemy(difficulty)
    print("A Level " + str(difficulty) + " Enemy approaches!  Make your decision wisely!")
    choice = input("(1) Fight (2) Flee (3) Cut a Deal")
    if choice == '1':
        if(vessel.weapons > opponent.shields and opponent.attack > vessel.shields):
            if vessel.weapons > opponent.attack:
                #vessel wins
                print("You barely survived!  Your shields took a lot of damage, but you gained some loot from the enemy.")
                owens.score += 5 * difficulty
                vessel.shields -= 20
                vessel.funds += random.randint(15,30)
            else:
                #opponent wins
                print("You lost the fight! the enemy had more powerful weapons!")
                running = False
                vessel.health = 0
                return("death")
        elif(vessel.weapons > opponent.shields and opponent.attack < vessel.shields):
            #win condition
            print("Congratulations! You destroyed the enemy ship and took their loot!")
            owens.score += 5 * difficulty
            vessel.funds += random.randint(30,50)
        elif(vessel.weapons < opponent.shields and opponent.attack > vessel.shields):
            print("The enemy destroyed you.  You didn't stand a chance.")
            vessel.health = 0
            return("death")
        elif(vessel.weapons < opponent.shields and opponent.attack < vessel.shields):
            #both weapons are too weak, the one with stronger weapons wins
            if(vessel.weapons > opponent.attack):
                print("Congratulations! You defeated your enemy and gained some funds")
                vessel.funds += random.randint(20,30)
            else:
                print("Your opponent destroyed your ship.  Nice try Captain " + vessel.captain)
                running = False
                vessel.health = 0
                return("death")
        print('fight')
    elif choice == '2':
        if vessel.engines > random.randint(0,6) and vessel.fuel > 5:
            print("Congratulations, you just barely escaped!")
            owens.score += 5 * difficulty
            time_effect(vessel)
        else:
            print("You failed to escape!")
            running = False
            vessel.health = 0
            return("death")
        #flee
    elif choice == '3':
        if vessel.funds > random.randint(0,vessel.funds):
            loss = random.randint(0,vessel.funds)
            print("the enemy accepts your deal of " + str(loss) + " space bucks")
            owens.score += 5 * difficulty
            vessel.funds -= loss
        else:
            print("While you tried to cut a deal, the enemy took advantage of the opportunity to destroy your ship!")
            running = False
            vessel.health = 0
            return("death")
        #cut a deal
    
    return("live")

def choose_action(vessel, act):
    if act < 5:
        battle(owens, 1)
        #case for a weak enemy
    elif act > 5 and act < 10:
        battle(owens, 2)
        #case for a medium enemy
    elif act > 10 and act < 15:
        battle(owens, 3)
        #case for a trade opportunity
    elif act > 15 and act < 18:
        #case for a rare discovery of supplies
        print("You discovered a bunch of supplies!")
        vessel.weapons += 20
        vessel.engines += 5
        vessel.fuel += 200

def shop(vessel):
    print("Welcome, to the shop, " + vessel.captain + "!  You can upgrade your ship here.")
    possible_fuel = 100-vessel.fuel
    offer = input("(1) Upgrade Engines: $30 (2) Fill Tank: " + str(possible_fuel * 4) + " (3)Repair Shields: $20 (4) Upgrade weapons $50")
    if offer == "1" and vessel.funds >= 30:
        vessel.engines += 5
        vessel.funds -= 30
    elif offer == "2" and vessel.funds >= possible_fuel*4:
        vessel.fuel = 100
        vessel.funds -= possible_fuel*4
    elif offer == "2" and vessel.funds <= possible_fuel*4:
        gallons = int(vessel.funds/4)
        vessel.fuel += gallons
        vessel.funds -= gallons*4
    elif offer == "3" and vessel.funds >= 20:
        vessel.shields += 10
        vessel.funds -= 20
    elif offer == "4" and vessel.funds >= 50:
        vessel.weapons += 10
        vessel.funds -= 50
def advance():
    print("advancing campaign")
    time_effect(owens)
    action = random.randint(0,18)
    choose_action(owens, action)
#game loop
if running is True:
    while True:
        command = input("Would you like to: (1) Check your Ship's Vitals or (2) Advance the campaign?")
        if command == "1":
            print("engines: " + str(owens.engines) + ", fuel: " + str(owens.fuel) + ", shields: " + str(owens.shields) + ", weapons: " + str(owens.weapons) +", space-bucks: " + str(owens.funds))
        elif command == "2":
            advance()
        elif command == "3":
            #shop(owens)
            break
        if owens.health <= 0:
            print("dead")
            break
        if owens.engines <= 0:
            print("Your engines failed!")
            break
        if owens.shields < 0:
            owens.shields = 0
        if owens.fuel < 0:
            owens.fuel = 0
        if owens.weapons < 0:
            owens.weapons = 0
        

file = open('scores.txt', 'a')
file.write("\n" + str(owens.score))
file.close()
file = open('scores.txt', 'r')
scores = file.read()
int_scores = scores.split("\n")
hist = []
for item in int_scores:
    hist.append(int(item))
plt.hist(hist)
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
z_score = (owens.score - np.mean(hist))/np.std(hist)
p = stats.percentileofscore(hist, owens.score)
print("You acheived a z-score of: " + str(z_score) + "!  Placing you in the " + str(p) + " percentile!  With a score of: " + str(owens.score))
plt.show()
print("Game Over! Thanks for playing!")
