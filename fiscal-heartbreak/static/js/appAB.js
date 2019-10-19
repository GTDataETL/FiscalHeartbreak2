
/* global Plotly */
var url =`/api/MaritalStatus`;

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
    var county = data[1003].County;
    var state = data[1003].State;
    var year = data[1003].Years;
    var FIPS = data[1003].FIPS;
    var div_error = data[1003].DivorcedError;
    var div_pct = data[1003].DivorcedPct;

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
      title: `County Divorce Rates`,
      xaxis: {
        autotick: "true",
      },
      
      yaxis: {
        autorange: true,
        type: "linear"
      }
    };

    Plotly.newPlot("plot", data, layout);
    

  });
}

buildPlot();