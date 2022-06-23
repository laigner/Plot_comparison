# Plot_comparison
Plotting the comparison of configurations, which are saved in csv, and save them as nice pdfs.

`csv_to_plot.py` will plot two columns of a csv as a beautiful matplotlib figure in seaborn-paper style

The `plot_parameter.py` is used to get the right width depending on the golden ratio.

`plot_kde.py` will plot the kernel estimated density of a csv with the help of `pandas` for different lengths of the same trajectory. Further it will integrate with the `scipy.simpson` function the kde to a specific point and plot this for every kde.

In general use the `--help` flag for more information on the parser arguments.
