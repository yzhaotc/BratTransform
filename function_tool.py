# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 15:04:58 2019

@author: yzhao
"""

'This is a Toolbox of useful function'

'------No.1 DataFrame to Nexted Dic'
'source'
'https://stackoverflow.com/questions/19798112/convert-pandas-dataframe-to-a-nested-dict'
def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.ix[:,1:]) for k,g in grouped}
    return d