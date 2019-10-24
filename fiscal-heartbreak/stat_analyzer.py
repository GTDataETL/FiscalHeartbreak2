import numpy as np
from scipy import stats
from app import FiscalHeartbreakAPI

def StatAnalyzer(year):
    
    diRatio = []
    divPct = []
    dataset = FiscalHeartbreakAPI(arg_year=year)

    for data in dataset:
        diRatio.append(dataset[data]['DtoI'])
        divPct.append(dataset[data]['DivorcedPct'])
    
    x = np.array(diRatio)
    y = np.array(divPct)

    slope, intercept, r_value, p_value = stats.linregress(x, y)
    stat_summary = {"slope":slope, "intercept":intercept, "R_squared":r_value**2, "P_value":p_value}

    return stat_summary