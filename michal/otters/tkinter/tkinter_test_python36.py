#tkinter
import tkinter as tk
from tkinter import ttk


class App(tk.Tk): #trida dedi vlastnosti z tridy Tk, ktera je ulozena v modulu tk.

    ### PLYN_PEDAL = 1
    ### BRZDA_PEDAL = 2

    def __init__(self):
        tk.Tk.__init__(self)    #spusti se init metoda tridy Tk z modulu tk

        self.title("Tkinter Tab Widgets")   #self je odkaz sam na sebe, takze tk.Tk udela title
        self.minsize(600,400)   #tk.Tk udela okno

        tabControl = ttk.Notebook(self) #promenna tabControl vola metodu Notebook tridy ttk
        
        tab1 = ttk.Frame(tabControl)    #promenna tab1 vytvori frame pomoci tabControl
        tabControl.add(tab1, text = "Tab 1")    #tabControl prida zalozku s textem Tab 1

        #viz tab1
        tab2 = ttk.Frame(tabControl)    
        tabControl.add(tab2, text = "Tab 2")

        tabControl.pack(expan = 1, fill = "both")   #to nevim, co presne dela, ale bez toho to nejede

        #tlacitko na tab1
        btn1t1 = tk.Button(tab1, text = "Button 2")
        btn1t1.pack()

        #tlacitko an tab2
        btn2t2 = tk.Button(tab2, text = "Button 2")
        btn2t2.pack()

        
        #win = tk.Tk() #win je instance tridy Tk, vytvori okno

        #pridam label a button
        #self.aLabel = ttk.Label(self, text="A Label")
        # self.aLabel.grid(column=0, row=0)
        #self.aLabel.pack()

        #adding button
        #self.action = ttk.Button(self, text="Please, master, click me!", command=self.clickMe)
        #self.action.grid(column=1, row=0)
        #self.action.pack()

        #self.cisloPlynPedalu = cisloPlynPedalu
        #self.cisloBrzdaPedalu = cisloBrzdaPedalu
    
    #button clicked
    def clickMe(self):        
        self.action.configure(text="** I have been Clicked, Thank you, master! **")
        self.aLabel.configure(foreground = "red")

    
app = App()
app.mainloop()
