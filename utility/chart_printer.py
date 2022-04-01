import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

class Chart_printer:

    def __init__(self):
        matplotlib.use('Agg')
        return

    def print_line_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):

        fig = plt.figure(figsize=(17,4))
        plt.plot(x, y, color='green')

        ax = plt.gca()

        plt.title(title, size=14, fontweight="bold")
        plt.xlabel(label_x, size=12, fontweight="bold")
        plt.ylabel(label_y, size=12, fontweight="bold")
        plt.grid()

        #-- axis_y_options
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        plt.xticks(size=10, rotation=270)
        plt.xticks(np.arange(0, len(x), max(1, int(len(x)/10))))
        plt.subplots_adjust(bottom=0.5, wspace=0.01)


        # every_nth = max(1, int(len(x)/10))
        # for n, label in enumerate(ax.xaxis.get_ticklabels()):
        #     if n % every_nth != 0:
        #         label.set_visible(False)

        plt.margins(x=0)

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw()
        plt.clf()
        plt.close("all")

    def print_isto_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):
        #plt.subplots(figsize=(50*CM, 10.3*CM))
        fig = plt.figure(figsize=(17,4))
        plt.bar(x, y)
        plt.margins(x=0)
        ax = plt.gca()

        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.grid(axis = 'y')

        #-- axis_y_options
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        plt.xticks(rotation=270)
        plt.subplots_adjust(bottom=0.5, wspace=0.01)

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw()
        plt.clf()
        plt.close("all")

    def print_bar_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):
        #plt.subplots(figsize=(50*CM, 10.3*CM))
        fig = plt.figure(figsize=(17,90))
        plt.barh(x, y)
        plt.margins(y=0)
        ax = plt.gca()

        plt.title(title, size = 20)
        plt.xlabel(label_x, size = 20)
        plt.ylabel(label_y, size = 20)
        plt.xticks(size = 20)
        plt.yticks(size = 20)
        plt.grid(axis = 'x')

        #-- axis_y_options
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        plt.subplots_adjust(bottom=0.5, wspace=0.01)

        every_nth = 5
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw()
        plt.clf()
        plt.close("all")

    def print_speed_chart(self, x, y, title, label_x, label_y, axis_y_options, path_output, name_file):
        fig = plt.figure(figsize=(17,4))
        for i in range(len(x[:-1])):
            plt.plot([x[i],x[i+1]], [y[i],y[i]], color='green')
        plt.margins(x=0)
        ax = plt.gca()

        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.grid()

        #-- axis_y_options
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        plt.xticks(rotation=270)
        plt.subplots_adjust(bottom=0.5, wspace=0.01)

        every_nth = 5
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw()
        plt.clf()
        plt.close("all")

    def print_seek_chart(self, min, events, title, label_x, label_y, axis_y_options, path_output, name_file):
        fig = plt.figure(figsize=(17,4))
        x = [[] for _ in range(4)]; y = [[] for _ in range(4)]
        for i in range(4):
            for j,e in enumerate(events[i]):
                if e > 0:
                    x[i].append(j)
                    y[i].append(e)
                    #if i == 0:
                        #plt.plot(x[j], e, marker='s', color='red', fillstyle='full', linestyle='None')
                    #elif i == 1:
                        #plt.plot(x[j], e, marker='o', color='green', fillstyle='full', linestyle='None')
                    #elif i == 2:
                        #plt.plot(x[j], e, marker='D', color='blue', fillstyle='full', linestyle='None')
                    #elif i == 3:
                        #plt.plot(x[j], e, marker='^', color='yellow', fillstyle='full', linestyle='None')

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
        ax = plt.gca()

        plt.title(title)
        plt.xlabel(label_x)
        plt.xlim(right=len(min)-1)
        plt.ylabel(label_y)
        plt.grid()

        #-- axis_y_options
        if "min" in axis_y_options.keys():
            plt.ylim(bottom=axis_y_options["min"])
        if "max" in axis_y_options.keys():
            plt.ylim(top=axis_y_options["max"])
        #--

        plt.subplots_adjust(bottom=0.5, wspace=0.01)

        every_nth = 5
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

        fig.savefig("%s\\%s.png" %(path_output,name_file), bbox_inches='tight')
        plt.draw()
        plt.clf()
        plt.close("all")
