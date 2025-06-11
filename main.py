from tkinter import *

#___________________Constants___________________#
#Color Palette
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

FONT_NAME = "Courier"  #Timer Font

#Timer intervals
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20


#tracks number of pomodoro timer starts that have occurred
reps = 1

#holds a reference to the function in the recursive loop that's doing the timer update each second
timer = None

#tracks whether a countdown is currently running
timer_running = False

remaining_time = 0 #tracks the amount of time left on the timer during pauses


#resets the timer and all check marks
def reset():
    if timer is not None:
        window.after_cancel(timer)

    global timer_running, reps, remaining_time
    timer_running = False
    reset_button.grid_forget()
    stop_button.grid(row= 3, column= 3)
    reps = 1
    remaining_time = 0

    timer_label.config(text= "Pomodoro Timer", fg= GREEN, bg= YELLOW, font= (FONT_NAME, 30, "bold"))
    check_marks.config(text= "")
    canvas.itemconfig(timer_text, text= "00:00")

#Begins a new countdown
def start_timer():
    global timer_running, remaining_time

    #this conditional ensures the user cannot accidentally run multiple timers at once
    if not timer_running:
        timer_running = True
        stop_button.grid(row= 3, column= 3)
        reset_button.grid_forget()

        #this conditional ensures that paused time will be correctly un-paused rather than reset
        if remaining_time > 0:
            count_down(remaining_time)

        else:
            #Work timer
            if reps % 2 == 1:
                count_down(WORK_MIN * 60)
                timer_label.config(text= "Work", fg= GREEN)
            #Long Break timer
            elif reps % 8 == 0:
                count_down(LONG_BREAK_MIN * 60)
                timer_label.config(text= "Take A Rest", fg= PINK)
            #Short Break timer
            else:
                count_down(SHORT_BREAK_MIN * 60)
                timer_label.config(text= "Break", fg= RED)

#pauses the current countdown
def stop_timer():
    global timer_running, remaining_time
    timer_running = False
    reset_button.grid(row= 3, column= 3)
    stop_button.grid_forget()

    #get time remaining
    time_left = canvas.itemcget(timer_text, 'text')
    time_left = time_left.split(":")
    minutes = int(time_left[0])
    seconds = int(time_left[1])
    remaining_time = int((60 * minutes) + seconds)

#updates the timer every second and increases reps when a countdown has reached 0
def count_down(count):
    global timer_running

    if timer_running:
        if count % 60 < 10:
            canvas.itemconfig(timer_text, text= f"{int(count / 60)}:0{count % 60}")
        else:
            canvas.itemconfig(timer_text, text= f"{int(count / 60)}:{count % 60}")

        if count > 0:
            global timer
            timer = window.after(1000, count_down, count - 1)
        else:
            global reps, remaining_time
            reps += 1
            remaining_time = 0

            #Append number of checkmarks to indicate pomodoro rounds completed
            marks = ""
            for mark in range(int(reps/2)):
                marks += '✔'
            check_marks.config(text= marks)

            timer_running = False
            start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx= 100, pady= 50, bg= YELLOW)

#provide tomato background and timer graphic
canvas = Canvas(width= 200, height= 224, bg= YELLOW, highlightthickness= 0)
tomato_img = PhotoImage(file= "tomato.png")
canvas.create_image(100, 112, image= tomato_img)
timer_text = canvas.create_text(103, 130, text= "00:00", fill= "white", font= (FONT_NAME, 35, "bold"))
canvas.grid(row= 2, column= 2)

#'Pomodoro Timer' Label
timer_label = Label(text= "Pomodoro Timer", fg= GREEN, bg= YELLOW, font= (FONT_NAME, 30, "bold"))
timer_label.grid(row= 1, column= 2)

#Timer start, stop, and reset buttons
start_button = Button(text= "Start", highlightthickness= 0, command= start_timer)
stop_button = Button(text= "Stop", highlightthickness= 0, command= stop_timer)
reset_button = Button(text= "Reset", highlightthickness= 0, command= reset)
start_button.grid(row= 3, column= 1)
stop_button.grid(row= 3, column= 3)

#Indicates number of Pomodoro rounds completed
check_marks = Label(text= "", fg= GREEN, bg= YELLOW, font= (FONT_NAME, 18, "bold"))
check_marks.grid(row= 4, column= 2)



window.mainloop()