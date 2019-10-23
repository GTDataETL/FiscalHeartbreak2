var scatter_url =`/api/fiscal-heartbreak/year/`;


function buildScatter(arg_year) {
    api_url = scatter_url + arg_year;

    d3.json(api_url).then(function(data) {
        
        
        var year = year;
        var diRatio = [];
        var divPct = [];
        var countyNames = [];

        Object.entries(data).forEach(([key, value]) => {
            diRatio.push(value.DtoI[0]);
            divPct.push(value.DivorcedPct[0]);
            countyNames.push(value.County);
        });

        var trace1 = {
            x: diRatio,
            y: divPct,
            mode: "markers",
            type: "scatter",
            name: countyNames,
            text: "Debt-to-Income Ratio: ",
            marker: {size: 12}
        };

        // var trace2 = {
        //     x: [],
        //     y: [],
        //     mode: 'lines',
        //     name: 'Linear Regression'
        // }

        var data = [trace1];

        var layout = {
            xaxis: {
                range: [0, 5]
            },
            yaxis: {
                range: [0, 100]
            },
            title:"Selected Year: "+year
        };

        Plotly.newPlot("scatter-plot", data, layout);
    });
}