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
      buildPlot(firstFIPS);
      buildScatter(2015);
    });
  }

// event handler for year selector
function yearChanged (newYear) {
    console.log(`New Year Selected: ${newYear}`);

    // call function to refresh scatter plot with new year
    buildScatter(newYear);

    // call function to refresh map with new year
    // PLACEHOLDER: call Mike H's function here passing in newYear as argument
   // d3.select('#map-title').text(`${newYear} - Debt to Income Ratio`);
    d3.select('#county-map').select('img').attr("src", `/static/img/country-${newYear}.png`);
}

// event handler for county selector
function countyChanged (newCountyFIPS) {
    console.log(`New County Selected: ${newCountyFIPS}`);

    // call function to refresh Bar Chart with new county
    buildPlot(newCountyFIPS);
}

// event handler for case study
function toggleMap(textObject) {

    var textElement = d3.select(textObject);
    var textId = textElement.attr("id");
    if (textId == "Idaho") {
        // update text element link
        textElement.text("Click for Country Map");
        textElement.attr("id", "Country");

        // update image
        d3.select('#county-map').select('img').attr("src", `/static/img/idaho.png`);


    } else {
        // update text element link
        textElement.text("Click for 'Idaho' Case Study");
        textElement.attr("id", "Idaho");
        
        // get current year from selector
        var selector = d3.select("#selYear");
        var currentYear = selector.node().value;
        
        // update image
        d3.select('#county-map').select('img').attr("src", `/static/img/country-${currentYear}.png`);
    }
}
// setup code to be executed after the page is loaded
window.addEventListener('load', function () {
    console.log('page loaded');

    // initialize the page
    init();
  });
