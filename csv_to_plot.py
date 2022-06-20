import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
from plot_parameter import set_size
import pathlib

# general theme for plot
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
# add parser arguments to start from command line
parser = argparse.ArgumentParser(description="Making nice plots of MMK csv")
parser.add_argument("-i", "--input", help="The file to plot", type=str)
parser.add_argument("-o", "--output", help="The output file", type=str)
parser.add_argument("-c", "--corr", help="Correlation time", default=10, type=int)
parser.add_argument("-s", "--size", help="Size of averaging window", default=10, type=int)
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
    "-y", "--ylabel", help="Label of y axis", default="MMK similarity", type=str
)
args = parser.parse_args()
# adjust plot parameter for presentations
if args.width == "beamer":
    tex_fonts = {
        # Use LaTeX to write all text
        "text.usetex": True,
        "font.family": "sans-serif",
        # Use 24pt font in plots, to match 24pt font in powerpoint
        "axes.labelsize": 124,
        "font.size": 24,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 14,
        "xtick.labelsize": 19,
        "ytick.labelsize": 19,
        # Handle ticks
        "xtick.top": True,
        "xtick.direction": "in",
        "ytick.right": True,
        "ytick.direction": "in",
    }
    plt.rcParams.update(tex_fonts)
# create figure
fig, ax = plt.subplots(1, 1, figsize=set_size(width=args.width))
# load data into dataframe
df = pd.read_csv(args.input)
# plot data
ax.plot(df[args.names[0]] * args.corr, df[args.names[1]], color=f"b", alpha=0.4)
# plot running average
ax.plot(
    df[args.names[0]] * args.corr,
    df[args.names[1]].rolling(args.size).mean(),
    color=f"b",
    linewidth=2.0,
)
# set axis labels
ax.set_xlabel("Time step")
ax.set_ylabel(args.ylabel)
# save figure
fig.savefig(pathlib.Path(args.output), format="pdf", bbox_inches="tight")
