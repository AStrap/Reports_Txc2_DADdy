# -*- coding: utf-8 -*-
import datetime

# Le date sono considerati nel formato:
# '%Y-%m-%dT%H:%M:%S.%f'
# '%Y-%m-%dT%H:%M:%S'
# '%Y-%m-%d'
#
# Solo nella stampa potrebbe essere presente un cambiamento nel ordine

"""
    Conversione stringa - data
    
    Parametri:
        date: string - YYYY-MM-DD (o formato sopra indicati)
            data da convertire
        
    Return:
        r_date: datetime.datetime
            data come oggetto del modulo datetime
             
"""
def get_datetime(date):
    date_format_cent = '%Y-%m-%dT%H:%M:%S.%f'
    date_format_no_cent = '%Y-%m-%dT%H:%M:%S'
    date_format_no_hour = '%Y-%m-%d'
    r_date = ""
    try:
        r_date = datetime.datetime.strptime(date, date_format_cent)
    except:
        try:
            r_date = datetime.datetime.strptime(date, date_format_no_cent)
        except:
            r_date = datetime.datetime.strptime(date, date_format_no_hour)
        
    return r_date

"""
    Conversione secondi - orario 
    
    Parametri:
        secondi: int
        
    Return:
        orario: string
            orario in formato HH:MM:SS
"""
def seconds_hours(seconds):
    
    r_hours = datetime.timedelta(seconds=seconds)
        
    return str(r_hours)

"""
    Confronto tra due date
    
    Parametri:
        date1: string - YYYY-MM-DD (o formato sopra indicati)
            prima data da confrontare
        date2: string - YYYY-MM-DD (o formato sopra indicati)
            seconda data da confrontare
            
    Return:
        0  se date uguali
        1  se la prima data è più grande della seconda
        -1 se la seconda data è più grande della prima
             
"""
def cmp_dates(date1, date2):
    date1 = get_datetime(date1)
    date2 = get_datetime(date2)
    
    r = 0
    if date1 < date2:
        r = -1
    elif date1 > date2:
        r = 1
       
    return r 

"""
    Incrementa data di x giorni
    
    Parametri:
        date: string - YYYY-MM-DD
            data da incrementare
        n_days: int 
            numero giorni da sommare
            
    Return:
        r_date: string
            data aggiornata
             
"""
def add_days(date, n_days):
    r_date = get_datetime(date)
    
    r_date = r_date + datetime.timedelta(days=n_days)
    
    return str(r_date)[:10]
    
"""
    Calcolo giorni dato il periodo
    
    Parametri:
        date_range_study: (string - string) (YYYY-MM-DD - YYYY-MM-DD)
            periodo di tempo  
            
    Return:
        r_days: list(string)
            lista giorni compresi nel periodo
             
"""
def get_days_by_period(period):
    r_days = list()
    date_s = get_datetime(period[0])
    date_e = get_datetime(period[1])
    
    while date_s <= date_e:
        r_days.append(str(date_s)[:10])
        date_s = date_s + datetime.timedelta(days=1)
    
    return r_days
    

