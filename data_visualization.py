import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# generates bar chart of earthquake frequency over time
# parameters:
    # frequency_data (dict): output from compute_frequency_trend(), contains 'dates' (list of strings), 'counts' (list of ints)
    # ax (matplotlib.axes.Axes, optional): axes to draw on, new figure/axes created if there is none
# returns: matplotlib.figure.Figure: figure containing plot, none if frequency_data us none/invalid
def plot_frequency_over_time(frequency_data, ax=None):

    if not frequency_data or not frequency_data.get("dates"):
        return None

    dates = [datetime.strptime(d, "%Y-%m-%d") for d in frequency_data["dates"]]
    counts = frequency_data["counts"]

    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4))
    else:
        fig = ax.get_figure()

    ax.bar(dates, counts, color="#3a7ebf", edgecolor="white", linewidth=0.5, width=0.8)
    ax.set_title("Earthquake Frequency Over Time", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Number of Earthquakes", fontsize=10)

    # format x-axis dates based on range
    date_range = (max(dates) - min(dates)).days
    if date_range <= 14:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.DayLocator())
    elif date_range <= 90:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())

    fig.autofmt_xdate(rotation=35, ha="right")
    ax.tick_params(axis="both", labelsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    trend = frequency_data.get("trend", "")
    if trend:
        ax.annotate(
            f"Trend: {trend}",
            xy=(0.02, 0.95),
            xycoords="axes fraction",
            fontsize=9,
            color="#555555",
            va="top"
        )

    if standalone:
        fig.tight_layout()
    return fig

# generates a histogram of earthquake magnitude distribution
# parameters:
    # earthquakes (list of dict): parsed earthquake records from parse_earthquakes()
    # ax (matplotlib.axes.Axes, optional): axes to draw on, new fig/axes created if none
# returns: matplotlib.figure.Figure: figure containing histogram, none if no valid magnitude data found
def plot_magnitude_histogram(earthquakes, ax=None):

    magnitudes = [eq["magnitude"] for eq in earthquakes if eq.get("magnitude") is not None]

    if not magnitudes:
        return None

    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 4))
    else:
        fig = ax.get_figure()

    n, bins, patches = ax.hist(magnitudes, bins=15, color="#f9b1ed", edgecolor="white", linewidth=0.5)

    ax.set_title("Magnitude Distribution", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Magnitude", fontsize=10)
    ax.set_ylabel("Number of Earthquakes", fontsize=10)
    ax.tick_params(axis="both", labelsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    # mark mean and median with vertical lines
    import numpy as np

    mean_val = float(np.mean(magnitudes))
    median_val = float(np.median(magnitudes))
    ax.axvline(mean_val, color="#c0392b", linestyle="--", linewidth=1.4, label=f"Mean: {mean_val:.2f}")
    ax.axvline(median_val, color="#2980b9", linestyle=":", linewidth=1.4, label=f"Median: {median_val:.2f}")
    ax.legend(fontsize=9)

    if standalone:
        fig.tight_layout()
    return fig

# builds a combined figure with both plots, for embedding in Tkinter results window
# parameters:
    # earthquakes (list of dict): parsed earthquake records
    # frequency_data (dict): output from compute_frequency_trend()
# returns: matplotlib.figure.Figure: figure with 2 subplots, none if both data inputs are invalid
def build_results_figure(earthquakes, frequency_data):
    magnitudes = [eq["magnitude"] for eq in earthquakes if eq.get("magnitude") is not None]
    if not magnitudes:
        return None
 
    has_freq = (
        frequency_data is not None
        and len(frequency_data.get("dates", [])) >= 2
    )
 
    if has_freq:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
        fig.patch.set_facecolor("#f7f7f7")
        plot_frequency_over_time(frequency_data, ax=ax1)
        plot_magnitude_histogram(earthquakes, ax=ax2)
    else:
        fig, ax = plt.subplots(1, 1, figsize=(7, 4.5))
        fig.patch.set_facecolor("#f7f7f7")
        plot_magnitude_histogram(earthquakes, ax=ax)
 
    fig.tight_layout(pad=2.5)
    return fig