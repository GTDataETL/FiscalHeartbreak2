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
            countyNames.push(`${value.County},${value.State} FIPS:${value.FIPS}`);
        });

        var trace1 = {
            x: diRatio,
            y: divPct,
            mode: "markers",
            type: "scatter",
            text: countyNames,
        //    name: "Debt-to-Income Ratio",
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
            hovermode:"closest",
            hoverdistance:"1",
            xaxis: {
                range: [0, 4]
            },
            yaxis: {
                range: [0, 26]
            },
            title:"Selected Year: "+arg_year
        };

        Plotly.newPlot("scatter-plot", data, layout);
        var scatterPlot = document.getElementById("scatter-plot");
        scatterPlot.on('plotly_click', data => {

            console.log("scatter clicked");
            // get text label of point clicked
            var dataText = data.points[0].text;
            console.log(dataText);

            // split text label on : to get FIPS code
            var chunks = dataText.split(":");
            var newFIPS = chunks[1];

            // change county selector based on click event
            d3.select('#selCounty').property('value', newFIPS);
            
            // call function to refresh Bar Chart with new county
            buildPlot(newFIPS);
        });
    });
}