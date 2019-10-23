
/* global Plotly */
var url =`/api/fiscal-heartbreak/county/`;

function buildPlot(arg_FIPS) {

  api_url = url+arg_FIPS;

  d3.json(api_url).then(function(data) {

    // Grab values from the data json object to build the plots
    var county = data.County;
    var state = data.State;
    var year = data.Years;
    var FIPS = data.FIPS;
    var div_error = data.DivorcedError;
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

    Plotly.newPlot("bar-chart", data, layout);

  });
}