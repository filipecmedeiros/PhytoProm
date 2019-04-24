var margin = {top: 30, right: 30, bottom: 30, left: 80};
var width = 510- margin.left - margin.right;
var height = 510 - margin.top - margin.bottom;

//Dados
d3.csv('Log2.csv', function(dataset) {

    console.log(dataset);

//Escalas
var dataXinterval = d3.extent(dataset, d=>d["upstream"]);
var xScale = d3.scaleLinear().domain([0,1000]).range([0, width-margin.left]);

var dataYinterval = d3.extent(dataset, d=>d["promoter_id"]);;
var yScale = d3.scaleOrdinal().domain(dataYinterval).range([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, height-margin.top]);

var mySVG = d3.select('svg')
.append('g')
.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

//scatterplots
mySVG
.selectAll()
.data(dataset)
.enter()
.append('g')
.attr('Class', d=>d["name"])
.append('circle')
.attr("cx",d=>xScale(JSON.parse("[" + d["upstream"] + "]")))
.attr("cy",d=>yScale(d["promoter_id"]))
.attr("r",5);

mySVG
.selectAll('g')
.append('text')
.text(d=>d["name"])
.attr("class", "ecr")
.attr('x', d=>xScale(d["upstream"]))
.attr('y', d=>yScale(d["promoter_id"])-5)
.attr('display', 'none');


var xAxisGroup = mySVG.append('g')
                           .attr('class','xAxis')
                           .attr('transform','translate(0,'+(height-margin.top)+')');
var xAxis = d3.axisBottom(xScale);
xAxisGroup.call(xAxis);


var yAxisGroup = mySVG.append('g')
                           .attr('class','yAxis')
                           .attr('transform','translate(0, 0)');
var yAxis = d3.axisLeft(yScale);
yAxisGroup.call(yAxis);


mySVG.selectAll('g')
    .on('mouseover',function(d){
    d3.select(this).select('circle').attr('fill', 'red');
    d3.select(this).select('text').attr('display', 'true');
    });

mySVG.selectAll('g')
    .on('mouseout',function(d){
    d3.select(this).select('circle').attr('fill', 'black');
    d3.select(this).selectAll('.ecr').attr('display', 'none');
    });
});