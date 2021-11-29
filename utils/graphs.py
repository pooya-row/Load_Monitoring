import math

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.figure
import matplotlib.axis
import numpy as np

from matplotlib.ticker import LogFormatterSciNotation


def plot_g_exc(x: list,
               y: list,
               base: float,
               tops: np.ndarray,
               top_bins: list,
               bottoms: np.ndarray,
               bottom_bins: list,
               print_label=False,
               print_bins=False,
               save_fig=False) -> matplotlib.figure.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=120)
    plt.subplots_adjust(wspace=.27, bottom=0.15, top=.95, right=.98, left=0.1)

    sns.lineplot(ax=axes[0], x=x, y=y,
                 linewidth=0.5, color='xkcd:dark slate blue')
    sns.scatterplot(x=top_bins, y=tops,
                    ax=axes[1], color='xkcd:dark slate blue')
    sns.scatterplot(x=bottom_bins, y=bottoms,
                    ax=axes[1], marker='^', color='xkcd:dark slate blue')

    axes[1].set_yscale('log')

    axes[0].axhline(base, c='r')
    axes[1].axvline(base, c='r')

    axes[0].grid(True, linewidth=0.3, alpha=0.5)
    axes[1].grid(which='both', linewidth=0.3, alpha=0.5)

    axes[0].set_xlabel('Time (sec)', fontsize=13)
    axes[0].set_ylabel(r'$N_Z$, Vertical Acceleration @ CG $[g]$', fontsize=13)
    axes[0].set_title('Recorded Vertical Acceleration', fontsize=15)
    axes[1].set_xlabel(r'$N_Z$, Vertical Acceleration [g]', fontsize=13)
    axes[1].set_ylabel('Cumulative Exceedance Count', fontsize=13)
    axes[1].set_title('g-Exceedance Spectra', fontsize=15)

    axes[1].yaxis.set_minor_formatter(
        LogFormatterSciNotation(labelOnlyBase=False,
                                minor_thresholds=(5, 0.5)))

    if print_bins:
        axes[1].annotate(f'Tops = {[int(i) for i in tops]}\n'
                         f'Bottoms = {[int(i) for i in bottoms]}', (-1.2, 2.))

    if print_label:
        i = 0
        for x, y in zip(x, y):
            # label = "{:.2f}".format(y)

            axes[0].annotate(i,  # this is the text
                             (x, y),  # this is the point to label
                             textcoords="offset points",
                             # how to position the text
                             xytext=(0, 3),
                             # distance from text to points (x,y)
                             ha='center')  # horizontal alignment can be left,
            # right or center
            i += 1

    if save_fig:
        return plt.savefig('g_exceedance.png', dpi=300)
    else:
        return plt.show()


def g_exceedance_plot(top_counts: np.ndarray,
                      top_bins: list,
                      bottom_counts: np.ndarray,
                      bottom_bins: list,
                      ax: matplotlib.axis,
                      title: str, x_label: str, y_label: str,
                      base_g: float = 1,
                      print_label=False,
                      print_bins=False) -> matplotlib.axis:
    """
    Generate the g-exceedance plot.


    :param top_counts: array containing the counts of exceedances in each
     bin above the baseline.
    :param top_bins: list containing the bins above the baseline.
    :param bottom_counts: array containing the counts of exceedances in
     each bin below the baseline.
    :param bottom_bins: list containing the bins below the baseline.
    :param ax: where to plot the generated axes.
    :param title: title of the graph.
    :param x_label: x-axis label.
    :param y_label: y-axis label.
    :param base_g: the baseline.
    :param print_label: Should the data labels be printed?
    :param print_bins: Should the bin counts be printed on the plot?

    :return: matplotlib.axis
    """

    sns.scatterplot(x=top_bins, y=top_counts, ax=ax, marker='.',
                    color='xkcd:dark slate blue')
    sns.scatterplot(x=bottom_bins, y=bottom_counts, ax=ax, marker='.',
                    color='xkcd:dark slate blue')
    ax.axvline(base_g, c='r', linestyle='--')

    ax.set_yscale('log')
    ax.grid(which='both', linewidth=0.3, alpha=0.5)
    y_max = max(max(top_counts), max(bottom_counts))
    y_lim = 10 ** (math.ceil(math.log(y_max, 10)))
    ax.set_ylim((0.1, y_lim))

    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    ax.set_title(title, fontsize=15)

    ax.yaxis.set_minor_formatter(
        LogFormatterSciNotation(labelOnlyBase=False,
                                minor_thresholds=(7, 0.1)))

    if print_bins:
        ax.annotate(f'Resolution = {round(top_bins[1] - top_bins[0], 3)}\n'
                    f'Tops = {[int(i) for i in top_counts]}\n'
                    f'Bottoms = {[int(i) for i in bottom_counts]}',
                    ((max(top_bins) + min(bottom_bins)) / 2, 0.2), ha='center')

    if print_label:
        for x, y in zip(top_bins, top_counts):
            ax.annotate(int(y), (x, y), textcoords="offset points",
                        xytext=(5, 0), rotation=0, va='center', ha='left')
        for x, y in zip(bottom_bins, bottom_counts):
            ax.annotate(int(y), (x, y), textcoords="offset points",
                        xytext=(5, 0), rotation=0, va='center', ha='left')
    return ax


def plot_rainflow(x: list,
                  y: list,
                  ranges: list,
                  cycles: list,
                  bin_size: float,
                  print_label=False,
                  save_fig=False) -> matplotlib.figure.Figure:
    """
    This function produces two plots:
     1. the measured signal versus time;
     2. histogram of count of different loop ranges.

    :param x: time increments that the signal was recorded at
    :param y: the recorded acceleration at each time increment
    :param ranges: list of ranges of loops counted by rainflow analysis
    :param cycles: list of number of cycles counted by rainflow analysis
    :param bin_size: size of bins for histogram counts
    :param print_label: should the data labels be printed?
    :param save_fig: should the generated figure be saved?
    :return: the generated plots
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=120)
    plt.subplots_adjust(wspace=.27, bottom=0.15, top=.95, right=.98, left=0.07)

    sns.lineplot(ax=axes[0], x=x, y=y, linewidth=0.5,
                 color='xkcd:dark slate blue')
    sns.barplot(x=ranges, y=cycles, ax=axes[1], color='xkcd:dark slate blue')

    axes[1].set_yscale('log')

    axes[0].grid(True, linewidth=0.3, alpha=0.5)
    axes[1].grid(axis='y', which='both', linewidth=0.3, alpha=0.5)

    axes[0].set_xlabel('Time (sec)', fontsize=12)
    axes[0].set_ylabel(
        r'$N_Z$, Vertical Acceleration @ CG $(\dfrac{ft}{s^2})$', fontsize=12)
    axes[0].set_title('Recorded Vertical Acceleration', fontsize=15)
    axes[1].set_xlabel(r'Range Magnitude $(\dfrac{ft}{s^2})$', fontsize=12)
    axes[1].set_ylabel(r'Counts', fontsize=12)
    axes[1].set_title(f'Count of Ranges for bin size = {bin_size}',
                      fontsize=15)

    axes[1].yaxis.set_minor_formatter(
        LogFormatterSciNotation(labelOnlyBase=False,
                                minor_thresholds=(5, 0.5)))

    if print_label:
        i = 0
        for x, y in zip(x, y):
            # label = "{:.2f}".format(y)

            axes[0].annotate(i,  # this is the text
                             (x, y),  # this is the point to label
                             textcoords="offset points",
                             # how to position the text
                             xytext=(0, 0),
                             # distance from text to points (x,y)
                             ha='center')  # horizontal alignment can be left,
            # right or center
            i += 1

    if save_fig:
        return plt.savefig('rainflow.png', dpi=300)
    else:
        return plt.show()


def plot_signal(x: list,
                y: list,
                ax: matplotlib.axis,
                marker: str = '.',
                print_label=False) -> matplotlib.axis:
    """
    This function plots the signal

    :param x: time increments that the signal was recorded at
    :param y: the recorded acceleration at each time increment
    :param ax: axis name to draw the plot
    :param marker: sets the marker type of the plot
    :param print_label: should the data labels be printed?
    :return: the generated plot axis
    """
    ax.plot(x, y, marker=marker, linewidth=.5, color='xkcd:dark slate blue',
            # axes=ax,
            )
    # sns.lineplot(ax=ax, x=x, y=y, linewidth=.5, color='xkcd:dark slate blue')

    ax.grid(True, linewidth=0.3, alpha=0.5)
    ax.set_xlabel('Time (sec)', fontsize=11)
    ax.set_ylabel(r'$N_Z$, Vertical Acceleration @ CG [g]', fontsize=11)
    ax.set_title('Recorded Vertical Acceleration', fontsize=15)

    if print_label:
        i = 0
        # t = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for x_, y_ in zip(x, y):
            label = "{:.3f}".format(y_[0])
            # if y_ > 0:
            #     y_ += .25
            # else:
            #     y_ -= 1

            ax.annotate(label,  # this is the text
                        (x_[0], y_[0]),  # this is the point to label
                        textcoords="offset points",  # how to position the text
                        xytext=(0, 0),  # distance from text to points (x,y)
                        ha='center',
                        # horizontal alignment can be left, right or center
                        fontsize=6,
                        )
            i += 1

    return ax


# axes[1].ticklabel_format(axis='y', useMathText=True)

# axes[1].set_xticks([i[0] for i in cycles])
# axes[1].set_xticks(np.linspace(min(range_list), max(range_list), num_of_bins
# + 1))
# axes[1].tick_params(axis='x', direction='out')  # , labelrotation=45)
# axes[1].hist(range_list)
#
# axes[1].xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axes[1].xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
# matplotlib.ticker.NullFormatter
# sns.histplot(ax=axes[1], data=cycles, bins=num_of_bins, shrink=0.8)

def mean_range_matrix_plot(data: np.ndarray,
                           rf_matrix: np.ndarray,
                           ax: matplotlib.axis,
                           labels=False) -> matplotlib.axis:
    """
    Plot the mean-range matrix for a given mean/range tuple.

    :param data: (n x 2) array.
     First column is `means`, second column is `ranges`.
    :param rf_matrix: the matrix to be plotted
    :param ax: axis for the plot
    :param labels: should the sequential labels be printed on the graph?
    :return: generated plot
    """
    x_min, y_min = np.floor(np.amin(data[:, 0])), np.floor(np.amin(data[:, 1]))
    x_max, y_max = np.ceil(np.amax(data[:, 0])), np.ceil(np.amax(data[:, 1]))
    resolution = len(rf_matrix) + 1
    x_bins = np.linspace(x_min, x_max, resolution)
    y_bins = np.linspace(y_min, y_max, resolution)
    x_bin_size = abs(x_max - x_min) / (resolution - 1)
    y_bin_size = abs(y_max - y_min) / (resolution - 1)

    x, y = np.meshgrid(x_bins, y_bins, indexing='ij')
    c_mesh = ax.pcolormesh(x, y, rf_matrix, cmap='jet')
    plt.colorbar(c_mesh, ax=ax)
    ax.set_title('Rainflow Matrix', fontsize=13)
    ax.set_xlabel('Mean [g]', fontsize=11)
    ax.set_ylabel('Range [g]', fontsize=11)

    # Loop over data dimensions and create text annotations.
    if labels:
        for i in range(len(x) - 1):
            for j in range(len(y) - 1):
                ax.text(x_min + (i + .5) * x_bin_size,
                        y_min + (j + .5) * y_bin_size,
                        (rf_matrix[i, j]), ha='center', va='center', color='w',
                        fontsize=7)

    return ax


def from_to_matrix_plot(data: np.ndarray,
                        from_to_matrix: np.ndarray,
                        ax: matplotlib.axis,
                        labels=False) -> matplotlib.axis:
    """
    Plot the from-to matrix.

    :param data: (n x 2) array. First column is `from`, second column is `to`.
    :param from_to_matrix: the matrix to be plotted
    :param ax: axis for the plot
    :param labels: should the sequential labels be printed on the graph?
    :return: generated plot
    """
    a_min, a_max = np.floor(np.amin(data)), np.ceil(np.amax(data))
    resolution = len(from_to_matrix) + 1
    bins = np.linspace(a_min, a_max, resolution)
    x, y = np.meshgrid(bins, bins, indexing='ij')
    c_map = ax.pcolormesh(x, y, from_to_matrix, cmap='crest')
    plt.colorbar(c_map, ax=ax)
    bin_size = abs(a_max - a_min) / (resolution - 1)

    # Loop over data dimensions and create text annotations
    if labels:
        for i in range(len(x) - 1):
            for j in range(len(y) - 1):
                ax.text(a_min + (i + .5) * bin_size,
                        a_min + (j + .5) * bin_size,
                        int(from_to_matrix[i, j]), ha='center', va='center',
                        color='w', fontsize=7)

    ax.set_aspect('equal')
    ax.set_xlim(a_min, a_max)
    ax.set_ylim(a_min, a_max)
    ax.set_title('From-To Matrix', fontsize=13)
    ax.set_xlabel('From [g]', fontsize=11)
    ax.set_ylabel('To [g]', fontsize=11)

    # zero range
    ax.plot([-20, 20], [-20, 20], c='k', ls=(0, (3, 3)), lw=2,
            dash_capstyle='round')
    ax.text(a_max * 0.5, 0.5 + a_max * 0.5, 'Zero Range',
            ha='left', va='bottom', ma='center', rotation=45, color='k')

    # mean = 1
    ax.plot([20, -20], [-18, 22], ls=(0, (3, 3)), color='xkcd:wine', lw=2,
            dash_capstyle='round')
    ax.text(a_min * 0.5, 2.5 - a_min * 0.5, 'Mean = 1.',
            ha='center', va='center', ma='center', rotation=-45,
            color='xkcd:wine')

    # zero mean
    ax.plot([20, -20], [-20, 20], ls=(0, (3, 3)), color='b', lw=2,
            dash_capstyle='round')
    ax.text(a_min * 0.5, 0.5 - a_min * 0.5, 'Mean = 0.',
            ha='center', va='center', ma='center', rotation=-45, color='b')

    # compression zone
    ax.plot([0, 0], [a_min, 0], 'r', ls=(0, (.1, 2)), dash_capstyle='round')
    ax.plot([a_min, 0], [0, 0], 'r', ls=(0, (.1, 2)), dash_capstyle='round')
    ax.fill([a_min, 0, 0, a_min], [a_min, a_min, 0, 0], 'r', alpha=0.2,
            hatch='.....')
    ax.text(a_min / 2, a_min / 2, 'Compression\nZone',
            color='w', rotation=0, ha='center', va='center', ma='center')

    return ax


def plot_rf_matrix(count_matrix: np.ndarray,
                   x: np.ndarray,
                   y: np.ndarray,
                   x_bin_size: float,
                   y_bin_size: float,
                   ax: matplotlib.axis,
                   color_map: str = 'crest',
                   tlt: str = 'Title',
                   x_lbl: str = 'X',
                   y_lbl: str = 'Y',
                   labels=False
                   ) -> matplotlib.axis:
    """
    Generate heat graph for rainflow count matrices.


    :param count_matrix: Matrix containing the heat plot values which are
     cycle counts
    :param x: 1d array containing values which will be plotted on the x-axis
    :param y: 1d array containing values which will be plotted on y-axis
    :param x_bin_size: the bin size used on x-axis
    :param y_bin_size: the bin size used on the y-axis
    :param ax: input axis to generate plot on
    :param color_map: color map
    :param tlt: graph title
    :param x_lbl: x-axis label
    :param y_lbl: y-axis label
    :param labels: Should the count values be printed in each cell from
     `count_matrix`?
    :return: content of matplotlib axis
    """

    x_bin_edges = np.arange(np.floor(np.amin(x)),
                            np.ceil(np.amax(x)) + x_bin_size, x_bin_size)
    y_bin_edges = np.arange(np.floor(np.amin(y)),
                            np.ceil(np.amax(y)) + y_bin_size, y_bin_size)
    # x_bin_edges = np.arange(0.5, 1.5 + x_bin_size, (1.5 - .5 + x_bin_size)
    # / 20)
    # y_bin_edges = np.arange(0, 1.25 + y_bin_size, (1.25 + y_bin_size) / 20)

    c_mesh = ax.pcolormesh(x_bin_edges, y_bin_edges,
                           count_matrix,
                           cmap=color_map)  # , edgecolors='k', linewidth=.5)
    plt.colorbar(c_mesh, ax=ax)

    ax.set_title(tlt, fontsize=13)
    ax.set_xlabel(x_lbl, fontsize=11)
    ax.set_ylabel(y_lbl, fontsize=11)
    ax.set_aspect('auto')

    # Loop over data dimensions and create text annotations
    if labels:
        for i in range(count_matrix.shape[1]):
            for j in range(count_matrix.shape[0]):
                ax.text(x_bin_edges[0] + (i + .5) * x_bin_size,
                        y_bin_edges[0] + (j + .5) * y_bin_size,
                        f'{count_matrix[j, i]:.1f}', ha='center', va='center',
                        color='w', fontsize=7)

    return ax
