from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import sqlite3 as sq
import test4

conn = sq.connect('game.db')
c = conn.cursor()


class gamedialogbox(GridLayout):
    def __init__(self, **kwargs):
        super(gamedialogbox, self).__init__(**kwargs)
        self.cols = 1
        self.row_force_default = True
        self.row_default_height =80
        self.add_widget(Label(text="Lastname:", bold = True, color = [0.2,0.8,1.00,1]))
        self.lastname = TextInput(multiline=False)
        self.add_widget(self.lastname)
        self.add_widget(Label(text="FirstName:", bold = True, color = [0.2,0.8,1.00,1]))
        self.firstname = TextInput(multiline=False)
        self.add_widget(self.firstname)
        self.submit = Button(text="Register", font_size=32, color= (0,0,0,1), background_color = (1.32,0.78,1.64,1))
        self.add_widget(self.submit)
        self.submit.bind(on_press=self.appear_button)
        self.submit = Button(text="Quit Game", font_size=32, color= (0,0,0,1), background_color = (1.25,1.13,0.86,1))
        self.add_widget(self.submit)
        self.submit.bind(on_press=self.exit_game)


    def appear_button(self, instance):
        lastname = self.lastname.text
        firstname = self.firstname.text
        players_value = [lastname, firstname]
        if lastname == '' or firstname == '':
            popup=Popup(title='Mandatory', content=Label(text='You need to register first, click ESC',bold = True,font_size=32, color = [1,0,0,1]))
            popup.open()
        else:
            c.execute('INSERT into players (Lastname,Firstname) VALUES (?,?)', players_value)
            conn.commit()
            self.submit = Button(text="Start Game", font_size=32, color= (0,0,0,1), background_color = (1.27,2.55,2.12,1))
            self.add_widget(self.submit)
            self.submit.bind(on_press=self.game_button)

    def game_button(self, instance):
        try:
            test4.find_image()
        finally:
            popup2 =Popup(title='Game is over',content=Label(text='Click ESC for a new game',bold = True,font_size=32, color = [0.2,0.4,1,1]))
            popup2.open()


    def exit_game(self,instance):
        App.get_running_app().stop()


class Mygame(App):
    def build(self):
        return gamedialogbox()


if __name__=='__main__':
    Mygame().run()










