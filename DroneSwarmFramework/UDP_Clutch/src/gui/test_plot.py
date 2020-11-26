import context

import HRI_communication as comm
import HRI_mapping as mapp
import matplotlib.pyplot as plt

mapp_dict = comm._import_mapping()

ax = mapp_dict['_debug']['plot_regression']

a = 1