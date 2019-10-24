
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
      name: 'Divorce %',
      x: year,
      y: div_pct,
      marker: {
        color: "#17a2b8"
      }
    };

    var trace2 = {
      type: "bar",
      name: 'Debt to Income Ratio',
      x: year,
      y: DtoI,
      marker: {
        color: "#000000"
      },
      textposition: 'auto'
    };

    var data = [trace1, trace2];

    var layout = {
      title: `${county}, ${state} - Divorce Rates and Debt to Income Ratio (2015-2017)`,

      xaxis: {
        title: 'Year',
        autotick: false,
        tick0: 2015,
        dtick: 1,
      },
      yaxis: {
        title: 'Divorce %',
        autorange: true,
      },
      yaxis2: {
        title: "Debt to Income Ratio",
        overlaying: "y",
        side: "right",
        range: true,
        anchor: "x",
      },
    };

    Plotly.newPlot("bar-chart", data, layout, {responsive: true});

  });
}
