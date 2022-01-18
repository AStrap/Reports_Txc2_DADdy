# -*- coding: utf-8 -*-

import support_classes.data_manager as data_manager

def main():
    
    #-- data manager: gestiore dei dati
    dm = data_manager.Data_manager()
    dm.load_data()
    #--
    
    return

if __name__ == "__main__":
    main()