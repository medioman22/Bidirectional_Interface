"""
Config Example
==============

This file contains a simple example of how the use the Kivy settings classes in
a real app. It allows the user to change the caption and font_size of the label
and stores these changes.

When the user next runs the programs, their changes are restored.

"""

from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivy import FigureCanvas,\
                                                NavigationToolbar2Kivy
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure

import numpy as np

import os
import sys

import context

from settings.settings import get_settings

import HRI_communication as comm
import HRI_mapping as mapp
import utilities.HRI as HRI

from subprocess import Popen, PIPE

settings_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings', 'settings.ini')

plot_gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Plot_GUI.py')
python_interpreter = sys.executable

class HRIWidget(Widget):
    state = StringProperty()
    log = StringProperty()
    info = StringProperty()
    buttonControl = ObjectProperty()

    def __init__(self, **kwargs):
        super(HRIWidget, self).__init__(**kwargs)

        settings = get_settings()
        self.log = ''
        self.update_state(settings)
        self.update_info(settings)


    def update_state(self, settings):
        self.state = HRI.hri_state(settings)
        
        if self.state == 'PROCESSED':
            self.buttonControl.disabled = False
        else:
            self.buttonControl.disabled = True


    def update_info(self, settings):
        self.info = '{0}\n{1}\n{2}\n{3}'.format(settings['robot'], settings['subject_name'], settings['input_device'], settings['instance'])


    def acquire(self):

        comm.update_settings(get_settings())

        err = comm.run(mode = 'acquisition')

        if err==1:      # folder existing error
            self.create_popup_DataExist()

        self.update_state(get_settings())


    def control(self):

        comm.update_settings(get_settings())

        err = comm.run(mode = 'control')

        if err==1:      # folder existing error
            self.create_popup_DataExist()

        self.update_state(get_settings())


    def mapping(self):

        def import_and_test(mapping):

            unprocessed_data = {}
            motion_data = {}
            
            # import and process train data
            unprocessed_data['train'] = mapping.import_data('train')
            motion_data, motion_data_idx, motion_data_man_list, parameters, _ = mapping.process_data(motion_data_unprocessed = unprocessed_data, which_user = 'train')

            # import and process test data
            unprocessed_data['test'] = mapping.import_data('test')
            motion_data, motion_data_idx, motion_data_man_list, parameters, _ = mapping.process_data(motion_data_unprocessed = unprocessed_data, which_user = 'test', param = parameters)
            
            # dimensionality reduction
            feats, dimred, dim_red_done, motion_data = mapping.run_dimensionality_reduction(parameters, motion_data)

            # separate by maneuver
            motion_data_maneuvers, motion_data_separated = mapping.separate_datasets(unprocessed_data, motion_data, motion_data_idx)
            
            motion_data, motion_data_man_list, motion_data_idx = mapping.augment_on_reduced_data(motion_data_separated)

            # test regressors
            test_results, test_info = mapping.implement_mapping(motion_data, dim_red_done, dimred, motion_data_idx)

            return feats, parameters, test_results, test_info, mapp.get_debug_data()

        # ### FIT SETTINGS ###
        sett = get_settings()
        mapp.update_settings(sett)
        
        # plot results
        # mapp.plot_test_results(test_results)

        feats, parameters, test_results, test_info, _debug = import_and_test(mapp)

        mapping_tostore = {'features' : feats,
                        'parameters' : parameters,
                        'settings' : mapp.settings,
                        'test_results' : test_results,
                        'test_info' : test_info,
                        '_debug' : _debug}

        if sett['store_mapping']:
            # store mapping
            mapp.store(mapping_tostore)

        self.update_state(get_settings())


    def create_popup_DataExist(self):
        show = DataExist(self)

        # create popup with warning
        self.popupDataExist = Popup(title = 'Data Already Exist!', content = show, size_hint = (None, None), size = (400, 300))
        self.popupDataExist.auto_dismiss = False        # can't be closed by clicking outside the box
        self.popupDataExist.open()                      # open popup


    def close_popup_DataExist(self):
        self.popupDataExist.dismiss()


    def delete_data(self):
        sett = get_settings()
        comm.update_settings(sett)
        comm.delete_existing_data()

        self.update_state(sett)

    def plot_map(self):
        os.system('{0} {1}'.format(python_interpreter, plot_gui))


class DataExist(FloatLayout):

    def __init__(self, root, **kwargs):
        self.is_popup = True
        self.root = root
        super(DataExist, self).__init__(**kwargs)

    def dismiss_as_popup(self):
        self.root.close_popup_DataExist()

class HRIApp(App):
    def build(self):
        """
        Build and return the root widget.
        """
        self.settings_cls = SettingsWithSidebar

        root = HRIWidget()
        return root

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        # config.setdefaults('basic', {'location' : 'mac',
        #                             'subject_name' : 'pilot_02',
        #                             'input_device' : 'imu',
        #                             'robot' : 'Fixed-wing (fixed speed)',
        #                             'control_style' : 'new'})

        # config.setdefaults('mapping', {})
        # config.setdefaults('communication', {'remote_id' : 'Logitech',
        #                             'remote_gain' : 1,
        #                             'dummy_read' : False,
        #                             'control_from_dummy_data' : False,
        #                             'n_rigid_bodies_in_skeleton' : 21,
        #                             'n_data_per_rigid_body' : 8,
        #                             'n_readings' : 100,
        #                             'simulate_flag' : False})
        # config.setdefaults('IPs', {'motive' : '127.0.0.1',
        #                             'imu' : '127.0.0.1',
        #                             'unity' : '127.0.0.1',
        #                             'unity_calib' : '127.0.0.1',
        #                             'unity_info' : '127.0.0.1',
        #                             'unity_write_sk' : '127.0.0.1',
        #                             'unity_write_sk_client' : '127.0.0.1',
        #                             'unity_sk_client' : '127.0.0.1'})
        # config.setdefaults('ports', {'motive' : 9000,
        #                             'imu' :29000,
        #                             'unity' : 30011,
        #                             'unity_calib' : 30012,
        #                             'unity_info' : 30013,
        #                             'unity_write_sk' : 30000,
        #                             'unity_write_sk_client' : 26000,
        #                             'unity_sk_client' : 26000})
        # config.setdefaults('debug', {'logging_level' : 'INFO'})

        config.read(settings_file)

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # load settings from JSON files
        settings.add_json_panel('basic', self.config, 'sett_basic.json')
        settings.add_json_panel('mapping', self.config, 'sett_mapping.json')
        settings.add_json_panel('communication', self.config, 'sett_communication.json')
        settings.add_json_panel('IPs', self.config, 'sett_IPs.json')
        settings.add_json_panel('ports', self.config, 'sett_ports.json')
        settings.add_json_panel('IMU_ID', self.config, 'sett_IMU_ID.json')
        settings.add_json_panel('debug', self.config, 'sett_debug.json')

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))

        try:
            os.rename(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hri.ini'), settings_file)
        except:
            pass

        # update info
        settings = get_settings()
        self.root.update_info(settings)
        self.root.update_state(settings)

        super(HRIApp, self).close_settings(settings)


class settingsSettingsWithSidebar(SettingsWithSidebar):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSidebar etc.).

    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """
    def on_close(self):
        Logger.info("main.py: settingsSettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: settingsSettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))

    def add_kivy_panel(self):
        pass

HRIApp().run()