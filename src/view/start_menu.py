#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class StartMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.add_widget(Label(text="Currency Converter", font_size='24sp'))
        
        self.start_button = Button(text="Start", size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5})
        self.start_button.bind(on_press=self.on_start_button_press)
        self.add_widget(self.start_button)
        
    def on_start_button_press(self, instance):
        print("Start button pressed")

class StartMenuApp(App):
    def build(self):
        return StartMenu()

if __name__ == '__main__':
    StartMenuApp().run()