# -*- coding: utf-8 -*-
"""Gbm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11FF8ZsQ2ZMkv3lUoWxE8B_rFCA5tDy8j
"""

class Gbm:
    def __init__(self,
                 init_state = 100.,
                 drift_ratio = .0475,
                 vol_ratio = .2
                ):
        self.init_state = init_state
        self.drift_ratio = drift_ratio
        self.vol_ratio = vol_ratio