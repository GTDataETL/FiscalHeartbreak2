
/* global Plotly */
var url =`/api/fiscal-heartbreak/county/`;

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
      name: "Divorce %",
      x: year,
      y: div_pct,
      width: [.4,.4,.4],
      offset: [-.3,-.3,-.3],
      marker: {
        color: "#17a2b8"
      }
    };

    var trace2 = {
      type: "bar",
      name: "Debt to Income Ratio",
      x: year,
      y: DtoI,
      width: [.4, .4, .4],
      offset: [-.1, -.1, -.1],
      marker: {
        color: "#000000"
      },
      yaxis: "y2"
    };

    var data = [trace1, trace2];

    var layout = {
      title: `Divorce Percentage vs. Debt to Income Ratio - ${county}, ${state}`,
      titlefont: {
        size: 24
      },
      font: {
        family: 'Helvetica Neue, monospace',
        size: 14,
        color: '#000000'
      },
      xaxis: {
        title: "Year of Record",
        autotick: false,
        tick0: 2015,
        dtick: 1,
      },
      //plot_bgcolor: "#efeee7",
      yaxis: {
        title: "Divorce Rate (%)",
        range: [0,25],
        type: "linear",
      },
      yaxis2: {
        title: "DtoI Ratio",
        range: [0,4.5],
        type: "linear",
        overlaying: "y",
        side: "right"
      },
      //paper_bgcolor: 'rgba(0,0,0,0)',

      
    };

    Plotly.newPlot("bar-chart", data, layout, {responsive: true});

  });
}
