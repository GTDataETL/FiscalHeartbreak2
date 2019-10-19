
/* global Plotly */
var url =`/api/MaritalStatus/county/1005`;

/**
 * Helper function to select stock data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - Date
 * index 1 - Open
 * index 2 - High
 * index 3 - Low
 * index 4 - Close
 * index 5 - Volume
 */
function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

function buildPlot() {
  d3.json(url).then(function(data) {

    // Grab values from the data json object to build the plots
    var county = data.County;
    var state = data.State;
    var year = data.Years;
    var FIPS = data.FIPS;
    var div_error = data.DivorcedError;
    var div_pct = data.DivorcedPct;

    var trace1 = {
      type: "bar",
      name: county,
      x: year,
      y: div_pct,
      line: {
        color: "#17BECF"
      }
    };

    var data = [trace1];

    var layout = {
      title: `${county} Divorce Rates`,

      xaxis: {
        autotick: false,
        tick0: 2015,
        dtick: 1,
      },
      yaxis: {
        autorange: true,
        type: "linear",
      }
    };

    Plotly.newPlot("plot", data, layout);
    

  });
}

buildPlot();