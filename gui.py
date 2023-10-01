#!/usr/binenv python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.popup import Popup
import serial
import threading

# Устанавливаем размер окна
Window.size = (1024, 600)
reverse = False
wheels = False
throttle = 0
angle = 0
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

    
    
    
    # Image:
    #     id: background_image
    #     source: 'background.jpg'
    #     allow_stretch: True
    #     keep_ratio: False  # Отключаем сохранение пропорций фона
    #     pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Позиционируем по центру
    RelativeLayout:          
        Button:
            text: 'Настройки'
            # background_normal: 'settings_icon.png'
            # background_down: 'settings_icon.png'
            size_hint: None, None
            size: 150, 50
            pos_hint: {'right': 1, 'top': 1}
            on_release: root.show_settings_popup()
        # Image:
        #     id: speedometr
        #     source: 'pict/speedometr.png'  # Изображение по умолчанию
        #     allow_stretch: True
        #     keep_ratio: True
        #     size_hint: None, None
        #     size: '300dp', '300dp'
        #     pos_hint: {'center_x': 0.2, 'center_y': 0.5}
        #     z: 1  # Устанавливаем порядок отображения нижней картинки
        # 
        # Image:
        #     id: arrow
        #     source: 'pict/arrow_angle.png'  # Путь к верхней картинке
        #     allow_stretch: True
        #     keep_ratio: True
        #     size_hint: None, None
        #     size: '300dp', '300dp'
        #     pos_hint: {'center_x': 0.2, 'center_y': 0.5}  # Задание координат положения
        #     angle: 0  # Начальный угол поворота
        #     z: 2 # Устанавливаем порядок отображения верхней картинки
    
    Button:
        text: 'Включение фар'
        size_hint_y: None
        height: '48dp'
        on_release: root.toggle_lights()
        background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
        on_press: root.toggle_button_color(self)  # Изменение цвета при нажатии

    BoxLayout:
        orientation: 'horizontal'
        spacing: '5dp'
        size_hint_y: None
        height: '48dp'
        background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
        
        
        Button:
            id: P
            text: 'P'
            on_release: root.change_gear('P')
            on_press: root.reset_button_colors([R, N, D]);root.toggle_button_color(self)

            background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            
        Button:
            id: R
            text: 'R'
            on_release: root.change_gear('R')
            on_press: root.reset_button_colors([P, N, D]);root.toggle_button_color(self)
            background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            
        Button:
            id: N
            text: 'N'
            on_release: root.change_gear('N')
            on_press: root.reset_button_colors([R, P, D]);root.toggle_button_color(self)
            background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            
        Button:
            id: D
            text: 'D'
            on_release: root.change_gear('D')
            on_press: root.reset_button_colors([R, N, P]);root.toggle_button_color(self)
            background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            
    BoxLayout:
        orientation: 'horizontal'
        spacing: '5dp'
        size_hint_y: None
        height: '48dp'
        background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)

        
        Button:
            text: 'Музыка'
            size_hint_y: None
            height: '48dp'
            on_release: root.toggle_music()
            background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            on_press: root.toggle_button_color(self)  # Изменение цвета при нажатии
            
    
        Button:
            text: 'Активный выхлоп'
            size_hint_y: None
            height: '48dp'
            on_release: root.toggle_exhaust()
            background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            on_press: root.toggle_button_color(self)  # Изменение цвета при нажатии

    Button:
        text: 'Дистанционное управление'
        size_hint_y: None
        height: '48dp'
        on_release: root.rc_control()
        background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
        on_press: root.toggle_button_color(self)  # Изменение цвета при нажатии
    
<SettingsPopup>:
    title: 'Настройки'
    size_hint: None, None
    size: 300, 200

    BoxLayout:
        orientation: 'vertical'
        padding: 20

        # Label:
        #     text: 'Здесь могут быть ваши настройки'
        Button:
            text: 'Инверсия вращения колёс'
            size_hint_y: None
            height: '24dp'
            on_release: root.reverse_control()
            # background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            on_press: root.toggle_button_color(self)  # Изменение цвета при нажатии
        Button:
            text: 'Инверсия руля'
            size_hint_y: None
            height: '24dp'
            on_release: root.reverse_wheel()
            # background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
            on_press: root.toggle_button_color(self)  # Изменение цвета при нажатии
        Button:
            text: 'Закрыть'
            size_hint: None, None
            size: 100, 24
            pos_hint: {'center_x': 0.5}
            on_release: root.dismiss()
''')


class CarControlPanel(BoxLayout):

    def rotate_car_image(self, angle_degrees=20):
        print('animation')
        car_image = self.ids.arrow
        anim = Animation(angle=angle_degrees, duration=2)
        anim.start(car_image)

    def show_settings_popup(self):
        settings_popup = SettingsPopup()
        settings_popup.open()

    def reset_button_colors(self, buttons_to_reset):
        for button in buttons_to_reset:
            button.background_color = [0, 0, 1, 1]

    def toggle_button_color(self, button):
        if button.background_color == [0, 0, 1, 1]:
            button.background_color = [0, 0.6, 1, 1]
        else:
            button.background_color = [0, 0, 1, 1]

    def change_car_image(self, angle, time):
        if image_number == 1:
            car_image.source = 'car_image_1.png'  # Замените на свой путь и имя изображения
        elif image_number == 2:
            car_image.source = 'car_image_2.png'  # Замените на свой путь и имя изображения
        else:
            car_image.source = 'car_default.png'

        car_image.opacity = 1  # Делаем изображение видимым

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


class SettingsPopup(Popup):
    def reverse_control(self):
        global reverse
        print('reverse= ', reverse)
        ser.write(str(reverse).encode())
        reverse = not reverse

    def toggle_button_color(self, button):
        if button.background_color == [0.8, 0.8, 0.8, 1 ]:
            button.background_color = [0.5, 0.5, 0.5, 1 ] # Серый цвет
        else:
            button.background_color = [0.8, 0.8, 0.8, 1 ]
            
    def reverse_wheel(self):
        global wheels
        print('reverse wheels= ', wheels)
        ser.write(('wheel'+str(wheels)).encode())
        wheels = not wheels


class CarControlApp(App):
    def build(self):
        return CarControlPanel()


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.write(b'hello')
    ser.flush()
    
    CarControlApp().run()

