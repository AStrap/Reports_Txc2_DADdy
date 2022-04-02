import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

class Chart_printer:

    def __init__(self):
        matplotlib.use('Agg')
        return

    def print_line_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa grafico
        fig = plt.figure(figsize=(17,4))
        ax = plt.gca()
        plt.plot(x, y, color='green')
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

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    def print_isto_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa del grafico
        fig = plt.figure(figsize=(17,4))
        ax = plt.gca()
        plt.bar(x, y)
        #--

        #-- formatazione grafico
        plt.title(title, size=16, fontweight="bold")
        plt.xlabel(label_x, size=12, fontweight="bold")
        plt.ylabel(label_y, size=12, fontweight="bold")
        plt.grid(axis = 'y')

        plt.xticks(size=11, rotation=270)
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

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    def print_bar_chart(self, x, y, title, label_x, label_y, axis_x_options, path_output, name_file):

        #-- stampa del grafico
        fig = plt.figure(figsize=(12,28))
        ax = plt.gca()
        plt.barh(x, y, height=0.2)
        #--

        #-- formatazione del grafico
        plt.title(title, size=20, fontweight="bold")
        plt.xlabel(label_x, size=16, fontweight="bold")
        ax.xaxis.set_label_position('top')
        plt.ylabel(label_y, size=16, fontweight="bold")
        plt.grid(axis = 'x')

        plt.xticks(size=16)
        plt.xticks(np.arange(0, axis_x_options["max"], max(1, int(axis_x_options["max"]/10))))
        ax.xaxis.tick_top()
        plt.yticks(size=16)

        #plt.subplots_adjust(bottom=0.2, wspace=0.01)
        plt.margins(y=0)
        #--

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

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

        plt.xticks(size=10, rotation=270)
        plt.xticks(np.arange(0, len(x), max(1, int(len(x)/10))))
        plt.yticks(size=10)

        plt.subplots_adjust(bottom=0.5, wspace=0.01)
        plt.margins(x=0)
        #--

        #-- opzione dati asse y
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return

    def print_seek_chart(self, min, events, title, label_x, label_y, axis_y_options, path_output, name_file):

        #-- stampa del grafico
        fig = plt.figure(figsize=(17,4))
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

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw(); plt.clf(); plt.close("all")
        return
