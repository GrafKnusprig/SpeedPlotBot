import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def setup_modern_plot():
    plt.style.use("dark_background")
    plt.rcParams.update(
        {
            "figure.facecolor": "#2E2E2E",
            "axes.facecolor": "#2E2E2E",
            "axes.edgecolor": "#FFFFFF",
            "axes.labelcolor": "#FFFFFF",
            "xtick.color": "#FFFFFF",
            "ytick.color": "#FFFFFF",
            "grid.color": "#5A5A5A",
            "grid.alpha": 0.3,
            "axes.titlepad": 20,
            "legend.facecolor": "#3A3A3A",
            "legend.edgecolor": "#FFFFFF",
            "patch.linewidth": 0,
            "font.size": 12,
            "lines.linewidth": 2,
            "lines.marker": "o",
            "lines.markersize": 6,
            "savefig.facecolor": "#2E2E2E",
            "savefig.edgecolor": "#2E2E2E",
        }
    )
