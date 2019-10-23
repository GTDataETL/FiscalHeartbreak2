import pandas as pd
import numpy as np
from scipy import stats

class StatAnalysis():
    
    x = np.array(df['diRatio'])
    y = np.array(corrected_df['divPct'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    stat_summary = {"slope":slope, "intercept":intercept, "R-squared":r_value**2, "P-value":p_value}

    return stat_summary