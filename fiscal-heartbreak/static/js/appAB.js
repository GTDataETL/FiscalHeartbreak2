
/* global Plotly */
var url =`/api/fiscal-heartbreak/county/`;

function buildPlot(FIPS) {

  api_url = url+FIPS;

function buildPlot(FIPS) {
  var FIPS_url = url+FIPS;
  d3.json(FIPS_url).then(function(data) {
  d3.json(api_url).then(function(data) {

    // Grab values from the data json object to build the plots
    var county = data.County;
    var state = data.State;
    var year = data.Years;
    var div_pct = data.DivorcedPct;
    var DtoI = data.DtoI;

    var trace1 = {
      type: "bar",
<<<<<<< Updated upstream
      name: 'Divorce %',
=======
      name: "Divorce %",
>>>>>>> Stashed changes
      x: year,
      y: div_pct,
      marker: {
        color: "#17a2b8"
      }
    };

    var trace2 = {
      type: "bar",
<<<<<<< Updated upstream
      name: 'Debt to Income Ratio',
=======
      name: "Debt to Income Ratio",
>>>>>>> Stashed changes
      x: year,
      y: DtoI,
      marker: {
        color: "#000000"
<<<<<<< Updated upstream
      },
      textposition: 'auto'
=======
      }
>>>>>>> Stashed changes
    };

    var data = [trace1, trace2];

    var layout = {
<<<<<<< Updated upstream
      title: `${county}, ${state} - Divorce Rates and Debt to Income Ratio (2015-2017)`,

      xaxis: {
        title: 'Year',
=======
      title: `${county}, ${state} - Divorce Percentage vs. Debt to Income Ratio`,
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
>>>>>>> Stashed changes
        autotick: false,
        tick0: 2015,
        dtick: 1,
      },
      plot_bgcolor: "#efeee7",
      yaxis: {
<<<<<<< Updated upstream
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
=======
        title: "Divorce Rate (%) vs. DtoI Ratio",
        autorange: true,
        type: "linear",
      },
      paper_bgcolor: 'rgba(0,0,0,0)',

      
>>>>>>> Stashed changes
    };

    Plotly.newPlot("bar-chart", data, layout, {responsive: true});

  });
}
}
