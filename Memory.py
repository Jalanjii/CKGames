# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed, state, counter
    counter = 0
    label.set_text('Turn = ' + str(counter))
    cards = ((range(0,8))*2)
    exposed = [False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False]
    trues = []
    random.shuffle(cards)
    state = 0

def mouseclick(pos):
    global state, fcard, scard, pos1, pos2, pos3, counter
    position = (list(pos)[0]) / 50
    if state == 0:
        for index in range(len(exposed)):
            pos1 = position
            if pos1 == index:
                counter += 1
                label.set_text('Turn = ' + str(counter))
                pos1 = position
                exposed[pos1] = True
                fcard = cards[pos1]
                state = 1
      
    elif state == 1:
        for index in range(len(exposed)):
            pos2 = position
            if pos2 == index  and exposed[pos2] != True:
                pos2 = position
                exposed[pos2] = True
                scard = cards[pos2]
                state = 2
                
    else:
        if fcard == scard and exposed[pos1] != True and exposed[pos2] != True: 
            exposed[pos1] = True #exposed[pos1]
            exposed[pos2] = True #exposed[pos2]
        if fcard != scard:
            exposed[pos1] = False
            exposed[pos2] = False
        
        for index in range(len(exposed)):
            pos1 = position
            if pos1 == index and exposed[pos1] != True:
                counter += 1
                label.set_text('Turn = ' + str(counter))
                pos1 = position
                exposed[pos1] = True
                fcard = cards[pos1]
                state = 1
                
# cards are logically 50x100 pixels in size 
def draw(canvas):
    for card_index in range(len(cards)):
        card_pos = 50 * card_index
        text_pos = 50 * card_index + 15
        if exposed[card_index] == True:
            canvas.draw_text(str(cards[card_index]), (text_pos, 50), 30, 'White')
        if exposed[card_index] == False:
            canvas.draw_line((card_pos, 50), (card_pos + 49, 50), 100, 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label('Turn = 0')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric