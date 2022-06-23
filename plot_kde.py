import matplotlib.pyplot as plt
import pandas as pd
import argparse
from plot_parameter import set_size
import numpy as np
from scipy import integrate

plt.style.use("seaborn-paper")
tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 6,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    # Handle ticks
    "xtick.top": True,
    "xtick.direction": "in",
    "ytick.right": True,
    "ytick.direction": "in",
}
plt.rcParams.update(tex_fonts)
parser = argparse.ArgumentParser(description="Making nice plots of MMK csv")
parser.add_argument("-i", "--input", help="The file to plot", type=str)
parser.add_argument("-okde", "--outputKDE", help="The output file for kde", type=str)
parser.add_argument("-oint", "--outputint", help="The output file for integral", type=str)
parser.add_argument(
    "-w", "--width", help="Width of the figure", default="thesis", type=str
)
parser.add_argument(
    "-n",
    "--names",
    nargs="+",
    help="Names of dataframe columns",
    default=["configuration_index", "maximum"],
)
parser.add_argument(
    "-x", "--xlabel", help="Label of x axis", default="MMK similarity", type=str
)
parser.add_argument("-d", "--divider", help="Number of histograms", type=int, default=5)
parser.add_argument("-c", "--corr", help="Correlation step", type=int, default=10)
args = parser.parse_args()
if args.width == "beamer":
    tex_fonts['font.family'] = 'sans-serif'
    tex_fonts['axes.labelsize'] = 24
    tex_fonts['font.size'] = 24
    tex_fonts['legend.fontsize'] = 14
    tex_fonts['xtick.labelsize'] = 19
    tex_fonts['ytick.labelsize'] = 19
    plt.rcParams.update(tex_fonts)
df = pd.read_csv(args.input)
divider = len(df[args.names[1]])/args.divider
division = np.linspace(start=divider, stop=len(df[args.names[1]]), num=args.divider, endpoint=True, dtype=int)
fig_1, ax_1 = plt.subplots(figsize=set_size(width=args.width))
for i in division:
    df[args.names[1]][:i].plot.kde(ax=ax_1, label=fr'Cut at $t={i*args.corr}$')
ax_1.axvline(0.93, color='grey', linestyle='dashed')
ax_1.text(0.89, 70,'integration limit')
ax_1.set_xlabel(args.xlabel)
ax_1.set_ylabel("Kernel estimated density")
ax_1.legend()
fig_1.savefig(args.outputKDE, format='pdf', bbox_inches='tight')
integrals = []
for i, line in enumerate(ax_1.get_lines()[:-1]):
    limit = np.where(np.around(line.get_data()[0], decimals=4) == 0.95)[0][0]
    x = line.get_data()[0][:limit]
    y = line.get_data()[1][:limit]
    integral_value = integrate.simps(y, x)
    integrals.append(integral_value)
fig_1.clear()
fig, ax = plt.subplots(figsize=set_size(width=args.width))
x_values = np.array([x*args.corr for x in division])
y_values = np.array(integrals)
ax.plot(x_values, y_values, '^', markersize=10, color='b')
ax.set_xlabel('Time step')
ax.set_ylabel('Probability')
fig.savefig(args.outputint, format='pdf', bbox_inches='tight')
fig.clear()