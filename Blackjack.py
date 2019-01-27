
import random
from time import sleep

suits = ('♦', '♣', '♥', '♠')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (f'{self.rank}{self.suit}')


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        s = ''
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + '\n'
        return s

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        is_empty = False
        if len(self.deck) == 0:
            is_empty = True
        if is_empty == False:
            return self.deck.pop()
        else:
            print('The deck is empty!')


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=0, bet=0):
        self.total = total
        self.bet = bet

    def win_bet(self):
        self.total = self.total + self.bet

    def lose_bet(self):
        self.total = self.total - self.bet


def take_bet():
    taken = False
    while not taken:
        try:
            bet = int(input("How much would you like to bet? You cannot bet more than you have."))
        except BaseException:
            print('Please give me an integer amount: ')
            continue
        if isinstance(bet, int):
            taken = True
    return bet


def take_total():
    taken = False
    while not taken:
        try:
            total = int(input("How many chips would you like to play with? "))
        except BaseException:
            print('Please give me an integer amount: ')
            continue
        if isinstance(total, int):
            taken = True
    return total


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    hit_stand = False
    while hit_stand == False:
        print('\n' * 2)
        question = input('Would you like to Hit or Stand? ')
        if question.lower() == 'hit':
        	print('You draw...\n')
        	sleep(2)
        	hit(deck, hand)
        	print(f'You drew a [{player.cards[-1]}]\n')
        	hit_stand = True
        elif question.lower() == 'stand':
            playing = False
            hit_stand = True


def show_some(player, dealer):
    print("The Dealer's cards are:") 
    print('\n')
    print('[Hidden]')
    for i in range(1, len(dealer.cards)):
        print('[' + str(dealer.cards[i]) + ']')
    print('\n')
    print('-------------------------')
    print('Your cards are: ')
    print('\n')
    for n in range(len(player.cards)):
        print('[' + str(player.cards[n]) + ']')
    print('\n')
    print(f'Your value is: {player.value}')

def show_all(player, dealer):
    print("The Dealer's cards are: ")
    print('\n')
    for i in range(len(dealer.cards)):
        print('[' + str(dealer.cards[i]) + ']')
    print('\n')
    print(f'Dealer value is: {dealer.value}')
    print('-------------------------')
    print('Your cards are: ')
    print('\n')
    for n in range(len(player.cards)):
        print('[' + str(player.cards[n]) + ']')
    print('\n')
    print(f'Your value is: {player.value}')

def player_busts():
    player.value = 0
    print('You bust! Your value is now 0.')

def player_wins():
    if dealer.value < player.value and player.value < 22:
        print('Player wins!')
        return player_chips.win_bet()


def dealer_busts():
    dealer.value = 0
    print('Dealer Busts!')


def dealer_wins():
    if player.value < dealer.value and dealer.value < 22:
        print('Dealer wins!')
        return player_chips.lose_bet()


def push():
    if dealer.value == player.value:
        print('It is a push!')


def replay():
    yes_no = False
    while not yes_no:
        replay = input(f'Your amount is {player_chips.total}. Would you like to play again? Please say Yes or No. ')
        if replay.lower() == 'yes':
            if player_chips.total == 0:
                print('Sorry, the amount of chips you own is 0. You can no longer play.')
                break
            yes_no = True
        elif replay.lower() == 'no':
            break

    return yes_no


print('Welcome to BlackJack!\n')
total = take_total()
playing = True
while True:

    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())

    bet = take_bet()
    while bet > total:
        bet = take_bet()
    player_chips = Chips(total, bet)
    print('\n')
    
    

    while playing:
        show_some(player, dealer)
        hit_or_stand(deck, player)
        
        if player.value > 21:
            player_busts()
            break
    print('\n')
    show_all(player, dealer)
    print('\n')
    if player.value == 0:
        dealer_wins()

    while dealer.value < 18 and player.value != 0:
        hit(deck, dealer)
        print('\nDealer draws...')
        sleep(3)
        print(f'Dealer drew a [{dealer.cards[-1]}]\n')
        show_all(player, dealer)
        

        if dealer.value > 21:
            dealer_busts()
            player_wins()
            break
    if dealer.value >= 17 and player.value != 0:
        if player_wins():
            break
        elif dealer_wins():
            break
        if push():
            break

    print("\n")

    if not replay():
        print(
            f'Thank for playing!! You started with {total} this round and now have {player_chips.total}. ')
        if player_chips.total < 0:
            print(f'You owe us {abs(player_chips.total)}.')
        break
    else:
        total = player_chips.total
        playing = True
