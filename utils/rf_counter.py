import os
from pathlib import Path

import fatpack
import numpy as np
from matplotlib import pyplot as plt

from utils import GUI, get_data_np, graphs, level_crossing, matrices
import rainflow
from datetime import datetime

# logger setup
from utils.loggers import MyLog

logger = MyLog().logger


class RainFlowCounter:
    def __init__(self, file_path,
                 mean_bin_size, range_bin_size,
                 material, k_t, g_exc_bin_size,
                 racetrack_filter=True, h=0.1,
                 verbose=False):
        self.verbose = verbose
        self.racetrack_filter = racetrack_filter,
        self.file_path = file_path
        self.mean_bin_size = mean_bin_size
        self.range_bin_size = range_bin_size
        self.material = material
        self.k_t = k_t
        self.gExc_bin_size = g_exc_bin_size

        # load data
        t0 = datetime.now()
        self.tt, self.nz = get_data_np.get_data(self.file_path, [7])
        self.nz = np.array(self.nz).reshape(-1)

        if verbose:
            logger.info(
                f'\t▪ Data successfully loaded in '
                f'{round((datetime.now() - t0).total_seconds(), 3)} s.')

        # check if Nz is higher than 3.5g
        self.invalid_data = False
        if np.partition(self.nz, 1)[-1:] > 3.5:
            self.invalid_data = True

        # filter data
        if racetrack_filter:
            self.nz, ix = fatpack.find_reversals_racetrack_filtered(
                self.nz, h=h, k=200)
            self.tt = self.tt[ix]

        # extract cycles and their properties - (n, 5)
        # - columns = [mean, range, count, start, end]
        cyc_prop = {
            'cyc_mean': [], 'cyc_range': [], 'cyc_count': [],
            'start_i': [], 'end_i': [],
            'peak': [], 'valley': []
        }

        t0 = datetime.now()
        for rg, mn, c, i_s, i_e in rainflow.extract_cycles(
                self.nz):  # this is a generator
            cyc_prop['cyc_mean'].append(mn)
            cyc_prop['cyc_range'].append(rg)
            cyc_prop['cyc_count'].append(c)
            cyc_prop['start_i'].append(self.nz[i_s])
            cyc_prop['end_i'].append(self.nz[i_e])
            cyc_prop['peak'].append(mn + rg / 2)
            cyc_prop['valley'].append(mn - rg / 2)
        if verbose:
            logger.info(
                f'\t▪ Load cycles successfully extracted in '
                f'{round((datetime.now() - t0).total_seconds(), 3)} s.')

        self.cycles = np.column_stack(
            (cyc_prop['cyc_mean'], cyc_prop['cyc_range'],
             cyc_prop['cyc_count'], cyc_prop['peak'], cyc_prop['valley']))

        # ==================== level cross counting ====================
        t0 = datetime.now()
        self.top_bins, self.bottom_bins, self.top_counts, self.bottom_counts \
            = level_crossing.level_cross_count(self.cycles[:, 2:],
                                               self.gExc_bin_size)
        if verbose:
            logger.info(f'\t▪ Level-crossings successfully calculated in '
                        f'{round((datetime.now() - t0).total_seconds(), 3)} '
                        f's.\n')

        # print(gc.get_count())
        # gc.collect()
        # print(gc.get_count())

    # ================ method to generate mean-range matrix ================
    def mean_range_matrix(self, mean_bin_size, range_bin_size):
        t0 = datetime.now()
        if self.verbose:
            m_r_matrix = matrices.mean_range_matrix(self.cycles, mean_bin_size,
                                                    range_bin_size)
            logger.info(f'\t▪ Mean-Range matrix successfully generated in '
                        f'{round((datetime.now() - t0).total_seconds(), 3)} '
                        f's.')
        else:
            m_r_matrix = matrices.mean_range_matrix(self.cycles, mean_bin_size,
                                                    range_bin_size)
        return m_r_matrix

    # ================== method to generate from-to matrix ==================
    def from_to_matrix(self, from_bin_size=0.25, to_bin_size=0.25):
        t0 = datetime.now()
        if self.verbose:
            from_to_matrix = matrices.from_to(self.cycles, from_bin_size,
                                              to_bin_size)
            logger.info(f'\t▪ From-To matrix successfully generated in '
                        f'{round((datetime.now() - t0).total_seconds(), 3)} '
                        f's.')
        else:
            from_to_matrix = matrices.from_to(self.cycles, from_bin_size,
                                              to_bin_size)
        return from_to_matrix

    # ========== method to calculate total damage from Minor's rule ==========
    def total_damage(self, material, k_t):
        t0 = datetime.now()
        if self.verbose:
            total_damage = matrices.damage(material, k_t)
            logger.info(f'\t▪ Total damage successfully calculated in '
                        f'{round((datetime.now() - t0).total_seconds(), 3)} '
                        f's.')
        else:
            total_damage = matrices.damage(material, k_t)
        return total_damage


class MultipleFlights:

    def __init__(self, verbose=False):
        """
        This is the main object that calls the GUI to either run a single
        IMU file or aggregate the IMU data from multiple flights and
        generate a total g-exceedance curve.

        :param verbose: bool Determines whether punch report of the process
         time in the run console.

        """
        t0 = datetime.now()
        self.verbose = verbose

        # call GUI
        self.mode, mean_bin_size, range_bin_size, gExc_bin_size, \
        self.address, material, k_t, rt_flt, h, self.show_labels = \
            GUI.call_gui()

        # adjust file names and addresses depending on analysis type requested
        if self.mode:  # if multi file analysis is requested
            # create list of all the files in `address`
            imu_files = os.listdir(self.address)
        else:  # if single file analysis is requested
            imu_files = [
                os.path.basename(self.address)]  # put the file name in a list
            # get the directory name
            self.address = os.path.dirname(self.address)

        # create and populate a list, each element of which is a
        # `RainFlowCounter` object generated by processing each file (flight)
        self.flights = []
        i = 0
        for file_name in imu_files:
            i += 1
            # use only *.dat files
            ext = os.path.splitext(file_name)[1]
            if ext != '.dat':
                pass
            else:
                with open(os.path.join(self.address, file_name), 'r') as f:
                    if len(f.readline()) != 152:
                        pass
                    else:
                        logger.info(
                            f'• {i}. Analyzing "{file_name.split(".")[0]}"')
                        flight = RainFlowCounter(
                            os.path.join(self.address, file_name),
                            mean_bin_size, range_bin_size,
                            material, k_t, gExc_bin_size,
                            racetrack_filter=rt_flt, h=h,
                            verbose=self.verbose)

                        # in case flight data contains Nz > 3, discard file
                        if flight.invalid_data:
                            logger.warning(
                                f'File "{file_name.split(".")[0]}" contains '
                                f'Nz values higher than 3.5g, therefore was '
                                f'discarded.')
                            continue
                        else:
                            self.flights.append(flight)

        # each flight object has its own dimensions based on its data range
        # and requested g-exceedance resolution. Below all flights are
        # padded with zeros to match the flight with the widest data range.

        # farthest bin above baseline (flight with the widest data range)
        highest_bin = max([len(f.top_counts) for f in self.flights])
        self.x_above = np.argmax([len(f.top_counts) for f in self.flights])

        # farthest bin below baseline (flight with the widest data range)
        lowest_bin = max([len(f.bottom_counts) for f in self.flights])
        self.x_below = np.argmax([len(f.bottom_counts) for f in self.flights])

        for f in self.flights:
            if len(f.top_counts) < highest_bin:
                f.top_counts = np.pad(f.top_counts,
                                      (0, highest_bin - len(f.top_bins)),
                                      'constant')

            if len(f.bottom_counts) < lowest_bin:
                f.bottom_counts = np.pad(f.bottom_counts,
                                         (0, lowest_bin - len(f.bottom_bins)),
                                         'constant')

        # aggregation of all flights (files)
        self.above_baseline_counts = \
            sum([f.top_counts for f in self.flights])
        self.below_baseline_counts = \
            sum([f.bottom_counts for f in self.flights])

        minutes = divmod((datetime.now() - t0).total_seconds(), 60)
        logger.info(
            f'Total collapsed time is '
            f'{int(minutes[0])} minutes and {round(minutes[1], 3)} seconds.')

    def g_exc_curve(self,
                    title: str = 'g-Exceedance Spectra',
                    x_label: str = r'$N_Z$, Vertical Acceleration [g]',
                    y_label: str = 'Cumulative Exceedance Count',
                    save_figure: bool = False):
        """
        Method to generate the aggregate g-exceedance curve from all input data

        :param title: Graph title
        :param x_label: x-axis label
        :param y_label: y-axis label
        :param save_figure: should the graph be saved?
        :return: Shows the graph.
        """

        fig, ax = plt.subplots(figsize=(11, 7), dpi=150)
        plt.subplots_adjust(bottom=0.1, top=0.94, right=0.96, left=0.1)

        graphs.g_exceedance_plot(top_bins=self.flights[self.x_above].top_bins,
                                 top_counts=self.above_baseline_counts,
                                 bottom_bins=self.flights[
                                     self.x_below].bottom_bins,
                                 bottom_counts=self.below_baseline_counts,
                                 title=title, x_label=x_label, y_label=y_label,
                                 print_label=self.show_labels,
                                 print_bins=False,
                                 ax=ax)

        # save graph if requested
        if save_figure:
            # form the image name and its storage directory
            now = datetime.now()
            d, m, y = \
                now.strftime('%d'), now.strftime('%b'), now.strftime('%Y')
            hr, mn = \
                now.strftime('%H'), now.strftime('%M')
            img_name = \
                title + ' ' + d + m + y + ', ' + hr + '-' + mn + '.png'
            img_dir = os.path.join(self.address, '~images')

            # check if the directory exist and if not, create it
            Path(img_dir).mkdir(parents=True, exist_ok=True)

            # save image and report the address
            plt.savefig(os.path.join(img_dir, img_name), dpi=300)
            logger.info(f'\nThe plot is saved as an image at the address '
                        f'below:\n\n{os.path.join(img_dir, img_name)}')

        # show the plot
        plt.show()
