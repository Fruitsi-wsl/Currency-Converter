#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from view.start_menu import StartMenu
from view.exchange_menu import ExchangeMenu
from view.compare_menu import CompareMenu


class StartMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(StartMenuScreen, self).__init__(**kwargs)
        self.add_widget(StartMenu())

class ExchangeWindowScreen(Screen):
    def __init__(self, **kwargs):
        super(ExchangeWindowScreen,self).__init__(**kwargs)
        self.add_widget(ExchangeMenu())


class CompareWindowScreen(Screen):
    def __init__(self, **kwargs):
        super(CompareWindowScreen,self).__init__(**kwargs)
        self.add_widget(CompareMenu())

class AppController(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        # Add existing and new screens
        self.screen_manager.add_widget(StartMenuScreen(name='start_menu'))
        self.screen_manager.add_widget(ExchangeWindowScreen(name='exchange_window'))
        self.screen_manager.add_widget(CompareWindowScreen(name = 'compare_window'))
        
        return self.screen_manager

if __name__ == '__main__':
    AppController().run()