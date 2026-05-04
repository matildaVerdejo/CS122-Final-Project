import numpy as np
from scipy import stats

# computes descriptive statistics on earthquake magnitudes
# parameters: earthquakes (list of dict): Parsed earthquake records from parse_earthquakes()
# returns: a dict with:
    # count (int): num of earthquakes
    # mean (float): mean magnitude
    # median (float): median magnitude
    # std_dev (float): standard deviation of magnitudes
    # min (float): minimum magnitude
    # max (float): maximum magnitude
# RETURNS NONE IF LIST IS EMPTY/MAGNITUDES CAN'T BE EXTRACTED
def compute_magnitude_stats(earthquakes):
    magnitudes = [eq["magnitude"] for eq in earthquakes if eq.get("magnitude") is not None]

    if not magnitudes:
        return None

    magnitudes = np.array(magnitudes)
    return {
        "count": len(magnitudes),
        "mean": round(float(np.mean(magnitudes)), 3),
        "median": round(float(np.median(magnitudes)), 3),
        "std_dev": round(float(np.std(magnitudes)), 3),
        "min": round(float(np.min(magnitudes)), 3),
        "max": round(float(np.max(magnitudes)), 3),
    }

# computes daily earthquake frequency and a linear trend, slope, over time with scipy linregress
# parameters: earthquakes (list of dict): parsed earthquake records from parse earthquakes()
# returns: a dict with:
    # dates (list of str): sorted dates in the dataset
    # counts (list of int): num of eathquakes per date
    # slope (float): linear regression slope (events / day trend)
    # trend (str): trend description (inc, dec, stable)
# RETURNS NONE IF FEWER THAN 2 DATA POINTS
def compute_frequency_trend(earthquakes):
    from collections import Counter

    date_counts = Counter()
    for eq in earthquakes:
        time_str = eq.get("time")

        if time_str:
            # extracting date 'YYYY-MM-DD'
            date = time_str[:10]
            date_counts[data] += 1

    if len(date_counts) < 2:
        return None

    sorted_dates = sorted(date_counts.key())
    counts = [date_counts[d] for d in sorted_dates]

    from datetime import date as date_type
    ordinals = [date_type.fromisoformat(d).toordinal() for d in sorted_dates]

    slope, intercept, r_value, p_value, std_err = stats.linregress(ordinals, counts)

    if slope > 0.05:
        trend = "increasing"
    elif slope < -0.05:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        "dates": sorted_dates,
        "counts": counts,
        "slope": round(slope, 4),
        "trend": trend,
    }
