#!/usr/bin/env python3

import os
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from model.get_exchange_rate_data import fetch_exchange_rates
from kivy.uix.widget import Widget

current_dir = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(current_dir, "Image Resources/background1.jpg" )

API_KEY = 'cb0c995beeb4118248dd2566'




class ExchangeMenu(FloatLayout):
    def __init__(self, **kwargs):
        super(ExchangeMenu, self).__init__(**kwargs)

        self.background = Image(source=image_path, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Example content for the new menu
        self.add_widget(Label(
            text="Currency Converter", font_size='24sp',
            color=(24/255, 198/255, 128/255, 1),
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 1}
        ))

        # Create a ScrollView
        self.scroll_view = ScrollView(size_hint=(0.9, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                      do_scroll_x=False, do_scroll_y=True)
        
        # Create a BoxLayout to hold the exchange rate labels
        self.box_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        self.box_layout.bind(minimum_height=self.box_layout.setter('height'))

        # Fetch and display exchange rates
        self.update_exchange_rates()

        # Add BoxLayout to ScrollView
        self.scroll_view.add_widget(self.box_layout)
        self.add_widget(self.scroll_view)

        self.back_button = Button(
            text="Back",
            background_color=(24/255, 198/255, 128/255, 1),
            color=(166/255, 227/255, 237/255, 1),
            size_hint=(None, None), size=(150, 50),
            pos_hint={'center_x': 0.1, 'center_y': 0.9}
        )
        self.back_button.bind(on_press=self.on_back_button_press)
        self.add_widget(self.back_button)
        
    def update_exchange_rates(self):
        try:
            data = fetch_exchange_rates(API_KEY)  # Use the function to get data
            rates = data.get('conversion_rates', {})

            # Clear previous entries
            self.box_layout.clear_widgets()

            # Add new exchange rate items with styling
            for currency, rate in rates.items():
                rate_box = BoxLayout(size_hint_y=None, height=50, padding=10, spacing=10)

                # Apply canvas instructions for each BoxLayout
                with rate_box.canvas.before:
                    Color(0.1, 0.1, 0.1, 0.3)  # Background color
                    self.rect = Rectangle(size=rate_box.size, pos=rate_box.pos)
                rate_box.bind(size=self._update_rect, pos=self._update_rect)

                rate_label = Label(
                    text=f"{currency}: {rate:.2f}",
                    size_hint=(1, 1),
                    color=(1, 1, 1, 1)  # White color for text
                )
                rate_label.size_hint = (1, 1)
                rate_box.add_widget(rate_label)
                self.box_layout.add_widget(rate_box)
        except requests.RequestException as e:
            # Handle request errors here
            error_label = Label(
                text=f"Error fetching rates: {e}",
                size_hint_y=None, height=40,
                color=(1, 0, 0, 1)  # Red color for errors
            )
            self.box_layout.add_widget(error_label)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_back_button_press(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'start_menu'