import matplotlib.pyplot as plt

CM = 1/2.54

def print_line_chart(x, y, title, label_x, label_y, axis_y_options, path_output):
    #plt.subplots(figsize=(50*CM, 10.3*CM))
    fig = plt.figure(dpi=128, figsize=(17,4))
    plt.plot(x, y)
    plt.margins(x=0)
    ax = plt.gca()

    plt.title(title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)

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

    plt.savefig("%s/%s.png" %(path_output,title), bbox_inches='tight')
    #plt.show()

def print_isto_chart(x, y, title, label_x, label_y, axis_y_options, path_output):
    #plt.subplots(figsize=(50*CM, 10.3*CM))
    fig = plt.figure(dpi=128, figsize=(17,4))
    plt.bar(x, y)
    plt.margins(x=0)
    ax = plt.gca()

    plt.title(title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)

    #-- axis_y_options
    if "min" in axis_y_options.keys():
        plt.ylim(bottom=axis_y_options["min"])
    if "max" in axis_y_options.keys():
        plt.ylim(top=axis_y_options["max"])
    #--

    plt.xticks(rotation=270)
    plt.subplots_adjust(bottom=0.5, wspace=0.01)

    plt.savefig("%s/%s.png" %(path_output,title), bbox_inches='tight')
