import simplegui
import random


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")


# initialize some useful global variables
in_play = False
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images,
                          card_loc,
                          CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        output = "Hand contains "
        for card in self.hand:
            output += str(card) + "|"
        return output

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        aces = 0
        for card in self.hand:
            if not card.get_rank() == "A":
                if hand_value + VALUES[card.get_rank()] > 21 and aces > 1:
                    hand_value = hand_value - 10
                    aces -= 1
                hand_value += VALUES[card.get_rank()]
            else:
                hand_value += 1
                aces += 1
                if hand_value + 10 <= 21:
                    hand_value += 10
        return hand_value

    def draw(self, canvas, pos):
        center_position = pos
        #print center_position
        for card in self.hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))
            canvas.draw_image(card_images,
                              # center_source
                              card_loc,
                              # width_height_source, (72, 96)
                              CARD_SIZE,
                              # center_destination, needs to shift with new card
                              [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                              # width_height_dest
                              CARD_SIZE)
            pos[0] += CARD_SIZE[0]



# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        next_card = self.deck.pop()
        return next_card

    def __str__(self):
        output = "Deck contains "
        for card in self.deck:
            output += str(card) + " "
        return output


#define event handlers for buttons
def deal():
    global in_play, deck, player_hand, dealer_hand
    # initialize a new deck
    deck = Deck()
    deck.shuffle()

    # initialize new hand for player and dealer
    player_hand, dealer_hand = Hand(), Hand()

    # player is dealt to first
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "PLAYER", player_hand
    print "DEALER", dealer_hand

    # switch to start play
    in_play = True


def hit():
    global in_play
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        print "PLAYER", player_hand
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        in_play = False
        print "You have busted."


def stand():
    global in_play, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print "DEALER", dealer_hand, dealer_hand.get_value()
        # assign a message to outcome, update in_play and score
        in_play = False
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted at " + str(dealer_hand.get_value()) + ". You win!"
        elif dealer_hand.get_value() > player_hand.get_value():
            outcome = "Dealer has " + str(dealer_hand.get_value()) + ". You have " + str(player_hand.get_value()) + ". Dealer wins."
        elif dealer_hand.get_value() == player_hand.get_value():
            outcome = "You and the dealer both have " + str(dealer_hand.get_value()) + ". Push. Dealer wins."
        else:
            outcome =  "Dealer has " + str(dealer_hand.get_value()) + ". You have " + str(player_hand.get_value()) + ". You win!"
        # final message
        print outcome


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # card = Card("S", "A")
    # card.draw(canvas, [300, 300])

    # test draw handler for hand.draw in upper left corner
    player_hand.draw(canvas, [600 // 5, 600 // 1.5])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()