import matplotlib.pyplot as plt

from utils.rf_counter import RainFlowCounter
from utils import graphs
from utils import GUI

mean_bin_size, range_bin_size, gExc_bin_size, path, material, k_t = GUI.gui_single_file()

f1 = RainFlowCounter(path, mean_bin_size, range_bin_size, material, k_t, gExc_bin_size,
                     verbose=True)
# f1 = RainFlowCounter('C:\\Users\\pooya.rowghanian\\Desktop\\Wednesday November 10, 2021 12-33 PM - Copy.dat',
#                      verbose=True)
print(f1.tt.shape)
print(f1.cycles.shape)
# print(f1.mean_range_matrix(mean_bin_size, range_bin_size).shape)
# print(f1.from_to_matrix().shape)
# print(f1.total_damage('2014-T6 Aluminium', '1.6, Bar, Longitudinal'))

# print(gc.get_count())
# gc.collect()
# print(gc.get_count())

fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(hspace=.3, wspace=.27, bottom=0.1, top=.94, right=.96, left=0.1)
graphs.g_exceedance_plot(top_bins=f1.top_bins, top_counts=f1.top_counts,
                         bottom_bins=f1.bottom_bins, bottom_counts=f1.bottom_counts,
                         print_label=False, print_bins=False,
                         ax=ax)
# graphs.plot_signal(x=f1.tt, y=f1.nz, ax=ax)
plt.show()
