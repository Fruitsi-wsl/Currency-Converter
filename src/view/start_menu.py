#!/usr/bin/env python3

import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

current_dir = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(current_dir, "Image Resources/background2.jpg" )

class StartMenu(FloatLayout):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)

        self.background = Image(source=image_path, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)
        
        # Label at the top center
        self.add_widget(Label(
            text="Currency Converter", font_size='24sp',
            color=(24/255, 198/255, 128/255, 1),
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 1}
        ))
        
        # Button at the center
        self.start_button = Button(
            text="Show current rates",
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.start_button.bind(on_press=self.on_start_button_press)
        self.add_widget(self.start_button)

        self.compare_button = Button(
            text="Compare currencies",
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        self.compare_button.bind(on_press=self.on_compare_button_press)
        self.add_widget(self.compare_button)

        
    def on_start_button_press(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'exchange_window'

    def on_compare_button_press(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'compare_window'