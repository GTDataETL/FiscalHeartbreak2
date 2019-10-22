
/* global Plotly */
var url =`/api/fiscal-heartbreak/county/`;

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

function buildPlot(FIPS) {
  var FIPS_url = url+FIPS;
  d3.json(FIPS_url).then(function(data) {

    // Grab values from the data json object to build the plots
    var county = data.County;
    var state = data.State;
    var year = data.Years;
    var div_pct = data.DivorcedPct;
    var DtoI = data.DtoI;

    var trace1 = {
      type: "bar",
      name: county,
      x: year,
      y: div_pct,
      line: {
        color: "#17BECF"
      }
    };

    var trace2 = {
      type: "bar",
      name: DtoI,
      x: year,
      y: DtoI,
      line: {
        color: "#FF0000"
      }
    };

    var data = [trace1, trace2];

    var layout = {
      title: `${county}, ${state} - Divorce Rates and Debt to Income Ratio (2015-2017)`,

      xaxis: {
        autotick: false,
        tick0: 2015,
        dtick: 1,
      },
      yaxis: {
        title: 'Divorce %',
        autorange: true,
      },
      yaxis2: {
        title: 'Debt to Income Ratio',
        autorange: true,
        overlaying: 'y',
        side: 'right'
    },
    };

    Plotly.newPlot("bar-chart", data, layout);

  });
}

buildPlot("1005");