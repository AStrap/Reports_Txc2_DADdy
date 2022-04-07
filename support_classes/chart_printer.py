import matplotlib
import matplotlib.pyplot as plt
import warnings
import numpy as np
import time

class Chart_printer:

    def __init__(self):
        matplotlib.use('Agg')
        warnings.filterwarnings("ignore")
        return

    """
        Stampa grafico a linee

        Parametri:
            - x: list
                valori asse x dei dati

            - y: list
                valori asse y dei dati

            - title: str
                titolo grafico

            - label_x: str
                titolo asse x

            - label_y: str
                titolo asse y

            - axis_y_options: dict()
                opzioni asse y (disponibili: min, max)

            - path_output: str
                percorso dove stampare il grafico

            - name_file: str
                nome file da salvare
    """
    def print_line_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa grafico
        fig = plt.figure(figsize=(17,4))
        ax = plt.gca()
        plt.plot(x, y, color='green', linewidth=3)
        #--

        #-- formatazione grafico
        plt.title(title, size=16, fontweight="bold")
        plt.xlabel(label_x, size=12, fontweight="bold")
        plt.ylabel(label_y, size=12, fontweight="bold")
        plt.grid()

        plt.xticks(size=11, rotation=270)
        plt.xticks(np.arange(0, len(x), max(1, int(len(x)/10))))
        plt.yticks(size=11)

        plt.subplots_adjust(bottom=0.5, wspace=0.01)
        plt.margins(x=0)
        #--

        #-- opzione dati asse y
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        fig.savefig("%s/%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    """
        Stampa grafico istogramma

        Parametri:
            - x: list
                valori asse x dei dati

            - y: list
                valori asse y dei dati

            - title: str
                titolo grafico

            - label_x: str
                titolo asse x

            - label_y: str
                titolo asse y

            - axis_y_options: dict()
                opzioni asse y (disponibili: min, max)

            - path_output: str
                percorso dove stampare il grafico

            - name_file: str
                nome file da salvare
    """
    def print_isto_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa del grafico
        fig = plt.figure(figsize=(17,4))
        ax = plt.gca()
        plt.bar(x, y, width=1, color='green', edgecolor='black')
        #--

        #-- formatazione grafico
        plt.title(title, size=16, fontweight="bold")
        plt.xlabel(label_x, size=12, fontweight="bold")
        plt.ylabel(label_y, size=12, fontweight="bold")
        plt.grid(axis = 'y')

        plt.xticks(size=11)
        plt.yticks(size=11)

        plt.subplots_adjust(bottom=0.2, wspace=0.01)
        plt.margins(x=0)
        #--

        #-- opzione dati asse y
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        fig.savefig("%s/%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    """
        Stampa grafico a barre orizzontali

        Parametri:
            - x: list
                valori asse x dei dati

            - y: list
                valori asse y dei dati

            - title: str
                titolo grafico

            - label_x: str
                titolo asse x

            - label_y: str
                titolo asse y

            - axis_x_options: dict()
                opzioni asse x (disponibili: min, max)

            - path_output: str
                percorso dove stampare il grafico

            - name_file: str
                nome file da salvare
    """
    def print_bar_chart(self, x, y, title, label_x, label_y, axis_x_options, path_output, name_file):

        #-- stampa del grafico
        if len(y)<21:
            fig = plt.figure(figsize=(8,len(y)))
            size_title = 16
            size_label = 12
        else:
            fig = plt.figure(figsize=(8,22))
            size_title = 20
            size_label = 16
        ax = plt.gca()
        plt.barh(x, y, height=0.4, color='green', edgecolor='black')
        #--

        #-- formatazione del grafico
        plt.title(title, size=size_title, fontweight="bold")
        plt.xlabel(label_x, size=size_label, fontweight="bold")
        ax.xaxis.set_label_position('top')
        plt.ylabel(label_y, size=size_label, fontweight="bold")
        plt.grid(axis = 'x')

        plt.xticks(size=12)
        if axis_x_options["max"]==0:
            plt.xticks([0,1])
        elif axis_x_options["max"]==1:
            plt.xticks([0,1,2])
        else:
            plt.xticks(np.arange(0, axis_x_options["max"], max(1, int(axis_x_options["max"]/10))))
        ax.xaxis.tick_top()
        ax.invert_yaxis()
        plt.yticks(size=size_label)
        plt.xlim(left=0)
        #plt.subplots_adjust(bottom=0.2, wspace=0.01)
        plt.margins(y=0)
        #--

        fig.savefig("%s/%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    """
        Stampa grafico a linee per lo studio della velocità di visione delle
        lezioni

        Parametri:
            - x: list
                valori asse x dei dati

            - y: list
                valori asse y dei dati

            - title: str
                titolo grafico

            - label_x: str
                titolo asse x

            - label_y: str
                titolo asse y

            - axis_y_options: dict()
                opzioni asse y (disponibili: min, max)

            - path_output: str
                percorso dove stampare il grafico

            - name_file: str
                nome file da salvare
    """
    def print_speed_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa del grafico
        fig = plt.figure(figsize=(17,4))
        ax = plt.gca()
        for i in range(len(x[:-1])):
            plt.plot([x[i],x[i+1]], [y[i],y[i]], color='green')
        #--

        #-- formattazione del grafico
        plt.title(title, size=14, fontweight="bold")
        plt.xlabel(label_x, size=12, fontweight="bold")
        plt.ylabel(label_y, size=12, fontweight="bold")
        plt.grid()

        plt.xticks(size=11, rotation=270)
        plt.xticks(np.arange(0, len(x), max(1, int(len(x)/10))))
        plt.yticks(size=11)

        plt.subplots_adjust(bottom=0.5, wspace=0.01)
        plt.margins(x=0)
        #--

        #-- opzione dati asse y
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        fig.savefig("%s/%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    """
        Stampa grafico per lo studio del numero e tipologia di eventi di
        ricerca

        Parametri:
            - min: list
                lista minutaggio asse x

            - events: [list(), list(), list(), list()]
                numero di eventi per ogni minutaggio, per ognuna delle 4
                categorie

            - title: str
                titolo grafico

            - label_x: str
                titolo asse x

            - label_y: str
                titolo asse y

            - axis_y_options: dict()
                opzioni asse y (disponibili: min, max)

            - path_output: str
                percorso dove stampare il grafico

            - name_file: str
                nome file da salvare
    """
    def print_seek_chart(self, min, events, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa del grafico
        fig = plt.figure(figsize=(17,3))
        ax = plt.gca()
        x = [[] for _ in range(4)]; y = [[] for _ in range(4)]
        for i in range(4):
            for j,e in enumerate(events[i]):
                if e > 0:
                    x[i].append(j)
                    y[i].append(e)

        for i in range(4):
            if i == 0:
                plt.plot(x[i], y[i], marker='s', color='red', fillstyle='full', linestyle='None')
            elif i == 1:
                plt.plot(x[i], y[i], marker='o', color='green', fillstyle='full', linestyle='None')
            elif i == 2:
                plt.plot(x[i], y[i], marker='D', color='blue', fillstyle='full', linestyle='None')
            elif i == 3:
                plt.plot(x[i], y[i], marker='^', color='yellow', fillstyle='full', linestyle='None')
            plt.xticks([i for i in range(len(min))], min, rotation=270)
            plt.margins(x=0)
        plt.grid()
        #--

        #-- formatazione grafico
        plt.title(title, size=16, fontweight="bold")
        plt.xlabel(label_x, size=12, fontweight="bold")
        plt.ylabel(label_y, size=12, fontweight="bold")

        plt.xticks(size=11)
        plt.xticks(np.arange(0, len(min), max(1, int(len(min)/10))))
        plt.yticks(size=11)
        plt.xlim(right=len(min)-1)

        plt.subplots_adjust(bottom=0.2, wspace=0.01)
        #--

        #-- opzione dati asse yopzione dati asse y
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        fig.savefig("%s/%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return
