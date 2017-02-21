#!/usr/bin/env python

import kivy
import requests
import time
import datetime
import os
import random
#import mpdclient2


CAM1 = '/var/www/static/img/cam1.jpg'
CAM = '/var/www/static/img/cam.jpg'
#MPD = mpdclient2.connect(host='www')

kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import AsyncImage

import cell

lights=cell.lights

'''

            GridLayout:
                id: light_grid
                cols: 4
                rows: 4
                size_hint_y: None
                height: dp(208)
                padding: dp(8)
                spacing: dp(16)
'''


Builder.load_string('''
<RootWidget>:
    carousel: carousel
    do_default_tab: False
    Carousel:
        on_index: root.on_index(*args)
        id: carousel 
        Button:
            on_press: root.t_start = 0
            on_release: pass
            background_color: 0, 0, 0, 1
            trigger_action: 0
            tab: background
            Image:
                source: '/var/www/static/img/cam.jpg'
                opacity: 0
                id: image_background
                nocache: True
                keep_ratio: False
                y: self.parent.y
                x: self.parent.x
                width: self.parent.width
                size: self.parent.width, self.parent.height
            Label:
                text: root.display_time
                x: 664
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time1
                color: 0,0,0
            Label:
                text: root.display_time
                color: 0.8,0.8,0.8
                text: root.display_time
                color: 0.8,0.8,0.8
                x: 660
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time2
        BoxLayout:
            orientation: 'vertical'
            tab: light_tab
            id: cam_display0
            canvas.before:
                Rectangle:
                    pos: self.pos
                    size: self.size
                    Image:
                        source: '/var/www/static/img/cam2.jpg'
                        opacity: 1
                        nocache: True
                        keep_ratio: False
                        y: self.parent.y
                        x: self.parent.x
                        width: self.parent.width
                        size: self.parent.width, self.parent.height
            GridLayout:
                id: light_grid
                cols: 4
                rows: 5
                size_hint_y: None
                height: dp(208)
                padding: dp(8)
                spacing: dp(16)

        BoxLayout:
            orientation: 'horizontal'
            height: '48dp'
            tab: sound_tab
            Slider:
                min: 0
                max: 100
                orientation: 'vertical'
                padding: 150
                on_value: root.sound_change(self.value)
                id: sound0_slider
                Label:
                    text: "Sound!" + str(sound0_slider.value)
                    x: 664
                    y: self.parent.height / 2  + 140
                    font_size: 30
                    bold: True
                    id: time5
                    color: 0,0,0

        Button:
            on_press: root.t_start = 0
            on_release: pass
            background_color: 0, 0, 0, 1
            trigger_action: 0
            tab: cam
            Image:
                source: '/var/www/static/img/cam.jpg'
                opacity: 1
                id: image_cam
                nocache: True
                keep_ratio: True
                y: self.parent.y
                x: self.parent.x
                width: self.parent.width
                size: self.parent.width, self.parent.height
            Label:
                text: root.display_time
                x: 664
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time3
                color: 0,0,0
            Label:
                text: root.display_time
                color: 0.8,0.8,0.8
                x: 660
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time4
        BoxLayout:
            orientation: 'vertical'
            height: '48dp'
            tab: news
            Image:
                source: '/var/www/static/img/cam.jpg'
                opacity: 1
                id: image_cam
                nocache: True
                keep_ratio: True
            Label:
                text: root.display_time
                x: 664
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time5
                color: 0,0,0
            Label:
                text: root.display_time
                color: 0.8,0.8,0.8
                x: 660
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time6
        BoxLayout:
            orientation: 'vertical'
            height: self.parent.height
            tab: news
            Image:
                source: '/var/www/static/img/cam1.gif'
                opacity: 1
                id: image_cam1
                nocache: True
                y: self.parent.y
                width: self.parent.width
                size: self.parent.width, self.parent.height
            Label:
                text: root.display_time
                x: 664
                y: self.parent.height / 2  + 140
                font_size: 30
                bold: True
                id: time7
                color: 0,0,0

    TabbedPanelItem: 
        id: background
        text: 'Background' 
        slide: 0
    TabbedPanelItem: 
        id: light_tab
        text: 'Light'
        slide: 1
    TabbedPanelItem:
        id: sound_tab
        text: 'Sound'
        slide: 2
    TabbedPanelItem:
        id: news
        text: 'News'
        slide: 3
    TabbedPanelItem:
        id: cam 
        text: 'Cam' 
        slide: 4
''')


class RootWidget(TabbedPanel):
    c = 0

    reload_cam = False
    fadeout = False

    display_time = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    inode = os.stat(CAM).st_ino

    fade_in = True
    fade_out = False

    cm = None

    def __init__(self, cm, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        layout = self.ids.light_grid
        self.cm = cm
        cm.talk("TOUCH:REGISTER:TOUCH")
        with layout.canvas.before:
            #Color(.2,.9,.2,1)
            #self.rect = Rectangle(size=(800,480), pos=layout.pos)
            for i in sorted(lights):
                outputControl = ToggleButton(text=i.title(), font_size=24, )
                outputControl.bind(on_press = press_callback)
                layout.add_widget(outputControl)
        Clock.schedule_interval(self.update, 0.01)
        #print(dir(self.ids.carousel))
        pass


    def sound_change(self, id):
        print(str(id))

    def on_index(self, instance, value):
        print('here!!', instance, value)
        #tab = instance.current_slide
        #if self.current_tab != tab:
        #    self.switch_to(tab)
        self.cm.talk("TOUCH:ON_INDEX:%s" % value)
        pass

    def switch_to(self, header):
        # we have to replace the functionality of the original switch_to
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header
        # set the carousel to load  the appropriate slide
        # saved in the screen attribute of the tab head
        self.cm.talk("TOUCH:SWITCH_TO:%s" % header)
        self.carousel.index = header.slide

    def on_touch_down(self, touch):
        self.cm.talk("TOUCH:ON_TOUCH_DOWN:%s" % str(type(touch)))
	if super(RootWidget, self).on_touch_down(touch):
	    return True
	if not self.collide_point(touch.x, touch.y):
	    return False
	return True

    def update(self, *args, **kwargs):
        current_time = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

        if not self.display_time == current_time:
            self.cm.talk("TOUCH:HEARTBEAT:%s" % str(time.time()))
            self.display_time = current_time

        self.ids.time1.text = current_time
        self.ids.time2.text = self.ids.time3.text = self.display_time
        self.ids.time4.text = self.display_time
        self.ids.time5.text = self.display_time
        self.ids.time6.text = self.display_time
        self.ids.time7.text = self.display_time

        if self.current_tab.text.lower() == 'background':
            self.reload_cam = False
            if self.c < 1 and not self.fadeout:
                self.c += 0.04
                self.ids.image_background.opacity = self.c
                self.t_start = time.time()
            elif not self.fadeout:
                if time.time() - self.t_start > (1 + random.random()) * 30:
                    self.fadeout = True
            if self.fadeout:
                self.c -= 0.1
                self.ids.image_background.opacity = self.c
                if self.c <= 0.0:
                    self.cm.talk("TOUCH:RELOAD_BACKGROUND")
                    self.ids.image_background.reload()
                    self.ids.image_background.opacity = self.c
                    self.fadeout = False
        if self.current_tab.text.lower() == 'cam':
            self.t_start = 0
            if not self.reload_cam:
                self.reload_cam = time.time()
                self.ids.image_cam.reload()
            if time.time() - self.reload_cam > 10:
                self.reload_cam = time.time()
                self.ids.image_cam.reload()
        if self.current_tab.text.lower() == 'light':
		self.current_tab.texture_update()

class TouchNerve(App):
    cm = None
    def __init__(self, cm):
        App.__init__(self)
        self.cm = cm

    def build(self):
       #super(RootWidget.build, self).__init__(**kwargs)
       root = RootWidget(self.cm)
       #for p in root.carousel.children:
       #    print(p, dir(p))
       return root
'''
def req(url):
    try:
        resp = requests.get(url, timeout=1)
        return resp.ok
    except:
        return False
    return False
'''

def press_callback(obj):
    light_name = obj.text.lower()
    url = lights.get(light_name).get('url')
    if lights.get(light_name) and lights.get(light_name).get('status'):
        url = url % 'on'
        response = cell.req(url)
        if response:
            lights[light_name]['status'] = not lights[light_name]['status']
    else:
        url = url % 'off'
        response = cell.req(url)
        if response:
            lights[light_name]['status'] = not lights[light_name]['status']

if __name__ == '__main__':
    cm = cell.Membrane()
    cm.start()
    cm.talk("TOUCH:BOOT")
    touch_nerve = TouchNerve(cm)
    touch_nerve.run()

'''
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
import threading
import time

Builder.load_string("""
<AnimWidget@Widget>:
    canvas:
        Color:
            rgba: 0.7, 0.3, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: 400, 30


<RootWidget>:
    cols: 1

    canvas:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size

    anim_box: anim_box
    but_1: but_1
    lab_1: lab_1
    lab_2: lab_2

    Button:
        id: but_1
        font_size: 20
        text: 'Start second thread'
        on_press: root.start_second_thread(lab_2.text)

    Label:
        id: lab_1
        font_size: 30
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'

    AnchorLayout:
        id: anim_box

    Label:
        id: lab_2
        font_size: 100
        color: 0.8, 0, 0, 1
        text: '3'
""")


class RootWidget(GridLayout):

    stop = threading.Event()

    def start_second_thread(self, l_text):
        threading.Thread(target=self.second_thread, args=(l_text,)).start()

    def second_thread(self, label_text):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        Clock.schedule_once(self.start_test, 0)

        # Do some thread blocking operations.
        time.sleep(5)
        l_text = str(int(label_text) * 3000)

        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        self.update_label_text(l_text)

        # Do some more blocking operations.
        time.sleep(2)

        # Remove some widgets and update some properties in the main thread
        # by decorating the called function with @mainthread.
        self.stop_test()

        # Start a new thread with an infinite loop and stop the current one.
        threading.Thread(target=self.infinite_loop).start()

    def start_test(self, *args):
        # Remove the button.
        self.remove_widget(self.but_1)

        # Update a widget property.
        self.lab_1.text = ('The UI remains responsive while the '
                           'second thread is running.')

        # Create and add a new widget.
        anim_bar = Factory.AnimWidget()
        self.anim_box.add_widget(anim_bar)

        # Animate the added widget.
        anim = Animation(opacity=0.3, width=100, duration=0.6)
        anim += Animation(opacity=1, width=400, duration=0.8)
        anim.repeat = True
        anim.start(anim_bar)

    @mainthread
    def update_label_text(self, new_text):
        self.lab_2.text = new_text
        self.lab_2.text = str(int(self.lab_2.text) + 1)

        self.remove_widget(self.anim_box)

    def infinite_loop(self):
        iteration = 0
        while True:
            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                return
            iteration += 1
            print('Infinite loop, iteration {}.'.format(iteration))
            time.sleep(1)


class ThreadedApp(App):
    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    ThreadedApp().run()
'''
