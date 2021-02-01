
import simplegui
import random
import math

num_range = 100
secret_number = 0
remaining = 0

def new_game():
    global num_range
    print 'New Game. Range is from 0 to', num_range
    global remaining
    remaining = int(math.ceil(math.log(num_range, 2)))
    print 'Number of remaining gueses is:',remaining , '\n\n'
    global secret_number
    secret_number = random.randrange(0, num_range)
    return secret_number

   
def range100():
    global num_range
    num_range = 100
    new_game()
    global secret_number
    secret_number = random.randrange(0, num_range)
    
    
def range1000():
    global num_range
    num_range = 1000
    new_game()
    global secret_number
    secret_number = random.randrange(0, num_range)
    
          
def input_guess(guess):
    global remaining
    remaining -= 1
    iguess = int(guess)
    print 'Guess was', iguess
    
    if iguess == secret_number:
        print 'Correct\n\n'
        new_game()
        
    elif iguess > secret_number:
        print 'Number of remaining gueses is:', remaining
        print 'Lower\n'
        
    elif iguess < secret_number:
        print 'Number of remaining gueses is:', remaining
        print 'Higher\n'
        
    if remaining == 0:
        #print 'Number of remaining gueses is:', remaining
        print 'You ran out of guesses. The number was:', secret_number, '\n\n\n'
        new_game()

f = simplegui.create_frame('Guess the number', 200, 200)
f.add_button('Range is [0, 100[', range100, 200)
f.add_button('Range is [0, 1000[', range1000, 200)
f.add_input('Guess!', input_guess, 100)


new_game()
f.start()