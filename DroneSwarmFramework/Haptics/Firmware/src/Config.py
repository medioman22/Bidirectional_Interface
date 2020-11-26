# -*- coding: utf-8 -*-
# Author: Cyrill Lippuner
# Date: October 2018
"""
Configuration file for the Firmware of the Wearable SoftWEAR. PLEASE DO NOT CHANGE AT RUNTIME.
"""

# Pin assignments on the board
"""
             'P8_07':7, 'P8_08':8,
             'P8_09':9, 'P8_10':10, 'P8_11':11, 'P8_12':12, 'P8_14':14, 'P8_15':15,
             'P8_16':16, 'P8_17':17, 'P8_18':18, 'P8_27':27, 'P8_28':28,
             'P8_29':29, 'P8_30':30, 'P8_31':31, 'P8_32':32, 'P8_33':33, 'P8_35':35,
             'P8_39':39, 'P8_40':40, 'P8_41':41, 'P8_42':42, 'P8_43':43, 'P8_44':44,
             'P8_45':45, 'P8_46':46,
             'P9_12':58, 'P9_14':60, 'P9_15':61, 'P9_16':62, 'P9_23':69, 'P9_25':71,
             'P9_27':73, 'P9_41':87
"""

# Layout configuration
LAYOUT = "DevLayout"

PIN_MAP = {
    "MUX": {
        "A": "P8_41",
        "B": "P8_42",
        "C": "P8_43",
        "DETECT": "P8_44"
    },
    "INPUT": [
#        {
#            "DATA": "P8_40",
#            "MUX": "P8_39"
#        }
    ],
    "OUTPUT": [
        # {
        #     "DATA": "USR0"
        # },
        # {
        #     "DATA": "USR1"
        # },
        # {
        #     "DATA": "USR2"
        # },
        # {
        #     "DATA": "USR3"
        # },
#        {
#            "DATA": "P9_16"
#        },
        # {
        #     "DATA": "P9_115"
        # },
        # {
        #     "DATA": "P9_117"
        # },
    ],
    "PWM": [
#        {
#            "DATA": "P9_14"
#        },
    ],
    "ADC": [
#        {
#            "DATA": "P9_39",
#            "MUX": "P9_41"
#        },
#        {
#            "DATA": "P9_40",
#            "MUX": None
#        },
        # {
        #     "DATA": "P9_33",
        #     "MUX": None
        # },
        # {
        #     "DATA": "P9_35",
        #     "MUX": None
        # },
        # {
        #     "DATA": "P9_36",
        #     "MUX": None
        # },
        # {
        #     "DATA": "P9_37",
        #     "MUX": None
        # },
        # {
        #     "DATA": "P9_38",
        #     "MUX": None
        # }
    ],
    "I2C": [
        {
            "CHANNEL": "1"
        }
    ]

}
