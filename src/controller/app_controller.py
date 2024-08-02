#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from view.start_menu import StartMenu

class StartMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(StartMenuScreen, self).__init__(**kwargs)
        self.add_widget(StartMenu())

class AppController(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(StartMenuScreen(name='start_menu'))
        return self.screen_manager

if __name__ == '__main__':
    AppController().run()