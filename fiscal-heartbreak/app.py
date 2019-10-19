from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import os
import sys


#################################################
# Database Reflection
#################################################
print("Starting...")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', '') }")
print(f"Database URL: {os.environ.get('DATABASE_URL', '') or 'sqlite:///../db/fiscal-heartbreak-slim.sqlite'}")
sys.stdout.flush()

db_url = os.environ.get('DATABASE_URL', '') or "sqlite:///../db/fiscal-heartbreak-slim.sqlite"
engine = create_engine(db_url)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#DEBUG
print(Base.classes.keys())

# Save reference to the table
FiscalHeartbreak_tbl = Base.classes.fiscal_heartbreak_all


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/ab")
def ab():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Divorce Plot</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/5.5.0/d3.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="plot"></div>
    <script src="../static/js/appAB.js"></script>
</body>
</html>

    '''
@app.route("/")
def home():
    """Homepage for Fiscal-Heartbreak Viz project"""
    return """
    <html>
    <title>Fiscal Heartbreak Visualization</title>
    <body>
    <h1>Fiscal Heartbreak Visualization</h1>
    <p>This page will be replaced with the wicked cool viz components
    built by Andrew, Michael, and Joseph</p>
    <p>To see the available API endpoints, navigate to <a href='./api'>/api</a>
    </body>
    </html>"""

@app.route("/api")
def api_list():
    """List all available api routes."""
    return """
    <html>
    <title>Fiscal Heartbreak API</title>
    <body>
    <h1>Fiscal Heartbreak API</h1>
    <p>The following API endpoints are available:</p>
    <br>
    <hr>
    <br>
    <p><b>Marital Status:</b><a href='./api/MaritalStatus'>/api/MaritalStatus</a> -- returns JSON of Divorce Rates by County and Year<br>
    Optional argument - year/<i><year></i> to return data for a single year. For example: <a href='./api/MaritalStatus/year/2016'>/api/MaritalStatus/year/2016</a>
    Optional argument - county/<i><fips code></i> to return data for a single county. For example: <a href='./api/MaritalStatus/county/1005'>/api/MaritalStatus/county/1005</a></p>
    <p><b>Debt to Income Ratio (DTI):</b><a href='./api/DTI'>/api/DTI</a> -- returns JSON of DTI ratios by County and Year<br>
    Optional argument - <i>year</i> to return data for a single year. For example: <a href='./api/DTI/2016'>/api/DTI/2016</a></p>
    <p><b>Fiscal Heartbreak:</b><a href='./api/fiscal-heartbreak'>/api/fiscal-heartbreak</a> -- returns JSON of both Divorce Rates and DTI ratios by County and Year<br>
    Optional argument - <i>year</i> to return data for a single year. For example: <a href='./api/fiscal-heartbreak/2016'>/api/fiscal-heartbreak/2016</a></p>

    </body>
    </html>"""

@app.route("/api/MaritalStatus")
@app.route("/api/MaritalStatus/year/<arg_year>")
@app.route("/api/MaritalStatus/county/<arg_county>")
def MaritalStatusAPI(arg_year=None,arg_county=None):
    """Return a list of all marital status records
       Optional Argument: Year for which data is requested
       Optional Argument: County FIPS for which data is requested
       """

    session = Session(engine)
    results = []

    # initialize dict to return
    MaritalJSON = {}

    if ((arg_year == None) and (arg_county == None)):
        # Query all county marital status entries
        results = session.query(FiscalHeartbreak_tbl).all()
    elif(arg_county == None):
        # Query county marital status in the selected year for all counties
        results = session.query(FiscalHeartbreak_tbl).filter(FiscalHeartbreak_tbl.Year == arg_year).all()
    else:
        # Query county marital status in the selected county for all years
        results = session.query(FiscalHeartbreak_tbl).filter(FiscalHeartbreak_tbl.FIPS == arg_county).all()

        # reset MaritalJSON to have properties directly on root since we will only have 1 county
        MaritalJSON = {
            "FIPS": "",
            "County": "",
            "State": "",
            "Years": [],
            "DivorcedPct": [],
            "DivorcedError": []
        }

    for record in results:

        # DEBUG
    #    print(f'{record.Year} | {record.CountyName} | {record.StateName} | {record.DivorcedPct} | {record.DivorcedError}')
        
        if (arg_county == None):
            # if county not in output JSON yet, initialize new output record
            if record.FIPS not in MaritalJSON.keys():
                MaritalJSON[record.FIPS] = {
                    "FIPS": record.FIPS,
                    "County": record.CountyName,
                    "State": record.StateName,
                    "Years": [],
                    "DivorcedPct": [],
                    "DivorcedError": []
                }

            #now that we know we have an existing record in output JSON, add stats for current county and year
            MaritalJSON[record.FIPS]["Years"].append(record.Year)
            MaritalJSON[record.FIPS]["DivorcedPct"].append(record.DivorcedPct)
            MaritalJSON[record.FIPS]["DivorcedError"].append(record.DivorcedError)
        else:
            # API was called for single county, just serve up the data directly without a new object by FIPS
            MaritalJSON["FIPS"] = record.FIPS,
            MaritalJSON["County"] = record.CountyName,
            MaritalJSON["State"] = record.StateName,
            MaritalJSON["Years"].append(record.Year)
            MaritalJSON["DivorcedPct"].append(record.DivorcedPct)
            MaritalJSON["DivorcedError"].append(record.DivorcedError)

    return jsonify(MaritalJSON)

@app.route("/api/DTI")
@app.route("/api/DTI/<arg_year>")
def DTI_API(arg_year=None):
    """Return a list of all Debt to Income records
       Optional Argument: Year for which data is requested"""

    session = Session(engine)
    results = []

    if (arg_year == None):
        # Query all county DTI entries
        results = session.query(FiscalHeartbreak_tbl).all()
    else:
        # Query county DTI in the selected year
        results = session.query(FiscalHeartbreak_tbl).filter(FiscalHeartbreak_tbl.Year == arg_year).all()

    # initialize dict to return
    DTI_JSON = {}

    for record in results:

        # DEBUG
    #    print(f'{record.Year} | {record.CountyName} | {record.StateName} | {record.DtoI_low} | {record.DtoI_high}')
        
        # if county not in output JSON yet, initialize new output record
       # countyState = record.CountyName + "|" + record.StateName
        if record.FIPS not in DTI_JSON.keys():
            DTI_JSON[record.FIPS] = {
                "FIPS": record.FIPS,
                "County": record.CountyName,
                "State": record.StateName,
                "Years": {}
            }

        #now that we know we have an existing record in output JSON, add stats for current year
        DTI_JSON[record.FIPS]["Years"][record.Year] = {
            "DtoI_low": record.DtoI_low,
            "DtoI_high": record.DtoI_high
        }

    return jsonify(DTI_JSON)

@app.route("/api/fiscal-heartbreak")
@app.route("/api/fiscal-heartbreak/<arg_year>")
def FiscalHeartbreakAPI(arg_year=None):
    """Return a list of all records
       Optional Argument: Year for which data is requested"""

    session = Session(engine)
    results = []

    if (arg_year == None):
        # Query all county entries
        results = session.query(FiscalHeartbreak_tbl).all()
    else:
        # Query county marital status in the selected year
        results = session.query(FiscalHeartbreak_tbl).filter(FiscalHeartbreak_tbl.Year == arg_year).all()

    # initialize dict to return
    outputJSON = {}

    for record in results:

        # DEBUG
    #    print(f'{record.Year} | {record.CountyName} | {record.StateName} | {record.DivorcedPct} | {record.DivorcedError} | {record.DtoI_low} | {record.DtoI_high}')
        
        # if county not in output JSON yet, initialize new output record
       # countyState = record.CountyName + "|" + record.StateName
        if record.FIPS not in outputJSON.keys():
            outputJSON[record.FIPS] = {
                "FIPS": record.FIPS,
                "County": record.CountyName,
                "State": record.StateName,
                "Years": {}
            }

        #now that we know we have an existing record in output JSON, add stats for current year
        outputJSON[record.FIPS]["Years"][record.Year] = {
            "DivorcedPct": record.DivorcedPct,
            "DivorcedError": record.DivorcedError,
            "DtoI_low": record.DtoI_low,
            "DtoI_high": record.DtoI_high
        }

    return jsonify(outputJSON)



if __name__ == '__main__':
    app.run(debug=True)
