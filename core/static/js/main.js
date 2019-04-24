/**
 * main.js
 * Filipe Cordeiro de Medeiros Azevedo
 * Cis-Element visualization by promoter
*/

var margin = {'left': 150, 'right': 15, 'top': 10, 'bottom': 100};

var width = 900 - margin.left - margin.right;
var height = 600 - margin.top - margin.bottom;

var g = d3.select("#chart-area")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", "translate(" + margin.left 
                + ", " + margin.top + ")")

d3.json("{{ json }}").then(function(data){
    console.log(data);

    var y = d3.scaleBand()
        .domain(data.map(function(d){
            return d.promoter;
        }))
        .range([0, height])
        .paddingInner(0.3)
        .paddingOuter(1);

    var x = d3.scaleLinear()
        .domain([0,1000])
        .range([0,width]);
    
    var color = d3.scaleSequential(d3.interpolateRainbow);
    var cisElement = d3.scaleBand()
        .domain(data.map(function(d){
            return d.name;
        }))
        .range([0,1]);

    var line = g.selectAll("line")
        .data(data);

    line.enter()
        .append('line')
            .attr('x1', 0)
            .attr('y1', (d,i)=>y(d.promoter))
            .attr('x2', width)
            .attr('y2', (d,i)=>y(d.promoter))
            .attr('stroke-width', 1)
            .attr('stroke', 'black');


    var circleGroups = g.selectAll("g.circles")
    .data(data)
        .enter()
        .append("g")
        .attr("class", "circles");

    var circle = circleGroups.selectAll("circle")
            .data(getCircleData)
        .enter()
            .append("circle")
            .attr("cy", function(d){
                return y(d.promoter)
            })
            .attr("cx", function(d){
            return x(d.upstream)
            })
            .attr("r", 5)
            .attr("fill", function(d) {
                return color(cisElement(d.name));
            })
            .attr("stroke-width", 1)
            .attr("stroke", "black");

    function getCircleData(d) {
        var cdata = d.upstream.map (function(ele) { 
            return {upstream: ele, promoter: d.promoter, name:d.name};
        });
        
        return cdata; 
    }

    var yAxisGroup = d3.selectAll('svg').append('g')
                           .attr('class','yAxis')
                           .attr('transform','translate(' + margin.left + ', 0)');
    var yAxis = d3.axisLeft(y);
    yAxisGroup.call(yAxis);


    var xAxisGroup = d3.selectAll('svg').append('g')
                           .attr('class','xAxis')
                           .attr('transform','translate('+margin.left+','+height+')');
    var xAxis = d3.axisBottom(x);
    xAxisGroup.call(xAxis);

}).catch(function(error){
    console.log(error);
});