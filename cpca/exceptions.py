# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 18:55:58 2018
自定义的一些异常类
@author: 燃烧杯
"""

class CPCAException(Exception):
    pass

class PlaceTypeNotExistException(CPCAException):
    pass

class InputTypeNotSuportException(CPCAException):
    input_type = \
"""
输入应该为
|省     |市    |区     |
|江苏省 |扬州市 |邗江区 |
格式的pandas.core.frame.DateFrame
"""
    pass