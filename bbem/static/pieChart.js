"use strict";
/*
const pieChart = d3.select("#pieChart") = {

	console.log("piechart");
	console.log(entries);
	const margin = {top:20, right:20, botton:30, left:40};
	const width = 350 - margin.left - margin.right;
	const height = 350 - margin.top - margin.bottom;
	const outerRadius = Math.min(width, height) / 2;
	const innerRadius = outerRadius * 0.5;
	const color = d3.scaleOrdinal(d3.schemeObservable10);

	const svg = d3.create("svg")
		.attr("viewBox", [-width/2, -height/2, width, height]);

	const arc = d3.arc()
		.innerRadius(innerRadius)
		.outerRadius(outerRadius);

	const pie = d3.pie().sort(null).value((d) => d["amount"]);

	const path = svg.datum(entries).selectAll("path")
		.data(pie)
		.join("path")
		.attr("fill", (d,i) => color(i))
		.attr("d", arc)
		.each(function(d) { this._current = d; });

	function change(value) {
		pie.value((d) => d[value]);
		path.data(pie);
		path.transition().duration(750).attrTween("d", arcTween);
	}

	function arcTween(a) {
		const i = d3.interpolate(this._current, a);
		this._current = i(0);
		return (t) => arc(i(t));
	}

	return Object.assign(svg.node(), {change});

}
/* 
function d3PieChart(dataset, chart) {
	const margin = {top:20, right:20, botton:30, left:40};
	const width = 350 - margin.left - margin.right;
	const height = 350 - margin.top - margin.bottom;
	const outerRadius = Math.min(width, height) / 2;
	const innerRadius = outerRadius * 0.5;
	const color = d3.scaleOrdinal(d3.schemeObservable10);



	const mychart = d3.select("#pieChart")
		.append("svg")
		.data([dataset])
		.attr("width", width)
		.attr("height", height)
		.append("g")
		.attr("transform", "translate(" + outerRadius + "," + outerRadius + ")");

	const data = d3.pie()
		.sort(null)
		.value(function(d){return d.value;})(dataset);

	const arc = d3.arc()
		.outerRadius(outerRadius)
		.innerRadius(0);

	const innerArc = d3.arc()
		.innerRadius(innerRadius)
		.outerRadius(outerRadius);

	const arcs = mychart.selectAll("g.slice")
		.data(data)
		.enter()
		.append("svg:g")
		.attr("class", "slice")
		.on("click", click);

	arcs.append("svg:path")
		.attr("fill", function(d,i){ return color(i); })
		.attr("d", arc)
		.append("svg:title")
		.text(function(d){ return d.data.category + ": " + d.data.amount + "%"; });

	d3.selectAll("g.slice")
		.selectAll("path")
		.transition()
		.duration(200)
		.delay(5)
		.attr("d", innerArc);

	arcs.filter(function(d){ return d.endAngle - d.startAngle > 0.1; })
		.append("svg:text")
		.attr("dy", "0.2em")
		.attr("text-anchor", "middle")
		.attr("transform", function(d){ return "translate(" + innerArc.centriod(d) + ")"; })
		.text(function(d){ return d.data.category; });

	mychart.append("svg:text")
		.attr("dy", "0.20em")
		.attr("text-anchor", "middle")
		.text("aaa")
		.attr("class", "title");

	function click(d, i){
		updateBarChart(d.data.category, color(i), datasetBarChart);
	} */
//}

