from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
# As per Pomodoro principles, work is organised into four sessions of 25 min each:
WORK_MIN = 25
# After first 3 work sessions, a 5 min break is needed:
SHORT_BREAK_MIN = 5
# After 4th work session, a 20 min break is needed:
LONG_BREAK_MIN = 20

# A global variable for a single work or rest session. It will later be incrementally increased when timer is set:
reps = 0

# A global variable that will be used later in the "countdown" function.
# Its default value "None" is needed for the "reset_timer" function later on:
timer = None

# ---------------------------- TIMER RESET ------------------------------- #

# Setting up a function "Reset":
def reset_timer():
    global reps, timer
    reps = 0
    window.after_cancel(timer)  # Cancelling our timer

    # The only way to change a canvas item - through canvas.itemconfig:
    canvas.itemconfig(timer_digits, text="00:00")  # Changing timer digits back to "00:00"
    timer_label.config(text="Timer", fg=GREEN) # Label displays "Timer" again
    checkmark_label.config(text="")  # Resetting checkmark label to empty

# ---------------------------- TIMER MECHANISM ------------------------------- #

# Setting up a function "Start timer":
def start_timer():
    global reps
    reps += 1  # Incrementing to keep track of work/break sessions

    # Converting minutes to seconds for the timer:
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Every 8th session is a 20 min break:
    if reps % 8 == 0:
        timer_label.config(fg=RED, text="Break")
        countdown(long_break_sec)

    # Every 2nd session is a 5 min break:
    elif reps % 2 == 0:
        timer_label.config(fg=PINK, text="Break")
        countdown(short_break_sec)

    # Every other session is 20 min work session:
    else:
        countdown(work_sec)
        timer_label.config(fg=GREEN, text="Work")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

## A function that calls itself inside the timer method "window.after" which will be called soon.
# The "count" argument is the length of each session in seconds.
# "Start_timer" function (defined earlier) will call "Countdown" function and the argument "count" will have a value
# appropriate to the session type (work or break)
def countdown(count):
    # Setting up the right format for the clock digits (00:00):
    count_min = math.floor(count/60)  # Number of minutes remaining of the total time for each session
    count_sec = count % 60   # Number of seconds remaining of the total time for each session

    ## Using dynamic typing, we can change the first value from "0" to "00" for both minutes and seconds.
    # (Python allows this temporary change of a data type from integer to string)
    if count_sec == 0:
        count_sec = "00"
    elif count_sec < 10:
        count_sec = f"0{count_sec}"

    # A method specific to CANVAS class. Changes items in a canvas:
    canvas.itemconfig(timer_digits, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer  # accessing this global variable

        # The timer waits for 1 sec (= 1000 ms), then executes the countdown function, while time has not run out
        # (controlled by incrementing the "count" value by -1 every second.
        # It's saved in a variable because later we need to be able to reset the timer if the reset button is clicked:
        timer = window.after(1000, countdown, count - 1)
    else:
        start_timer()  # A function defined earlier, that manages work/break pattern and their time length
        marks = ""  # Checkmarks are not there at the start.
        work_sessions = math.floor(reps / 2)

        # One checkmark appears for every work/break session:
        for _ in range(work_sessions):
            marks += "???"
        checkmark_label.config(text=marks)  # Placing the check mark on the label to be displayed

# ---------------------------- UI SETUP ------------------------------- #

# Creating the main window for all the widgets:
window = Tk()
window.title("POMODORO".center(125))
window.config(padx=100, pady=50, bg=YELLOW)  # Adding padding and background colour


# Setting up a Canvas on which the image and clock will go:
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # Removing the white border (last parameter)


# PhotoImage is a class that reads through a file to get hold of a particular image at a particular location.
# It requires image file name and path (if it is in a different folder).
tomato_img = PhotoImage(file="tomato.png")  # Creating an object containing the tomato image
canvas.create_image(100, 100, image=tomato_img)  # Setting up canvas size to match the image and placing the image on it
canvas.grid(column=1, row=1)

# Digits of the clock timer will be displayed on the tomato image:
timer_digits = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 22, "bold"))

# Creating "Timer" label at the top of the window. Later it will change to "Work" or "Break" as appropriate:
timer_label = Label(text="Timer", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

# Creating "Start" button which will start the timer when pressed.
# One of its arguments is a function "start_timer" defined previously:
start_button = Button(bg="white", text="Start", font=(FONT_NAME, 10, "bold"), command=start_timer)
start_button.grid(column=0, row=2)

# Creating "Reset" button which will reset the timer to its original state.
# One of its arguments is a function "reset_timer" defined earlier:
reset_button = Button(bg="white", text="Reset", font=(FONT_NAME, 10, "bold"), command=reset_timer)
reset_button.grid(column=2, row=2)

# Creating a label for all the checkmarks.
# When the timer is running, every work+break session completed will get one checkmark
# (this functionality is defined within "countdown" function created earlier):
checkmark_label = Label(font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
checkmark_label.grid(column=1, row=3)


window.mainloop()