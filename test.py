#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.popup import Popup
import serial

# Устанавливаем размер окна
Window.size = (1024, 600)
reverse = False
wheels = False

# Загружаем стилизацию через файл kv
Builder.load_string('''
<CarControlPanel>:
    orientation: 'vertical'
    spacing: '5dp'
    padding: '10dp'
    on_parent:
        self.z = float('inf') if self.parent else 0
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'background.jpg'

    RelativeLayout:
        Button:
            text: 'Настройки'
            size_hint: None, None
            size: 150, 50
            pos_hint: {'right': 1, 'top': 1}
            on_release: root.show_settings_popup()

    Button:
        text: 'Включение фар'
        size_hint_y: None
        height: '48dp'
        background_color: 0, 0, 1, 1
        on_touch_up: root.toggle_lights()

    BoxLayout:
        orientation: 'horizontal'
        spacing: '5dp'
        size_hint_y: None
        height: '48dp'
        background_color: 0, 0, 1, 1

        Button:
            id: P
            text: 'P'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            on_touch_up: root.change_gear('P')

        Button:
            id: R
            text: 'R'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            on_touch_up: root.change_gear('R')

        Button:
            id: N
            text: 'N'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            on_touch_up: root.change_gear('N')

        Button:
            id: D
            text: 'D'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            on_touch_up: root.change_gear('D')

    BoxLayout:
        orientation: 'horizontal'
        spacing: '5dp'
        size_hint_y: None
        height: '48dp'
        background_color: 0, 0, 1, 1

        Button:
            text: 'Музыка'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            on_touch_up: root.toggle_music()

        Button:
            text: 'Активный выхлоп'
            size_hint_y: None
            height: '48dp'
            background_color: 0, 0, 1, 1
            on_touch_up: root.toggle_exhaust()

    Button:
        text: 'Дистанционное управление'
        size_hint_y: None
        height: '48dp'
        background_color: 0, 0, 1, 1
        on_touch_up: root.rc_control()

<SettingsPopup>:
    title: 'Настройки'
    size_hint: None, None
    size: 300, 200

    BoxLayout:
        orientation: 'vertical'
        padding: 20

        Button:
            text: 'Инверсия вращения колес'
            size_hint_y: None
            height: '24dp'
            on_touch_up: root.reverse_control()

        Button:
            text: 'Инверсия руля'
            size_hint_y: None
            height: '24dp'
            on_touch_up: root.reverse_wheel()

        Button:
            text: 'Закрыть'
            size_hint: None, None
            size: 100, 24
            pos_hint: {'center_x': 0.5}
            on_touch_up: root.dismiss()
''')

class SettingsPopup(Popup):
    def reverse_control(self):
        global reverse
        print('reverse= ', reverse)
        ser.write(str(reverse).encode())
        reverse = not reverse

    def reverse_wheel(self):
        global wheels
        print('reverse wheels= ', wheels)
        ser.write(('wheel'+str(wheels)).encode())
        wheels = not wheels

class CarControlPanel(BoxLayout):

    def show_settings_popup(self):
        settings_popup = SettingsPopup()
        settings_popup.open()

    def toggle_lights(self):
        # Код для управления освещением
        print('toggle_lights')

    def change_gear(self, gear):
        # Код для переключения скоростей
        print('change_gear', gear)
        data = 'change_gear' + str(gear)
        ser.write(data.encode())

    def toggle_music(self):
        # Код для управления музыкой
        print('toggle_music')
        ser.write(b'toggle_music')

    def toggle_exhaust(self):
        # Код для управления активным выхлопом
        print('toggle_exhaust')
        ser.write(b'toggle_exhaust')

    def rc_control(self):
        # Код для управления машиной дистанционно
        print(b'rc_control')

class CarControlApp(App):
    def build(self):
        return CarControlPanel()

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.write(b'hello')
    ser.flush()

    CarControlApp().run()
