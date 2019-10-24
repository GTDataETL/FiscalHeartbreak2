import numpy as np
from scipy import stats
from sqlalchemy.orm import Session

def StatAnalyzer(year, FiscalHeartbreak_tbl, engine):
    session = Session(engine)

    outputJSON = {}
  
    results = session.query(FiscalHeartbreak_tbl).filter(FiscalHeartbreak_tbl.Year == year).all()

    for record in results:
        if record.FIPS not in outputJSON.keys():
            outputJSON[record.FIPS] = {
                "FIPS": record.FIPS,
                "County": record.CountyName,
                "State": record.StateName,
                "Years": [],
                "DivorcedPct": [],
                "DivorcedError": [],
                "DtoI": []
            }
            outputJSON[record.FIPS]["Years"].append(record.Year)
            outputJSON[record.FIPS]["DivorcedPct"].append(record.DivorcedPct)
            outputJSON[record.FIPS]["DivorcedError"].append(record.DivorcedError)
            outputJSON[record.FIPS]["DtoI"].append((record.DtoI_low + record.DtoI_high)/2)
        else:
            outputJSON["FIPS"] = record.FIPS,
            outputJSON["County"] = record.CountyName,
            outputJSON["State"] = record.StateName,
            outputJSON["Years"].append(record.Year)
            outputJSON["DivorcedPct"].append(record.DivorcedPct)
            outputJSON["DivorcedError"].append(record.DivorcedError)
            outputJSON["DtoI"].append((record.DtoI_low + record.DtoI_high)/2)

    session.close()
    
    diRatio = []
    divPct = []
    # pass year into api function
    dataset = outputJSON

    # iterate through api data
    # append ratio and percent data into appropriate lists
    for data in dataset:
        diRatio.append(dataset[data]['DtoI'][0])
        divPct.append(dataset[data]['DivorcedPct'][0])
    
    # use numpy and stats to find calculations
    x = np.array(diRatio)
    y = np.array(divPct)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # store results into dictionary and return
    stat_summary = {"slope":slope, "intercept":intercept, "R_squared":r_value**2, "P_value":p_value}

    return stat_summary