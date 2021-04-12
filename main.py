#modules needed to shuffle deck
import random
#importing OS module to clear terminal
import os
#to enable the ability to sleep/pause the program for game flow
from time import sleep

#global variables to construct Deck
card_values = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
               "Jack":10, "Queen":10, "King":10, "Ace":11,}
suits = ("Spades", "Clubs", "Hearts", "Diamonds")

#function to clear the terminal
def clear():
    os.system('cls')


#Card class to create one Card
class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __str__(self):
        return f'{self.rank} of {self.suit}'

#Deck class to create a deck of 52 cards
class Deck(Card):
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank,value in card_values.items():
                self.deck.append(Card(rank, suit, value))

    #shuffle deck at random
    def shuffle(self):
        return random.shuffle(self.deck)

    #drawing a card from the top of the deck
    def draw(self):
        return self.deck.pop(0)

#Player class that will keep count of player's hand,bet, money, etc
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.money = 500
        self.bet = 0
        self.winnings = 0

    #player asks for another card during blackjack
    def hit(self, deck):
        card = deck.draw()
        self.hand.append(card)

    #asking the player to make their bet
    def player_bet(self):
        while True:
            try:
                print(f"Cash Available: {self.money}")
                bet_input = int(input("Please place your bet (2 - 500): "))
            except:
                print("Please input only a number within the limit range 2 - 500. ")
                print("\n")
                continue
            else:
                if bet_input > self.money:
                    print("Not enough money to place bet.")
                    continue
                elif bet_input < 2 or bet_input > 500:
                    print("Please input only a number within the limit range 2 - 500. ")
                    continue
                else:
                    self.bet = bet_input
                    self.money -= self.bet
                    return


    #asking the player if they'd like to hit or stand
    def decision(self):
        while True:
            decision = input("\n\nWould you like to Hit or Stand? ")

            if decision[0].capitalize() == "H":
                return "Hit"
            elif decision[0].capitalize() == "S":
                return "Stand"
            else:
                print("Please use only Hit or Stand.")
                continue


#function to calculate the value of the passed in player's hand
def calculate_hand_value(player_name, *args):
    hand_value = 0

    #account for aces being 1 or 11
    for card in args:
        for c in card:
            if c.rank == 'Ace':
                #if the Dealer has an ace, set value to 11
                if player_name == "Dealer":
                    ace_value = 11
                    hand_value += ace_value
                    continue
                else:
                    #ask the player each time what theyd like for the ace value to be
                    while True:
                        try:
                            ace_value = int(input("Would you like the Ace to count as 1 or 11?"))
                        except:
                            print("Please input only 1 or 11.")
                            continue
                        else:
                            if ace_value == 11:
                                hand_value += ace_value
                            elif ace_value == 1:
                                hand_value += ace_value
                            break
            else:
                hand_value += c.value

    return hand_value


#player wins round
def player_win(player_1, dealer):
    print(f"{player_1.name} wins round!")

    #allocating bets to player_1 money
    player_1.money += player_1.bet
    player_1.money += dealer.bet

    #allocating bets to player_1 winnings
    player_1.winnings += player_1.bet
    player_1.winnings += dealer.bet

    print(f"{player_1.name}'s winnings this round: {player_1.bet + dealer.bet} \n\n")

    #setting each player's bet back to 0
    player_1.bet = 0
    dealer.bet = 0
    sleep(1)



#dealer wins round
def dealer_win(player_1, dealer):
    print(f"{dealer.name} wins round!")

    #allocating bets to dealer money
    dealer.money += player_1.bet
    dealer.money += dealer.bet

    #removing bet lost from winnings
    #negative winnings = money lost
    player_1.winnings -= player_1.bet

    #setting each player's bet back to 0
    player_1.bet = 0
    dealer.bet = 0
    sleep(1)



#function to ask player if they'd like to play another round of blackjack
def continue_game():
     while True:
            try:
                result = input("Another Round? Yes/No: ")
            except:
                print("Please utilize Yes or No only.")
                continue
            else:
                 #if they want another round, clear the player and dealer's hand
                if result[0].capitalize() == "Y":
                    player_1.hand = []
                    dealer.hand = []
                    return True
                elif result[0].capitalize() == "N":
                    return False
                else:
                    print("Please utilize Yes or No only.")
                    continue


'''
*****************************
Start of Blackjack Game Logic
*****************************
'''
#begin the game
print("Welcome to Blackjack!")

#asking for Player's Name and creating Player 1
name = input("Please input your Player's name: ")
player_1 = Player(name.capitalize())

#creating the Dealer
dealer = Player("Dealer")

#allows the game to keep going as long as value is True
game_on = True

#bool vars to know when either the player or dealer has busted
player_bust = False
dealer_bust = False

#create deck
deck = Deck()

#shuffle the deck
deck.shuffle()

#keep game going until game_on is False
while game_on:

    print("Placing Bets...")
    #setting the Dealer's bet to 50
    print("Dealer Bet: $50 \n")
    dealer.bet = 50
    dealer.money -= dealer.bet

    print("Player Bet... ")
    #placing the player's bet; 2 to 500
    player_1.player_bet()
    clear()

    # deal cards; 2 cards to player
    print(f"Dealing cards to {player_1.name}")

    #Deal cards to player
    player_1.hit(deck)
    player_1.hit(deck)

    #show player their cards
    print(f"{player_1.name}'s Current Hand: ")
    for card in player_1.hand:
        print(card)

    #displaying the total value of player's cards
    player_hand_value = calculate_hand_value(player_1.name, player_1.hand)
    print(f"Player's current card hand value: {player_hand_value}")

    #check for natural blackjack
    if player_hand_value == 21:
        print(f"{player_1.name} wins round!")
        player_win(player_1, dealer)

        #ask if they'd like another round
        game_on = continue_game()
        clear()
        continue

    #while the player has not busted
    while player_bust != True:
        #while player is under 21, ask player for hit/stand
        player_decision = player_1.decision()

        #if hit, check for blackjack or bust
        #if stand, dealers turn
        if player_decision == "Hit":
            #deal card to player
            player_1.hit(deck)

            #print out players current hand
            print(f"{player_1.name}'s Current Hand: ")
            for card in player_1.hand:
                print(card)

            player_hand_value = calculate_hand_value(player_1.name, player_1.hand)
            print(f'New hand value: {player_hand_value}')

            #check for blackjack or bust
            if player_hand_value == 21:
                player_win(player_1, dealer)
                player_bust = False

                #ask if they'd like another round
                game_on = continue_game()
                clear()
                break
            elif player_hand_value > 21:
                print(f"{player_1.name} has busted!")

                player_bust = True
                break
        elif player_decision == "Stand":
            break;

    #catch if the user won on the first turn and doesn't want to play
    if game_on == False:
        break

    #starting the dealer's turn
    sleep(1)
    clear()
    print(f"\n\nDealing cards to {dealer.name}")
    #put program to sleep to control flow of game
    sleep(1)
    dealer.hit(deck)
    dealer.hit(deck)

    #while the dealer has not busted
    while dealer_bust != True:
        #printing dealers current hand
        print(f"{dealer.name}'s Current Hand: ")
        for card in dealer.hand:
            print(card)

        #calculating dealers hand
        dealer_hand_value = calculate_hand_value(dealer.name, dealer.hand)
        print(f"Dealers's current card hand value: {dealer_hand_value} \n\n")

        #put program to sleep to control flow of game
        sleep(2)

        #if dealer is over 21, bust
        #if dealer in between 17 and 21, stand
        #if dealer under 16, hit
        if dealer_hand_value > 21:
            print(f"{dealer.name} has busted!")
            dealer_bust = True
        elif dealer_hand_value >= 17 and dealer_hand_value <= 21:
            print(f"{dealer.name} stands! \n\n")
            break
        elif dealer_hand_value <= 16:
            dealer.hit(deck)


    #Both players are under 21 and have not busted
    if player_bust != True and dealer_bust != True:
        print("Players are all under 21")
        print(f"{player_1.name}'s Hand Value: {player_hand_value}")
        print(f"{dealer.name}'s Hand Value: {dealer_hand_value} \n\n")

        #if the player is closer to 21 than the dealer; player takes bet
        #if the dealer is closer to 21 than the player; dealer takes bet
        #if equal, player loses
        if player_hand_value > dealer_hand_value:
            print(f"{player_1.name} is closer to 21! \n\n")
            player_win(player_1, dealer)
        elif player_hand_value < dealer_hand_value:
            print(f"{dealer.name} is closer to 21! \n\n")
            dealer_win(player_1, dealer)
        else:
            print("Draw. Dealer takes all!")
            dealer_win(player_1, dealer)


    #one of the players busted
    if player_bust == True and dealer_bust == False:
        print(f"{player_1.name} busted and has lost the round! \n\n")
        dealer_win(player_1, dealer)
    elif player_bust == False and dealer_bust == True:
        print(f"{dealer.name} busted and has lost the round! \n\n")
        player_win(player_1, dealer)
    elif player_bust == True and dealer_bust == True:
        print("Both players have busted! Dealer takes all!")
        dealer_win(player_1, dealer)

    #if player is out of money and their bet is set to 0, they automatically lose
    if player_1.money == 0 and player_1.bet == 0:
        print(f"{player_1.name} is out of money! \n\n")
        break
    elif dealer.money == 0 and dealer.bet == 0:
        print(f"{dealer.name} is out of money! \n\n")
        break

    #print player's available cash
    print(f"{player_1.name}'s cash on hand: {player_1.money} \n\n ")
    #reset player & dealer bust values to false
    player_bust = False
    dealer_bust = False
    #ask for next round or take winnings home
    game_on = continue_game()
    clear()



#game ended or player chose not to play another round
clear()
print("Thank you for playing Blackjack!")
#print total cash and their winnnings (calculated into their total cash already)
print(f"{player_1.name}'s total cash: {player_1.money} & winnings: {player_1.winnings}")
