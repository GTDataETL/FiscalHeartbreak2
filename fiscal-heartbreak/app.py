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
    Optional argument - <i>year</i> to return data for a single year. For example: <a href='./api/MaritalStatus/2016'>/api/MaritalStatus/2016</a></p>
    <p><b>Debt to Income Ratio (DTI):</b><a href='./api/DTI'>/api/DTI</a> -- returns JSON of DTI ratios by County and Year<br>
    Optional argument - <i>year</i> to return data for a single year. For example: <a href='./api/DTI/2016'>/api/DTI/2016</a></p>
    <p><b>Fiscal Heartbreak:</b><a href='./api/fiscal-heartbreak'>/api/fiscal-heartbreak</a> -- returns JSON of both Divorce Rates and DTI ratios by County and Year<br>
    Optional argument - <i>year</i> to return data for a single year. For example: <a href='./api/fiscal-heartbreak/2016'>/api/fiscal-heartbreak/2016</a></p>

    </body>
    </html>"""

@app.route("/api/MaritalStatus")
@app.route("/api/MaritalStatus/<arg_year>")
def MaritalStatusAPI(arg_year=None):
    """Return a list of all marital status records
       Optional Argument: Year for which data is requested"""

    session = Session(engine)
    results = []

    if (arg_year == None):
        # Query all county marital status entries
        results = session.query(FiscalHeartbreak_tbl).all()
    else:
        # Query county marital status in the selected year
        results = session.query(FiscalHeartbreak_tbl).filter(FiscalHeartbreak_tbl.Year == arg_year).all()

    # initialize dict to return
    MaritalJSON = {}

    for record in results:

        # DEBUG
    #    print(f'{record.Year} | {record.CountyName} | {record.StateName} | {record.DivorcedPct} | {record.DivorcedError}')
        
        # if county not in output JSON yet, initialize new output record
       # countyState = record.CountyName + "|" + record.StateName
        if record.FIPS not in MaritalJSON.keys():
            MaritalJSON[record.FIPS] = {
                "FIPS": record.FIPS,
                "County": record.CountyName,
                "State": record.StateName,
                "Years": {}
            }

        #now that we know we have an existing record in output JSON, add stats for current year
        MaritalJSON[record.FIPS]["Years"][record.Year] = {
            "DivorcedPct": record.DivorcedPct,
            "DivorcedError": record.DivorcedError
        }

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
