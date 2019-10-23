var api_url =`/api/fiscal-heartbreak`;

function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selCounty");
  
    var firstFIPS = "";

    // Use the list of sample names to populate the select options
    d3.json(api_url).then((counties) => {
      Object.entries(counties).forEach(([fips, county]) => {
        
        // if this is the first sample, store away the FIPS for later
        if (firstFIPS == "") {
            firstFIPS = fips;
        }

        // append fips and text to drop-down selector
        selector
          .append("option")
          .text(`${county.County}, ${county.State}`)
          .property("value", fips);
      });
  
      // Use the first sample from the list to build the initial plots
      buildPlot(counties[firstFIPS]);
    });
  }

// event handler for year selector
function yearChanged (newYear) {
    console.log(`New Year Selected: ${newYear}`);

    // call function to refresh scatter plot with new year
    // PLACEHOLDER: call Joseph's function here passing in newYear as argument

    // call function to refresh map with new year
    // PLACEHOLDER: call Mike H's function here passing in newYear as argument
}

// event handler for county selector
function countyChanged (newCountyFIPS) {
    console.log(`New County Selected: ${newCountyFIPS}`);

    // call function to refresh Bar Chart with new county
    buildPlot(newCountyFIPS);
}

// initialize the page
init();