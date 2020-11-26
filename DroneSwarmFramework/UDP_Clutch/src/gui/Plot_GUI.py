from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivy import FigureCanvas,\
                                                NavigationToolbar2Kivy
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.button import Button

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import context

from settings.settings import get_settings

import HRI_communication as comm
import HRI_mapping as mapp
import utilities.HRI as HRI

from kivy.core.window import Window

scale = 1
Window.size = (int(1600*scale), int(900*scale))

class PlotTest(FloatLayout):

    def __init__(self, **kwargs):
        super(PlotTest, self).__init__(**kwargs)
        self.ids.destination.bind(minimum_height=self.ids.destination.setter('height'))

        mapp_dict = comm._import_mapping()

        axes = []
        axes.append(mapp_dict['_debug']['plot_regression'])

        for ax in axes:
            # matplotlib.rcParams.update({'font.size': 200})
            self.ids.destination.add_widget(FigureCanvasKivyAgg(ax))


class PlotApp(App):
    def build(self):
        """
        Build and return the root widget.
        """
        
        root = PlotTest()
        return root

if __name__ == '__main__':
    PlotApp().run()