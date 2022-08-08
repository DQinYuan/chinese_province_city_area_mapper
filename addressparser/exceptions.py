# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description:
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
