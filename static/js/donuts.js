"use strict";

function getWindowWidth() {
    return $(window).width();
}
$(window).resize( function() {
    initializeDonuts;
});


function initializeDonuts() {

        function plot_donuts(error,data) {

            if (error) throw error;
            console.log(data.columns);
            console.table(data);

            var margin = 50,
                width = getWindowWidth() - margin,
                height = 1000 - margin;

            d3.select(".donut-charts-title")
              .append("h3")
              .text("Visualizing Women Engineers in Tech");
            d3.select(".donut-charts-title")
              .append("p")
              // creatively obtained.
              .html("<p>Data visualization using d3.js.</p><p>Crowdsourced data by Tracy Chou. <a href='https://twitter.com/triketora' target='_blank'>@triketora</a></p>");

            var donutPadding = 25;

            var maxRadius = 100;
            var innerRadius = 25;

            var maxEng = d3.max(data, function(d) {
                return d['num_eng'];
            });
            var minEng = d3.min(data, function(d) {
                return d['num_eng'];
            });

            var highlight = "#00BCD4";

            // scales
            var color = d3.scaleOrdinal()
                .range([highlight, "steelblue"]);

            var r = d3.scaleSqrt()
                .domain([minEng, maxEng])
                .range([1, maxRadius]);

            var arc = d3.arc()
                .outerRadius(function(d) {
                    var outerRadius = innerRadius + d.data.radius;
                    d['outerRadius'] = outerRadius;
                    d['innerRadius'] = innerRadius;
                    return outerRadius; })
                .innerRadius(function(d) {
                    return innerRadius; });

            var pie = d3.pie()
                .sort(null)
                .value(function(d) {
                    return d.counts;
                });

            color.domain(d3.keys(data[0]).filter(function(key) {
                return key === "WOMEN" || key === "OTHER";
            }));

            data.forEach(function(d) {
                var pieRadius = r(d.num_eng);
                var percentFemale = d.percent_female_eng;
                d.piePercents = color.domain().map(function(gender) {
                    return {
                        gender: gender,
                        counts: +d[gender],
                        'radius': pieRadius,
                        'female': percentFemale
                    };
                });
            });

            // LEGEND
            var legend = d3.select(".donut-charts-legend").append("svg")
                .attr("class", "legend")
                .attr("width", 100)
                .attr("height", 50)
                .selectAll("g")
                .data(color.domain().slice())
                .enter().append("g")
                .attr("transform", function(d, i) { return "translate(0," + i * 30 + ")"; });
            legend.append("rect")
                .attr("width", 25)
                .attr("height", 25)
                .style("fill", color);
            legend.append("text")
                .attr("x", 30)
                .attr("y", 12)
                .attr("dy", ".35em")
                .text(function(d) { return d; });

            // DONUTS
            var svg = d3.select(".donut-charts-container").selectAll(".pie")
                .data(data)
                .enter()
                .append("svg")
                .attr("class", "pie")
                .attr("width", function(d) {
                    return (r(d.num_eng)+innerRadius+donutPadding)*2;
                })
                .attr("height", function(d) {
                    return (r(d.num_eng)+innerRadius+donutPadding)*2;
                })
                .append("g")
                .attr("transform", function(d) {
                    return "translate(" + (r(d.num_eng)+innerRadius+donutPadding) + "," + (r(d.num_eng)+innerRadius+donutPadding) + ")";});

            // company label
            svg.append("text")
                .attr("dy", function(d) {
                    return (15 + r(d.num_eng)+innerRadius); })
                .style("text-anchor", "middle")
                .text(function(d) { return d.key; });

            // ARCS
            var arcs = svg.selectAll(".arc")
                .data(function(d) { return pie(d.piePercents); })
                .enter()
                .append("svg:g")
                .attr("class", "arc");

            arcs.append("svg:path")
                .attr("d", arc)
                .style("fill", function(d) { return color(d.data.gender); })
                .style("stroke-width", 0);

            // data label
            arcs.on("mouseover", function(d) {
                d3.select(this)
                    .style("opacity", 0.8)
                    .append("svg:text")
                    .attr("text-anchor", "middle")
                    .attr("transform", function(d) {
                        var c = arc.centroid(d);
                        return "translate(" + c[0]*2.3 + "," + c[1]*1.8 + ")";
                    })
                    .style("fill", function(d) { return color(d.data.gender); })
                    .style("font-weight", "bold")
                    .text(function(d) { return d.data.counts; });
            });

            arcs.on("mouseout", function(d) {
                d3.select(this)
                    .style("opacity", 1.0)
                    .select("text").remove();
            });
        }

        d3.csv("../static/data/data_spreadsheet.csv", function(d) {
            d['num_eng'] = +d['num_eng'];
            d['WOMEN'] = +d['num_female_eng'];
            d['OTHER'] = +(d['num_eng'] - d['num_female_eng']);
            d['percent_female_eng'] = +(d3.format(".0f")(d['percent_female_eng']));
            d['percent_other_eng'] = 100. - d['percent_female_eng'];
            d['last_updated'] = d3.timeParse("%m/%d/%Y")(d['last_updated']);
            return d;
        }, plot_donuts);

}
