
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


in_play = False
outcome = ""
score = 0


SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        stri = ""
        for i in self.hand:# return a string representation of a hand
            stri += " " + str(i)
        return "Hand Contains" + stri
            

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        ace = False
        if len(self.hand) == 0: return value
        
        for i in self.hand:
            value += int(VALUES[str(i)[1]])
            if str(i)[1] == "A":
                ace = True
        if value + 10 <= 21 and ace:
            value += 10
        else:
            value = value   
        return value
        
    def draw(self, canvas, pos):
        i = 1
        card_locs = []
        for hnd in self.hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(hnd.get_rank()),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(hnd.get_suit()))
            if i <= 5:
                canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0]*i + CARD_CENTER[0],
                                                    pos[1] + CARD_CENTER[1]], CARD_SIZE)
            else:
                canvas.draw_text("You Can't Hit More, Stand!", (350, 100), 20, "Red")
            i += 1            
        
class Deck:
    def __init__(self):
        self.deck = []
        for i in RANKS:# create a Deck object
            for j in SUITS:
                self.deck.append(Card(j, i))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return random.choice(self.deck)	# deal a card object from the deck
    
    def __str__(self):
        stri = ""
        for i in self.deck:	# return a string representing the deck
            stri += " " + str(i)
        return "Deck contains" + stri


def deal():
    global outcome, in_play, player, dealer, deckshuffle, deck, score
    deck = Deck()
    deckshuffle = deck.shuffle()
    player = Hand()
    dealer = Hand()
    
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        
    outcome = "Hit/stand? Or New deal?"
    
    if in_play:
        outcome = "Dealer Has Just Won it!"
        score -= 1
        in_play = False
        
    elif player.get_value() <= 21:
        in_play = True
    else:
        in_play = False
    
    return outcome
    
def hit():
    global in_play, outcome, score
    if player.get_value() <= 21 and in_play:# if the hand is in play, hit the player
        player.add_card(deck.deal_card())
#        outcome = "Dealer "+str(dealer)+", Player "+str(player)
        in_play = True
        
    if player.get_value() > 21:# if busted, assign a message to outcome, update in_play and score
        in_play = False
        outcome = "You have Just Busted!"
        score -= 1
    return outcome

def stand():
    global outcome, in_play, score
    if not in_play:
        return "You have Just Busted!"
    while in_play:
        dealer.add_card(deck.deal_card())
        if 17 <= dealer.get_value()<= 21:
            in_play = True
            if player.get_value() <= dealer.get_value():
                outcome = "Dealer Has Just Won it!"
                score -= 1
            else:
                outcome = "Player Has Just Won it!"
                score += 1
        if dealer.get_value() > 21:
            outcome = "Dealer Has Just Busted!"
            score += 1
            in_play = False
        
            
    return outcome

    
  
def draw(canvas):
    global player, outcome
    player.draw(canvas, [72, 120])
    dealer.draw(canvas, [72, 240])
    canvas.draw_text("Blackjack Game", (160, 60), 40, "White")
    canvas.draw_text("Player", (11, 110), 20, "White")
    canvas.draw_text(outcome, (170, 430), 25, "Black")
    canvas.draw_text("Dealer", (11, 240), 20, "White")
    canvas.draw_text("Player's Score:"+str(score), (230, 500), 20, "Black")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [72 + CARD_CENTER[0],
                                                    240 + CARD_CENTER[1]], CARD_BACK_SIZE)
    
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()

frame.start()
