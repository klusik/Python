'''
author: Michal Sykora
date: 7.5.2022
version: 0.1 pre-alpha
license: freeware
'''
# https://www.geeksforgeeks.org/python-easygui-enter-box/?ref=rp
# change for the sake of GIT testing 

# IMPORTS
import easygui

# just a little test of gui
text = 'enter some value'
title = 'test gui'
d_text = 'enter value'
output = easygui.enterbox(text, title, d_text)

title = 'message box'
message = 'entered name:' + str(output)

msg = easygui.msgbox(message, title)
print(output, message)
