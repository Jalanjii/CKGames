# template for "Stopwatch: The Game"
import simplegui
# define global variables
n = 0
stopcount = 0
stopmatch = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global D
    D = t % 10
    C = (t / 10) % 10
    B = (t / 100) % 6
    A = t // 600
    string = str(A)+':'+str(B)+str(C)+'.'+str(D)
    return string
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    
    timer.start()
def stop():
    global stopcount, stopmatch
    run = timer.is_running()
    if run == True:
        stopcount = stopcount + 1
        if D == 0:
            stopcount = stopcount - 1
            stopmatch = stopmatch + 1
    timer.stop()
def reset():
    global n, stopcount, stopmatch
    n = 0
    stopcount = 0
    stopmatch = 0
    timer.stop()


# define event handler for timer with 0.1 sec interval
def glob():
    global n
    n = n + 1

# define draw handler
def draws(canvas):
    N = format(n)
    canvas.draw_text(N, (75,105), 26, 'White')
    result = (str(stopmatch) + '/' + str(stopcount))
    canvas.draw_text(result, (160,30), 20, 'White')
    
# create frame
frame = simplegui.create_frame('Stopwatch', 200, 200)
timer = simplegui.create_timer(100, glob)
# register event handlers
frame.set_draw_handler(draws)
frame.add_button('Start', start)
frame.add_button('Stop', stop)
frame.add_button('Reset', reset)

# start frame

frame.start()

# Please remember to review the grading rubric
