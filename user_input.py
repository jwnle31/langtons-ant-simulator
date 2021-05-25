from tkinter import *
from os import startfile
import re
import ant_pattern

# Initializing Window
root = Tk()
root.title("Langton's Ant Simulator")
root.geometry('405x210')
root.iconbitmap('ant_img.ico')
root.resizable(width=False, height=False)

# Labels and Text Boxes
rule_frame = Frame(root, bd=10)
rule_frame.grid(row=0, column=0, sticky=E)
rule_label = Label(rule_frame, text='Ruleset:')
rule_label.config(font=('Verdana', 10))
rule_label.grid()

rule_txt = Entry(root, width=45)
rule_txt.grid(row=0, column=1, sticky=W, columnspan=2)
rule_txt.insert(0, 'RL')

speed_frame = Frame(root, bd=10)
speed_frame.grid(row=1, column=0, sticky=E)
speed_label = Label(speed_frame, text='Steps/Frame:')
speed_label.config(font=('Verdana', 10))
speed_label.grid()

speed_txt = Entry(root, width=8)
speed_txt.grid(row=1, column=1, sticky=W)
speed_txt.insert(0, '1000')

rec_frame = Frame(root, bd=10)
rec_frame.grid(row=1, column=2, sticky=SW)
rec_label = Label(rec_frame, text='Recommendation: 0<x≤3000')
rec_label.config(font=('Verdana', 6))
rec_label.grid()

color_frame = Frame(root, bd=10)
color_frame.grid(row=2, column=0, sticky=E)
color_label = Label(color_frame, text='Colors:')
color_label.config(font=('Verdana', 10))
color_label.grid()


def edit_color():
    startfile('colors.txt')


color_button = Button(root, text='Edit File', command=edit_color).grid(row=2, column=1, columnspan=2, sticky=W)

warning_frame = Frame(root)
warning_frame.grid(row=4, column=0, columnspan=3, sticky=N)
warning_label = Label(warning_frame, text='')
warning_label.config(font=('Verdana', 6))
warning_label.grid()


def disable_event():
    pass


# Checking Errors and Running the Pyglet Program
def launch_ant():
    r_txt = rule_txt.get()
    s_txt = speed_txt.get()
    valid_rule = re.fullmatch('[RLUN]+', r_txt)
    valid_speed = re.fullmatch('[1-9][0-9]*', s_txt)

    c_file = open('colors.txt')
    c_list = c_file.readlines()
    c_file.close()

    valid_file_length = True
    if len(c_list) < len(r_txt):
        valid_file_length = False

    range_pattern = '([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'  # Numbers Between 0~255 (Inclusive)
    valid_file = True
    for idx, color in enumerate(c_list):
        if color[len(color) - 1] == '\n':
            color = color[:-1]
        valid_color = re.fullmatch('\(' + range_pattern + ', ' + range_pattern + ', ' + range_pattern + '\)', color)
        if not valid_color:
            print('Invalid Color Detected')
            valid_file = False
            break
        c_list[idx] = eval(color)

    # Error Statements
    warning_label['fg'] = 'red'
    if not valid_rule:
        warning_label['text'] = 'Please enter a valid ruleset (R, L, U, or N).'
    elif not valid_speed:
        warning_label['text'] = 'Please enter a valid steps/frame (positive integer).'
    elif not valid_file_length:
        warning_label['text'] = 'The length of the ruleset is greater than the number of lines in the color file.'
    elif not valid_file:
        warning_label['text'] = 'Invalid color detected in the color file.'
    elif len(c_list) != len(set(c_list)):
        warning_label['text'] = 'Duplicate color detected in the color file.'
    else:
        # Running Process
        root.protocol("WM_DELETE_WINDOW", disable_event)
        warning_label['fg'] = 'green'
        warning_label['text'] = 'Successfully launched.'
        launch_button['state'] = 'disabled'
        launch_button.update()
        ant_pattern.ant_run(r_txt, eval(s_txt))
        launch_button.update()
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        warning_label['text'] = ''
        launch_button['state'] = 'normal'


launch_button_frame = Frame(root)
launch_button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
launch_button = Button(launch_button_frame, text='Launch', width=10, height=2, command=launch_ant)
launch_button.grid()

root.mainloop()
