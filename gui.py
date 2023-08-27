from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation

# Устанавливаем размер окна
Window.size = (1024, 600)

# Загружаем стилизацию через файл kv
Builder.load_string('''
<CarControlPanel>:
    orientation: 'vertical'
    spacing: '5dp'
    padding: '10dp'
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
        Image:
            id: speedometr
            source: 'pict/speedometr.png'  # Изображение по умолчанию
            allow_stretch: True
            keep_ratio: True
            size_hint: None, None
            size: '300dp', '300dp'
            pos_hint: {'center_x': 0.2, 'center_y': 0.5}
            z: 1  # Устанавливаем порядок отображения нижней картинки
    
        Image:
            id: arrow
            source: 'pict/arrow_angle.png'  # Путь к верхней картинке
            allow_stretch: True
            keep_ratio: True
            size_hint: None, None
            size: '300dp', '300dp'
            pos_hint: {'center_x': 0.2, 'center_y': 0.5}  # Задание координат положения
            angle: 0  # Начальный угол поворота
            z: 2 # Устанавливаем порядок отображения верхней картинки
    
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
        on_release: root.rotate_car_image()
        background_color: 0, 0, 1, 1  # Синий цвет (R, G, B, A)
        on_press: root.toggle_button_color(self); root.rotate_car_image()  # Изменение цвета при нажатии      
''')


class CarControlPanel(BoxLayout):
    def rotate_car_image(self, angle_degrees=20):
        print('animation')
        car_image = self.ids.arrow
        anim = Animation(angle=angle_degrees, duration=2)
        anim.start(car_image)

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

    def toggle_music(self):
        # Код для управления музыкой
        print('toggle_music')

    def toggle_exhaust(self):
        # Код для управления активным выхлопом
        print('toggle_exhaust')

    def rc_control(self):
        # Код для управления машиной дистанционно
        print('rc_control')


class CarControlApp(App):
    def build(self):
        return CarControlPanel()


if __name__ == '__main__':
    CarControlApp().run()
