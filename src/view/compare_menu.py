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
from model.get_exchange_rate_data import fetch_exchange_rates, get_specific_rates
from controller import shared_variables as shared_variables

current_dir = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(current_dir, "Image Resources/background1.jpg" )

API_KEY = 'cb0c995beeb4118248dd2566'



class CompareMenu(FloatLayout):
    def __init__(self, **kwargs):
        super(CompareMenu, self).__init__(**kwargs)
        self.updating_text = False

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
        self.currency1_spinner.bind(text=self.update_selected_currency1)
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
        self.currency2_spinner.bind(text=self.update_selected_currency2)
        self.add_widget(self.currency2_spinner)

        self.selected_currency1 = ""
        self.selected_currency2 = ""

        self.currency1 = CurrencyTextInput(
            prefix = "",
            size_hint=(None, None), size=(150,35),
            disabled = False,
            background_color=(24/255, 198/255, 128/255, 1),
            hint_text_color=('#16c6db'),
            pos_hint={'center_x': 0.35, 'center_y': 0.5},
            multiline=False
        )
        self.currency1.bind(text=self.on_currency1_text_change)
        self.add_widget(self.currency1)

        self.currency2 = CurrencyTextInput(
            prefix = "",
            size_hint=(None, None), size=(150,35),
            disabled = False,
            background_color=(24/255, 198/255, 128/255, 1),
            hint_text_color=('#16c6db'),
            pos_hint={'center_x': 0.65, 'center_y': 0.5},
            multiline=False
        )
        self.add_widget(self.currency2)


        self.add_label = Label(
            text="Exchange rate", font_size='24sp',
            color=(24/255, 198/255, 128/255, 1),
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.38}
        )
        self.add_widget(self.add_label)


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


    def on_currency1_text_change(self, instance, value):
        if not self.updating_text:
            shared_variables.amount = self.currency1.get_numeric_value()
            if shared_variables.selected_currency1 and shared_variables.selected_currency2 != "Select Currency" and shared_variables.amount != "":
                self.rate = self.fetch_selected_exchange_rates()
                self.currency2.text = f"{self.currency2.prefix}{str(self.rate)}"



    def update_selected_currency1(self, instance=None, value=''):
        shared_variables.selected_currency1 = self.currency1_spinner.text
        
        if shared_variables.selected_currency1 != "Select Currency":
            self.updating_text = True
            self.currency1.prefix = shared_variables.selected_currency1 + " "
            self.currency1.text = f"{self.currency1.prefix}{shared_variables.amount}"
            if shared_variables.selected_currency1 and shared_variables.selected_currency2 != "Select Currency" and shared_variables.amount != "":
                self.rate = self.fetch_selected_exchange_rates()
                self.currency2.text = f"{self.currency2.prefix}{str(self.rate)}"
            self.updating_text = False
        

    def update_selected_currency2(self, instance=None, value=''):
        shared_variables.selected_currency2 = self.currency2_spinner.text
        if shared_variables.selected_currency1 and shared_variables.selected_currency2 != "Select Currency" and shared_variables.amount != "":
            self.rate = self.fetch_selected_exchange_rates()
            self.currency2.text = f"{self.currency2.prefix}{str(self.rate)}"
        
        
        if shared_variables.selected_currency2 != "Select Currency":
            self.currency2.prefix = shared_variables.selected_currency2 + " "





    def fetch_initial_exchange_rates(self):
        try:
            data = fetch_exchange_rates(API_KEY)
            return data.get('conversion_rates', {}).keys()
        except requests.RequestException as e:
            return []
        

    def fetch_selected_exchange_rates(self):
        try:
            data = get_specific_rates(API_KEY, shared_variables.selected_currency1, shared_variables.selected_currency2,shared_variables.amount)
            return data.get('conversion_result')

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
        self.updating_text = True
        shared_variables.amount = ""
        shared_variables.selected_currency1 = "Select Currency"
        shared_variables.selected_currency2 = "Select Currency"

        self.currency1_spinner.text = "Select Currency"
        self.currency2_spinner.text = "Select Currency"

        self.currency1.prefix = ""
        self.currency1.text = ""

        self.currency2.prefix = ""
        self.currency2.text = ""
        
        self.currency1_input.text = ""
        self.currency2_input.text = ""

        self.updating_text = False

        app = App.get_running_app()
        app.screen_manager.current = 'start_menu'






class CurrencyTextInput(TextInput):
    def __init__(self, prefix="", **kwargs):
        self._prefix = prefix
        super(CurrencyTextInput, self).__init__(**kwargs)
        self.text = self._prefix  # Initialize with the prefix

    def insert_text(self, substring, from_undo=False):
        if not self.text.startswith(self._prefix):
            self.text = self._prefix

        insertion_point = self.cursor_index()
        if insertion_point < len(self._prefix):
            return

        filtered_substring = ''.join([char for char in substring if char.isdigit() or char == '.'])
        new_text = self.text[:insertion_point] + filtered_substring + self.text[insertion_point:]
        self.text = new_text

    def on_text(self, instance, value):
        if not value.startswith(self._prefix):
            self.text = self._prefix

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value
        self.text = self._prefix

    def get_numeric_value(self):
        numeric_part = self.text[len(self._prefix):].strip()

        return numeric_part 


