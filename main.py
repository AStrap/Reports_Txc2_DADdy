# -*- coding: utf-8 -*-
import os

import principal_classes.user_info_computer as user_info_computer
import principal_classes.reports_computer as reports_computer

import config
import support_classes.data_manager as data_manager
import support_classes.excel_manager as excel_manager

PATH_OUTPUT = config.PATH_OUTPUT

def main():
    
    #-- data manager: gestiore dei dati
    dm = data_manager.Data_manager()
    dm.load_data()
    #--
    
    #-- excel manager: gestione dei fogli excel
    em = excel_manager.Excel_manager()
    #--
    
    #-- creazione cartelle output
    for c in dm.get_courses():
        try:
            os.mkdir("%s\\%s-%s" %(PATH_OUTPUT, c, dm.get_course_name(c)))
        except:
            pass
        
    try:
        os.mkdir("%s\\_reports" %(PATH_OUTPUT))
    except:
        pass
    
    try:
        os.mkdir("%s\\_users_info" %(PATH_OUTPUT))
    except:
        pass
    #--
    
    #-- stampa info utenti per ogni classe
    uc = user_info_computer.User_info_computer(dm)
    
    for id_course in dm.get_courses():
        uc.compute_save(id_course)
    #--
    
    #-- stampa report per ogni classe
    rc = reports_computer.Reports_computer(dm,em)
    
    #for id_course in dm.get_courses():
    #    rc.compute_print(id_course)
    #--
    
    return

if __name__ == "__main__":
    main()