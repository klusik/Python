'''
author: Michal Sykora
date: 7.5.2022
version: 0.1 pre-alpha
license: freeware
'''
# https://www.geeksforgeeks.org/python-easygui-enter-box/?ref=rp

# GLOBAL IMPORTS

# PRIVATE IMPORTS

# THIRD PARTY IMPORTS
import easygui

def MainWindow():
    '''Main application window showing control buttons'''

    # message displayed to user
    message = '''
    
    Welcome to BMI tracker

    Click on buttons to:
    enter values
    generate graph
    generate pdf
    show records
    create new file
    '''

    # create buttons
    title = 'BMI Tracker - know your fat!'
    button_list = []
    weight = 'Weight'
    height = 'Height'
    chest = 'Chest'
    belly = 'Belly'
    bottom = 'Bottom'
    graph = 'Graph'
    pdf = 'PDF'
    records = 'show records'
    exit = 'exit'
    file = 'new file'

    # add buttons to list of buttons
    button_list.append(weight)
    button_list.append(height)
    button_list.append(chest)
    button_list.append(belly)
    button_list.append(bottom)
    button_list.append(graph)
    button_list.append(pdf)
    button_list.append(records)
    button_list.append(exit)
    button_list.append(file)
    
    # create indexbox, where each button has assigned index from 0 to infinity
    IndexOfMaineChoice = easygui.indexbox(message, title, button_list)

    # weight button pressed
    if  IndexOfMaineChoice == 0:
        # ask for value
        userWeight = easygui.enterbox('Enter your weight [kg]', 'Weight[kg]')
        # confirmation message
        easygui.msgbox(f'You have entered {userWeight}, value persisted', 'Status: Confirmation')
        
        # write value to xml file

        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)        

    # height button pressed
    elif IndexOfMaineChoice == 1:
        # ask for value
        UserHeight = easygui.enterbox('Enter your height [cm]', 'Height[cm]')
        # confirmation message
        easygui.msgbox(f'You have entered {UserHeight}, value persisted', 'Status: Confirmation')

        # write value to xml file

        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # chest button pressed
    elif IndexOfMaineChoice == 2:
        # ask for value
        UserChest = easygui.enterbox('Enter your height [cm]', 'Height[cm]')
        # confirmation message
        easygui.msgbox(f'You have entered {UserChest}, value persisted', 'Status: Confirmation')

        # write value to xml file

        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # belly button pressed
    elif IndexOfMaineChoice == 3:
        # ask for value
        UserBelly = easygui.enterbox('Enter your height [cm]', 'Height[cm]')
        # confirmation message
        easygui.msgbox(f'You have entered {UserBelly}, value persisted', 'Status: Confirmation')

        # write value to xml file

        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # bottom button pressed
    elif IndexOfMaineChoice == 4:
        # ask for value
        UserBottom = easygui.enterbox('Enter your height [cm]', 'Height[cm]')
        # confirmation message
        easygui.msgbox(f'You have entered {UserBottom}, value persisted', 'Status: Confirmation')

        # write value to xml file

        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # graph button pressed
    elif IndexOfMaineChoice == 5:
        # not implemented alert
        easygui.msgbox('Functionality not yet implemented, stay tuned!', 'Graph')
        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # PDF button pressed
    elif IndexOfMaineChoice == 6:
        # not implemented alert
        easygui.msgbox('Functionality not yet implemented, stay tuned!', 'PDF')
        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # records button pressed
    elif IndexOfMaineChoice == 7:
        # not implemented alert
        easygui.msgbox('Functionality not yet implemented, stay tuned!', 'Records')
        # regenerate the main window
        WindowObject = easygui.indexbox(message, title, button_list)

    # exit button pressed
    elif IndexOfMaineChoice == 8:
        # not implemented alert
        easygui.msgbox('Finishing!', 'Exit')

MainWindow()