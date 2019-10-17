from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Reflection
#################################################
engine = create_engine("sqlite:///../db/fiscal-heartbreak.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
DTI = Base.classes.DebtToIncomeRatiosByYear
MaritalStatus = Base.classes.MaritalStatus

#DEBUG
print(Base.classes.keys())

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
        results = session.query(MaritalStatus).all()
    else:
        # Query county marital status in the selected year
        results = session.query(MaritalStatus).filter(MaritalStatus.Year == arg_year).all()

    # initialize dict to return
    MaritalJSON = {}

    for record in results:

        # DEBUG
    #    print(f'{record.Year} | {record.CountyName} | {record.StateName} | {record.DivorcedPct} | {record.DivorcedError}')
        
        # if county not in output JSON yet, initialize new output record
        countyState = record.CountyName + "|" + record.StateName
        if countyState not in MaritalJSON.keys():
            MaritalJSON[countyState] = {
                "County": record.CountyName,
                "State": record.StateName,
                "Years": {}
            }

        #now that we know we have an existing record in output JSON, add stats for current year
        MaritalJSON[countyState]["Years"][record.Year] = {
            "DivorcedPct": record.DivorcedPct,
            "DivorcedError": record.DivorcedError
        }

    return jsonify(MaritalJSON)


if __name__ == '__main__':
    app.run(debug=True)
