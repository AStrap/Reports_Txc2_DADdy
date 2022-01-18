# -*- coding: utf-8 -*-
import config

class Reports_manager:

    DATA_RANGE_STUDY = config.DATE_RANGE_STUDY

    def __init__(self, dm, em):

        #-- data_manager
        self.dm = dm
        #--        
        
        #-- excel_manager
        self.em = em
        #--

        return