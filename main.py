#to be able to clear output
from IPython.display import clear_output
#modules needed to shuffle deck
import random

#global variables to construct Deck
card_values = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
               "Jack":10, "Queen":10, "King":10, "Ace":11,}
suits = ("Spades", "Clubs", "Hearts", "Diamonds")


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
            bet_input = input("Please place your bet (2 - 500): ")

            if bet_input.isdigit():
                bet_input = int(bet_input)

                if bet_input > self.money:
                    print("Not enough money to place bet.")
                    print(f"Current cash on hand: {self.money}")
                    continue

                if bet_input < 2:
                    print("Please place a bet greater than or equal to 2.")
                    continue
                elif bet_input > 500:
                    print("Please place a bet less than or equal to 500.")
                    continue
                else:
                    self.bet = bet_input
                    self.money -= self.bet
                    return
            else:
                continue

    #asking the player if they'd like to hit or stand
    def decision(self):
        while True:
            decision = input("\n\nWould you like to Hit or Stand? ")

            if decision.capitalize() == "Hit":
                return "Hit"
            elif decision.capitalize() == "Stand":
                return "Stand"
            else:
                print("Please use only Hit or Stand.")
                continue


#to be able to clear output
from IPython.display import clear_output

#begin the game
print("Welcome to Blackjack!")

#asking for Player's Name
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

                #ask the player each time what theyd like for the ace value to be
                while True:
                    ace_value = input("Would you like the Ace to count as 1 or 11?")

                    if ace_value.isdigit():
                        ace_value = int(ace_value)

                        if ace_value == 11:
                            hand_value += ace_value
                            break
                        elif ace_value == 1:
                            hand_value += ace_value
                            break
                        else:
                            print("Please select 1 or 11 only.")
            else:
                hand_value += c.value

    return hand_value

#function to ask player if they'd like to play another round of blackjack
def continue_game():
    while True:
        result = input("Another Round? (True/False): ")

        #if they want another round, clear the player and dealer's hand
        if result.capitalize() == "True":
            player_1.hand = []
            dealer.hand = []
            return True
        elif result.capitalize() == "False":
            return False
        else:
            print("Please use True or False only.")



#keep game going until game_on is False
while game_on:


    #placing the player's bet; 2 to 500
    player_1.player_bet()
    clear_output()

    # deal cards; 2 up & 1 down - player
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
        player_1.money += player_1.bet
        player_1.winnings += player_1.bet
        player_1.bet = 0
        #ask if they'd like another round
        game_on = continue_game()
        clear_output()
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

            #look for blackjack or bust
            if player_hand_value == 21:
                print(f"{player_1.name} wins round!")
                player_1.money += player_1.bet
                player_1.winnings += player_1.bet
                player_1.bet = 0
                player_bust = False
                #ask if they'd like another round
                game_on = continue_game()
                clear_output()
                break
            elif player_hand_value > 21:
                print(f"{player_1.name} has busted!")
                player_1.bet = 0
                player_bust = True
        elif player_decision == "Stand":
            break;

    #catch if the user one on first turn and doesn't want to play
    if game_on == False:
        break

    #dealing the dealers hand
    print(f"\n\nDealing cards to {dealer.name}")
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


        #if dealer is over 21, bust
        #if dealer in between 17 and 21, stand
        #if dealer under 16, hit
        if dealer_hand_value > 21:
            print(f"{dealer.name} has busted!")
            print(f"{player_1.name}'s winnings this round: {player_1.bet} \n\n")
            player_1.money+=player_1.bet
            player_1.winnings += player_1.bet
            player_1.bet = 0
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

        # if the player is closer to 21 than the dealer; player takes bet
        #if the dealer is closer to 21 than the player; dealer takes bet
        if player_hand_value > dealer_hand_value:
            print(f"{player_1.name} is closer to 21! \n\n")
            player_1.money+=player_1.bet
            player_1.winnings += player_1.bet
        else:
            print(f"{dealer.name} is closer to 21! \n\n")
            player_1.bet = 0

    #both stand but one of the players busted
    if player_bust == True and dealer_bust == False:
        print(f"{player_1.name} has lost the round! \n\n")
    elif player_bust == False and dealer_bust == True:
        print(f"{dealer.name} has lost the round! \n\n")
    else:
        print("Both players have busted!")

    #if player is out of money and their bet is set to 0, they automatically lose
    if player_1.money == 0 and player_1.bet == 0:
        print(f"{player_1.name} is out of money! \n\n")
        break

    print(f"{player_1.name}'s cash on hand: {player_1.money} \n\n ")
    #ask for next round or take winnings home
    game_on = continue_game()



clear_output()
print("Thank you for playing Blackjack!")
#print total cash and any they won from rounds including money they won back from betting
print(f"{player_1.name}'s total cash: {player_1.money} & winnings: {player_1.winnings}")

    