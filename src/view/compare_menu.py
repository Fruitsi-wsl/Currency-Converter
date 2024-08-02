#!/usr/bin/env python3

import os
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from model.get_exchange_rate_data import fetch_exchange_rates
from controller import shared_variables as shared_variables

current_dir = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(current_dir, "Image Resources/background1.jpg" )

API_KEY = 'cb0c995beeb4118248dd2566'

class CompareMenu(FloatLayout):
    def __init__(self, **kwargs):
        super(CompareMenu, self).__init__(**kwargs)

        self.background = Image(source=image_path, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Example content for the new menu
        self.add_widget(Label(
            text="Currency Converter", font_size='24sp',
            color=(24/255, 198/255, 128/255, 1),
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 1}
        ))

        self.back_button = Button(
            text="Back",
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            size_hint=(None, None), size=(150, 50),
            pos_hint={'center_x': 0.1, 'center_y': 0.9}
        )
        self.back_button.bind(on_press=self.on_back_button_press)
        self.add_widget(self.back_button)



        # First currency selection
        self.currency1_input = TextInput(
            hint_text="Search currency",
            size_hint=(None, None), size=(150,35),
            pos_hint={'center_x': 0.35, 'center_y': 0.8},
            multiline=False
        )
        self.currency1_input.bind(text=self.update_currency1_options)
        self.add_widget(self.currency1_input)

        self.currency1_spinner = Spinner(
            text="Select Currency",
            values=[],  # This will be updated with available currencies
            size_hint=(None, None),size=(150,50),
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            pos_hint={'center_x': 0.35, 'center_y': 0.7}
            
        )
        self.add_widget(self.currency1_spinner)

        # Second currency selection
        self.currency2_input = TextInput(
            hint_text="Search currency",
            size_hint=(None, None),size=(150,35),
            pos_hint={'center_x': 0.65, 'center_y': 0.8},
            multiline=False
        )
        self.currency2_input.bind(text=self.update_currency2_options)
        self.add_widget(self.currency2_input)

        self.currency2_spinner = Spinner(
            text="Select Currency",
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            values=[],  # This will be updated with available currencies
            pos_hint={'center_x': 0.65, 'center_y': 0.7},
            size_hint=(None, None),size=(150,50),
        )
        self.add_widget(self.currency2_spinner)


        self.back_button = Button(
            text="Back",
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            size_hint=(None, None), size=(150, 50),
            pos_hint={'center_x': 0.1, 'center_y': 0.9}
        )
        self.back_button.bind(on_press=self.on_back_button_press)
        self.add_widget(self.back_button)

        # Fetch initial exchange rates to populate spinners
        self.all_rates = self.fetch_initial_exchange_rates()
        self.update_currency1_options()
        self.update_currency2_options()



    def fetch_initial_exchange_rates(self):
        try:
            data = fetch_exchange_rates(API_KEY)
            return data.get('conversion_rates', {}).keys()
        except requests.RequestException as e:
            return []

    def update_currency1_options(self, instance=None, value=''):
        search_query = value.upper()
        filtered_currencies = [currency for currency in self.all_rates if search_query in currency]
        self.currency1_spinner.values = filtered_currencies

    def update_currency2_options(self, instance=None, value=''):
        search_query = value.upper()
        filtered_currencies = [currency for currency in self.all_rates if search_query in currency]
        self.currency2_spinner.values = filtered_currencies

    def on_back_button_press(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'start_menu'