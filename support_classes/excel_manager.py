# -*- coding: utf-8 -*-
import xlsxwriter
import os

class Excel_manager:

    def __init__(self):
        # cursori: x riga - y colonna
        self.c_x = 0
        self.c_y = 0

        return

    #- GESTIONE FILE ----------------------------------------------------------
    """
        Settaggio file excel di lavoro

        Parametri:
            workbook: string
                nome file excel da creare
    """
    def set_workbook(self, workbook, path_output):
        os.chdir(path_output)
        self.workbook = xlsxwriter.Workbook(workbook)
        return

    """
        Chiusura file excel di lavoro corrente
    """
    def close_workbook(self):
        self.workbook.close()
        return

    #- GESTIONE FOGLI ---------------------------------------------------------

    """
        Creazione di un foglio excel

        Parametri:
            worksheet: string
                nome foglio excel da creare
    """
    def add_worksheet(self, worksheet):
        self.worksheet = self.workbook.add_worksheet(worksheet)
        self.c_x = 0
        self.c_y = 0
        # per auto gestione larghezza colonne
        self.size_columns=dict()
        return

    """
        Creazione di un foglio excel, impostando il foglio precedente come
        nascosto, data la natura di supporto del foglio precedentemente
        impostato

        Parametri:
            worksheet: string
                nome foglio excel da creare
    """
    def add_worksheet_support_sheet(self, worksheet):
        support_sheet = self.worksheet
        self.worksheet = self.workbook.add_worksheet(worksheet)
        self.c_x = 0
        self.c_y = 0
        self.worksheet.activate()
        support_sheet.hide()

        # per auto gestione larghezza colonne
        self.size_columns=dict()
        return

    #- GESTIONE CURSORI -------------------------------------------------------

    """
        Return posizione corrente dei cursori
    """
    def get_cursors(self):
        return self.c_x, self.c_y


    """
        Modifica posizione dei cursori

        Parametri:
            c_x: int
                posizione cursore riga

            c_y: int
                posizione cursore colonna
    """
    def set_cursors(self, c_x, c_y):
        self.c_x = c_x
        self.c_y = c_y
        return

    """
        Spostamento cursore x di n_x righe
    """
    def add_row(self, n_x):
        self.c_x += n_x
        return

    """
        Spostamento cursore x di n_y colonne
    """
    def add_col(self, n_y):
        self.c_y += n_y
        return

    """
        Scrittura di una cella

        Parametri:
            x: int
                indice riga
            y: int
                indice colonna
            value: string
                valore da scrivere
            cell_format: dict
                dizionario formato come indicato da xlsxwriter
    """
    def write_cell(self, x, y, value, cell_format):
        cell = "%s%d" %(self.colnum_string(y+1), x+1)
        cell_format = self.workbook.add_format(cell_format)
        self.worksheet.write(cell, value, cell_format)
        return


    #- TABELLA ----------------------------------------------------------------
    """
        Scrittura parte testa della tabella

        Parametri:
            data: list(list())
                dati da scrivere
    """
    def write_head_table(self, data):
        #-- colonna di partenza
        y_i = self.c_y
        #--
        
        #-- scrittura celle
        cell_format = self.workbook.add_format({'bold': True, 'align':'center', 'top': 2, 'left': 2, 'bottom': 2, 'right': 2})
        for row in data:
            for d in row:
                self.worksheet.write(self.c_x, self.c_y, d, cell_format)
                self.update_size_column(d, len(str(d))+5)
                self.c_y+=1
            self.c_y = y_i; self.c_x+=1
        #--

        return

    """
        Scrittura parte corpo della tabella

        Parametri:
            data: list(list())
                dati da scrivere
    """
    def write_body_table(self, data):
        #--colonna di partenza
        y_i = self.c_y
        #--

        #-- lista celle da formattare, divisione per top, left, bottom, right
        cells={"top":list(), "left":list(), "bottom":list(), "right":list()}
        cells_values={"top":list(), "left":list(), "bottom":list(), "right":list()}
        for i,row in enumerate(data):
            for j,value in enumerate(row):
                if i==0:
                    cells["top"].append("%s%d" %(self.colnum_string(self.c_y+j+1), self.c_x+i+1))
                    cells_values["top"].append(value)
                elif i==len(data)-1:
                    cells["bottom"].append("%s%d" %(self.colnum_string(self.c_y+j+1), self.c_x+i+1))
                    cells_values["bottom"].append(value)
                else:
                    if j==0:
                        cells["left"].append("%s%d" %(self.colnum_string(self.c_y+j+1), self.c_x+i+1))
                        cells_values["left"].append(value)
                    elif j==len(row)-1:
                        cells["right"].append("%s%d" %(self.colnum_string(self.c_y+j+1), self.c_x+i+1))
                        cells_values["right"].append(value)
        #--

        #-- scrittura celle
        for row in data:
            for d in row:
                self.worksheet.write(self.c_x, self.c_y, d)
                self.update_size_column(d, len(str(d))+1)
                self.c_y+=1
            self.c_y = y_i; self.c_x+=1
        #--

        #-- formattazione celle nei bordi
        if len(cells["bottom"])>1:
            #angoli
            cell_format = self.workbook.add_format({'top': 2, 'left': 2})
            self.worksheet.write(cells["top"][0], cells_values["top"][0], cell_format)
            cell_format = self.workbook.add_format({'top': 2, 'right': 2})
            self.worksheet.write(cells["top"][-1], cells_values["top"][-1], cell_format)
            cell_format = self.workbook.add_format({'left': 2, 'bottom': 2})
            self.worksheet.write(cells["bottom"][0], cells_values["bottom"][0], cell_format)
            cell_format = self.workbook.add_format({'bottom': 2, 'right': 2})
            self.worksheet.write(cells["bottom"][-1], cells_values["bottom"][-1], cell_format)
            del cells["top"][0]; del cells["top"][-1]
            del cells["bottom"][0]; del cells["bottom"][-1]
            del cells_values["top"][0]; del cells_values["top"][-1]
            del cells_values["bottom"][0]; del cells_values["bottom"][-1]

            #bordi
            cell_format = self.workbook.add_format({'top': 2})
            for i,cell in enumerate(cells["top"]):
                self.worksheet.write(cell, cells_values["top"][i], cell_format)
            cell_format = self.workbook.add_format({'left': 2})
            for i,cell in enumerate(cells["left"]):
                self.worksheet.write(cell, cells_values["left"][i], cell_format)
            cell_format = self.workbook.add_format({'bottom': 2})
            for i,cell in enumerate(cells["bottom"]):
                self.worksheet.write(cell, cells_values["bottom"][i], cell_format)
            cell_format = self.workbook.add_format({'right': 2})
            for i,cell in enumerate(cells["right"]):
                self.worksheet.write(cell, cells_values["right"][i], cell_format)

        elif len(cells["top"])>1:
            #angoli
            cell_format = self.workbook.add_format({'top': 2, 'left': 2, 'bottom': 2})
            self.worksheet.write(cells["top"][0], cells_values["top"][0], cell_format)
            cell_format = self.workbook.add_format({'top': 2, 'bottom': 2, 'right': 2})
            self.worksheet.write(cells["top"][-1], cells_values["top"][-1], cell_format)
            del cells["top"][0]; del cells["top"][-1]
            del cells_values["top"][0]; del cells_values["top"][-1]

            #bordi
            cell_format = self.workbook.add_format({'top': 2, 'bottom':2})
            for i,cell in enumerate(cells["top"]):
                self.worksheet.write(cell, cells_values["top"][i], cell_format)

        elif len(cells["bottom"])==1:
            #angoli
            cell_format = self.workbook.add_format({'top': 2, 'left': 2, 'right':2})
            self.worksheet.write(cells["top"][0], cells_values["top"][0], cell_format)
            cell_format = self.workbook.add_format({'top': 2, 'right': 2, 'bottom':2})
            self.worksheet.write(cells["bottom"][0], cells_values["bottom"][0], cell_format)

            #lati
            cell_format = self.workbook.add_format({'left': 2, 'right':2})
            for i,cell in enumerate(cells["left"]):
                self.worksheet.write(cell, cells_values["left"][i], cell_format)
        elif len(cells["top"])==1:
            cell_format = self.workbook.add_format({'top': 2, 'left': 2, 'bottom': 2, 'right':2})
            self.worksheet.write(cells["top"][0], cells_values["top"][0], cell_format)
        #--
        
        return

    """
        Funzione che unisce un gruppo di celle

        Parametri:
            x: (int, int)
                riga iniziale, riga finale da considerare

            y: (int, int)
                colonna iniziale, colonna finale da considerare

            value: string
                valore da scrivere

            cell_format: dict()
                formato secondo modulo xlsxwriter
    """
    def merge_cells(self, x, y, value, cell_format):
        c_x_i = self.c_x; c_y_i = self.c_y
        self.c_x = x[0]; self.c_y = y[0]
        if y[0]==y[1]:
            self.update_size_column(value, len(str(value))+4)

        cell_format = self.workbook.add_format(cell_format)
        c_s = "%s%d" %(self.colnum_string(y[0]+1),x[0]+1)
        c_e = "%s%d" %(self.colnum_string(y[1]+1),x[1]+1)

        self.worksheet.merge_range('%s:%s'%(c_s,c_e), value, cell_format)
        self.c_x = c_x_i; self.c_y = c_y_i
        return

    """
        Inserimento formattazione condizionale

        Parametri:
            x: (int, int)
              riga iniziale, riga finale da considerare

            y: (int, int)
                colonna iniziale, colonna finale da considerare

            criteria: string
                criterio come considerati dal modulo xlsxwriter

            value: string
                valore da scrivere

            cell_format: dict()
                formato in caso di condizione vera
    """
    def conditional_format_cells(self, x, y, criteria, value, cell_format):
        c_s = "%s%d" %(self.colnum_string(y[0]+1),x[0]+1)
        c_e = "%s%d" %(self.colnum_string(y[1]+1),x[1]+1)

        cell_format = self.workbook.add_format(cell_format)

        self.worksheet.conditional_format( '%s:%s'%(c_s,c_e), {'type':'cell',
                                                                'criteria': criteria,
                                                                'value': value,
                                                                'format': cell_format})

        return

    #- GRAFICI ----------------------------------------------------------------
    """
        Stampa di un grafico a linee

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e riga dati, y indica range colonne valori
              vert : y indica colanna label e colonna dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            label_x: string
                label asse x
                
            label_y: string
                label asse y
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
            axis_y_option: dict()
                opzioni aggiuntive per l'asse y
        Return:

    """
    def print_line_chart(self, orient, x, y, support_sheet, title, label_x, label_y, p_x, p_y, axis_y_option):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'line'})

        #-- differenza a seconda dell'orientamento dei dati
        if orient == "oriz":
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[0]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[1]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-
        else:
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[0]+1),x[1]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[1]+1),x[0]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-

        #- creazione serie
        chart.add_series({
            'name':'Serie',
            'categories': '=%s!%s:%s' %(support_sheet, labels_s, labels_e),
            'values':     '=%s!%s:%s' %(support_sheet, values_s, values_e),
            'line':       {'color': 'green'}})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        chart.set_x_axis({'name': label_x,
                          'display_units_visible': False,
                          'position_axis': 'on_tick',
                          'num_font':  {'rotation': 90},
                          'major_gridlines': {
                                  'visible': True,
                                  'line': {'width': 0.25}}})
        
        options_y = {'name':label_y}
        options_y.update(axis_y_option)
        chart.set_y_axis(options_y)
        
        chart.set_legend({'none': True})
        chart.set_size({'width': 1000, 'height': 227})

        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    """
        Stampa di un grafico a torte

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e riga dati, y indica range colonne valori
              vert : y indica colanna label e colonna dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
        Return:

    """
    def print_pie_chart(self, orient, x, y, support_sheet, title, p_x, p_y):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'pie'})

        #-- differenza a seconda dell'orientamento dei dati
        if orient == "oriz":
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[0]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[1]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-
        else:
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[0]+1),x[1]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[1]+1),x[0]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-

        #- creazione serie
        chart.add_series({
            'name':'Serie',
            'categories': '=%s!%s:%s' %(support_sheet, labels_s, labels_e),
            'values':     '=%s!%s:%s' %(support_sheet, values_s, values_e)})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        chart.set_size({'width': 577, 'height': 227})

        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    """
        Stampa di un grafico a colonne

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e riga dati, y indica range colonne valori
              vert : y indica colanna label e colonna dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            label_x: string
                label asse x
                
            label_y: string
                label asse y
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
            axis_y_option: dict()
                opzioni aggiuntive per l'asse y
        Return:

    """
    def print_column_chart(self, orient, x, y, support_sheet, title, label_x, label_y, p_x, p_y, axis_y_option):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'column'})

        #-- differenza a seconda dell'orientamento dei dati
        if orient == "oriz":
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[0]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[1]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-
        else:
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[0]+1),x[1]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[1]+1),x[0]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-

        #- creazione serie
        chart.add_series({
            'name':'Serie',
            'categories': '=%s!%s:%s' %(support_sheet, labels_s, labels_e),
            'values':     '=%s!%s:%s' %(support_sheet, values_s, values_e)})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        chart.set_x_axis({'name': label_x, 'display_units_visible': False, 'position_axis': 'on_tick', 'major_gridlines': {
                'visible': True,
                'line': {'width': 0.25}} })
        
        options_y = {'name':label_y}
        options_y.update(axis_y_option)
        chart.set_y_axis(options_y)
        
        chart.set_legend({'none': True})
        chart.set_size({'width': 1000, 'height': 227})

        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    """
        Stampa di un grafico a istogramma

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e riga dati, y indica range colonne valori
              vert : y indica colanna label e colonna dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            label_x: string
                label asse x
                
            label_y: string
                label asse y
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
            axis_y_option: dict()
                opzioni aggiuntive per l'asse y
        Return:

    """
    def print_isto_chart(self, orient, x, y, support_sheet, title, label_x, label_y, p_x, p_y, axis_y_option):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'column'})

        #-- differenza a seconda dell'orientamento dei dati
        if orient == "oriz":
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[0]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[1]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-
        else:
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[0]+1),x[1]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[1]+1),x[0]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-

        #- creazione serie
        chart.add_series({
            'name':'Serie',
            'categories': '=%s!%s:%s' %(support_sheet, labels_s, labels_e),
            'values':     '=%s!%s:%s' %(support_sheet, values_s, values_e),
            'line':       {'color': 'white'},
            'gap':        0})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        chart.set_x_axis({'name': label_x})
        
        options_y = {'name':label_y}
        options_y.update(axis_y_option)
        chart.set_y_axis(options_y)
        
        chart.set_legend({'none': True})
        chart.set_size({'width': 1000, 'height': 227})

        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    """
        Stampa di un grafico a barre

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e riga dati, y indica range colonne valori
              vert : y indica colanna label e colonna dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            label_x: string
                label asse x
                
            label_y: string
                label asse y
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
        Return:

    """
    def print_bar_chart(self, orient, x, y, support_sheet, title, label_x, label_y, p_x, p_y, axis_x_option):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'bar'})

        #-- differenza a seconda dell'orientamento dei dati
        if orient == "oriz":
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[0]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[1]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-
        else:
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[0]+1),x[1]+1)
            values_s = "$%s$%d"%(self.colnum_string(y[1]+1),x[0]+1); values_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[1]+1)
            #-

        #- creazione serie
        chart.add_series({
            'name':'Serie',
            'categories': '=%s!%s:%s' %(support_sheet, labels_s, labels_e),
            'values':     '=%s!%s:%s' %(support_sheet, values_s, values_e)})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        
        options_x = {'name':label_y,
                     'display_units_visible': False,
                     'position_axis': 'on_tick'}
        options_x.update(axis_x_option)
        chart.set_x_axis(options_x)
        
        

        chart.set_y_axis({'name': label_y, 'reverse': True})
        chart.set_legend({'none': True})
        chart.set_size({'width': 577, 'height': 1000})

        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    #- GRAFICI MULTIPLE SERIE -------------------------------------------------

    """
        Stampa a linee colonne multiple

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e righe serie dei dati, y indica range colonne valori
              vert : y indica colanna label e colonne serie dei dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            label_x: string
                label asse x
                
            label_y: string
                label asse y
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
            axis_y_option: dict()
                opzioni aggiuntive per l'asse y
    """
    def print_column_chart_multp(self, orient, x, y, name_series, support_sheet, title, label_x, label_y, p_x, p_y, axis_y_option):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'column'})

        #-- differenza a seconda dell'orientamento dei dati
        values_s=list(); values_e=list()
        if orient == "oriz":
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[1]+1),x[0]+1)

            for val_x in x[1:]:
                values_s.append("$%s$%d"%(self.colnum_string(y[0]+1),val_x+1)); values_e.append("$%s$%d" %(self.colnum_string(y[1]+1),val_x+1))
            #-
        else:
            #- intervalli dati da considerare (start,end)
            labels_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); labels_e = "$%s$%d" %(self.colnum_string(y[0]+1),x[1]+1)
            for val_y in y[1:]:
                values_s.append("$%s$%d"%(self.colnum_string(val_y+1),x[0]+1)); values_e.append("$%s$%d" %(self.colnum_string(val_y+1),x[1]+1))
            #-

        #- creazione serie
        for i, (val_s,val_e) in enumerate(zip(values_s, values_e)):
            chart.add_series({
                'name':name_series[i],
                'categories': '=%s!%s:%s' %(support_sheet, labels_s, labels_e),
                'values':     '=%s!%s:%s' %(support_sheet, val_s, val_e)})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        chart.set_x_axis({'name': label_x, 'display_units_visible': False, 'major_gridlines': {
                'visible': True,
                'line': {'width': 0.25}} })
        
        options_y = {'name':label_y}
        options_y.update(axis_y_option)
        chart.set_y_axis(options_y)
        
        chart.set_size({'width': 1000, 'height': 227})
        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    """
        Stampa Grafico a linee specifico per il caso di visualizzazione medie velocità
        per report

        Parametri:
            orien: "oriz" o "vert"
              indica l'orientamento dei dati e il significato x,y
              oriz : x indica riga label e righe serie dei dati, y indica range colonne valori
              vert : y indica colanna label e colonne serie dei dati, x indica range righe valori

            x: (int, int)
                (riga iniziale, riga finale)

            y: (int, int)
                (colonna iniziale, colonna finale)

            support_sheet: string
                nome foglio da cui prendere i dati
                
            title: string
                titolo grafico
                
            label_x: string
                label asse x
                
            label_y: string
                label asse y
                
            p_x: int
                indice riga dove posizionare il grafico
                
            p_y: int
                indice colonna dove posizionare il grafico
                
            axis_y_option: dict()
                opzioni aggiuntive per l'asse y
    """
    def print_line_chart_speed(self, x, y, support_sheet, title, label_x, label_y, p_x, p_y, axis_y_option):

        # creazione grafico
        chart = self.workbook.add_chart({'type': 'line'})
        label_s = "$%s$%d"%(self.colnum_string(y[0]+1),x[0]+1); label_e = "$%s$%d"%(self.colnum_string(y[1]+1),x[0]+1)
        values_s = list(); values_e = list()
        for y_s, y_e in y[2:]:
            values_s.append("$%s$%d"%(self.colnum_string(y_s+1),x[1]+1))
            values_e.append("$%s$%d"%(self.colnum_string(y_e+1),x[1]+1))

        #- creazione serie
        for i, (val_s,val_e) in enumerate(zip(values_s, values_e)):
            chart.add_series({
                'name': 'serie',
                'categories': '=%s!%s:%s' %(support_sheet, label_s, label_e),
                'values':     '=%s!%s:%s' %(support_sheet, val_s, val_e),
                'line':       {'color': 'green'}})
        #-
        #--

        chart.set_title({'name': title,
                         'name_font':  {'name': 'Arial', 'size': 9}})
        chart.set_x_axis({'name': label_x,
                          'display_units_visible': False,
                          'position_axis': 'on_tick',
                          'num_font':  {'rotation': 90},
                          'major_gridlines': {
                                  'visible': True,
                                  'line': {'width': 0.25}}})
        
        options_y = {'name':label_y}
        options_y.update(axis_y_option)
        chart.set_y_axis(options_y)
        
        chart.set_size({'width': 1000, 'height': 227})
        chart.set_legend({'none': True})
        #-- salvataggio grafico
        self.worksheet.insert_chart("$%s$%d"%(self.colnum_string(p_y+1),p_x+1), chart)
        #--
        return

    #--------------------------------------------------------------------------
    """
        Funzione per auto-fittare la dimensione delle colonne
        
        Parametri:
            value: string
                valore presente nella cella
                
            size: int
                dimensione cella da impostare
    """
    def update_size_column(self, value, size):
        if not self.c_y in self.size_columns.keys():
            self.size_columns[self.c_y]=0

        if size>self.size_columns[self.c_y]:
            self.worksheet.set_column("%s:%s"%(self.colnum_string(self.c_y+1),self.colnum_string(self.c_y+1)), size)
            self.worksheet.write(self.c_x, self.c_y, value)
            self.size_columns[self.c_y]=size
        return


    """
        Conversione indice numerico in indice alfabetico secondo logica excel
        1 = A
        
        Parametri:
            n: int
                indice colonna
    """
    def colnum_string(self, n):
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string
