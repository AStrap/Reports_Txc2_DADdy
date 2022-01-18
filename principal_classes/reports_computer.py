# -*- coding: utf-8 -*-
import os

import config
import support_classes.reports_manager as reports_manager

class Reports_computer:
    
    PATH_OUTPUT = config.PATH_OUTPUT
    
    def __init__(self, dm, em):
        
        #-- data_manager
        self.dm = dm
        #--
        
        #-- excel_manager
        self.em = em
        #--
        
        #-- report manager: elaborazione informazione per report
        self.rm = reports_manager.Reports_manager(self.dm, self.em)
        #--
        
        return
    
    """
        Calcolo e stampa del report
    """
    def compute_print(self, id_course):
        
        #-- file markdown report
        f = open("%s\\_reports\\%s-%s.md"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course)), "w")
        
        f.write("# Report per il corso %s \n" %(self.dm.get_course_name(id_course)))
        
        f.close()
        #--
        
        #-- md file to pdf
        os.chdir("%s\\_reports" %(self.PATH_OUTPUT))
        os.system('cmd /k "mdpdf \"./%s-%s.md\"" --border=12mm' %(id_course, self.dm.get_course_name(id_course)))
        os.remove("%s\\_reports\\%s-%s.md"%(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))) 
        #--
        
        return
        
