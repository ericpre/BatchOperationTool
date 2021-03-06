# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:57:30 2015

@author: eric
"""
import sys
from qtpy import QtWidgets

from batch_operation_tool.EMS_conversion.EMS_conversion_tab import EMSConversionTab
from batch_operation_tool.EMS_conversion.operation_widget import EMSConversionWidget  
from batch_operation_tool.batch_operation_tool_ui import BatchOperationToolUI

class Test_EMSConversionWidgets:
    @classmethod
    def setup_class(self):
        self.app = QtWidgets.QApplication(sys.argv)

    @classmethod
    def teardown_class(self):
        self.app.quit()

    def setup_method(self):
        self.operation_parameters = {'extension_list':[],
                                     'data_type':'image',
                                     'log_to_linear_scale':True,
                                     'overwrite':False}
        
        self.botui = BatchOperationToolUI(load_settings=None)
        self.emsct = EMSConversionTab(self.botui.fill_tables, parent=self.botui)
        self.emscw = EMSConversionWidget(self.emsct.get_files_lists, parent=self.emsct)

    def test_set_parameters(self):
        self.emscw.set_parameters(**self.operation_parameters)
        for key in list(self.operation_parameters.keys()):
            assert self.emscw.parameters[key] == self.operation_parameters[key]

    def test_get_parameters(self):
        self.emscw.set_parameters(**self.operation_parameters)
        for key in list(self.operation_parameters.keys()):
            assert self.emscw.parameters[key] == self.operation_parameters[key]
    
    def test_convert_file(self):
        pass
    
if __name__ == '__main__':
    import pytest
    pytest.main()