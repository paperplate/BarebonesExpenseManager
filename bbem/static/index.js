/*function run(dataset){
	d3PieChart(dataset[0], dataset[0]);
	d3BarChart(dataset[0]);
};

document.addEventListener("DOMContentLoaded", function(e){
	run([entries,user,category,source]);
});*/



const rolled = d3.rollup(
	entries,
	v => d3.sum(v, d => d.amount/100.0),
	d => d.category
);

const aggData = Array.from(rolled, ([category, total]) => ({category, total}));

const color = d3.scaleOrdinal()
	.domain(aggData.map(d => d.category))
	.range(d3.schemeCategory10);

(function drawPie() {
	const width = 600;
	const height = 600;
	const radius = Math.min(width, height) / 2;

	const svg = d3.select("#pieChart")
		.append("svg")
		//.attr("viewBox", `0 0 ${width} ${height}`)
		//.attr("preserveAspectRatio", "xMidYMid meet")
		//.style("width", "100%")
		//.style("height", "100%")
		.attr("width", width)
		.attr("height", height)
		.append("g")
		.attr("transform", `translate(${width/2},${height/2})`);
	
	const pie = d3.pie()
		.sort(null)
		.value(d => d.total);
	
	const arcs = pie(aggData);

	const arcGen = d3.arc()
		.innerRadius(0)
		.outerRadius(radius - 10);
	
	svg.selectAll("path")
		.data(arcs)
		.enter()
		.append("path")
		.attr("d", arcGen)
		.attr("fill", d => color(d.data.category))
		.attr("stroke", "#fff")
		.attr("stroke-width", 1);
	
	const labelArc = d3.arc()
		.innerRadius(radius * 0.6)
		.outerRadius(radius * 0.6);
	
	svg.selectAll("text")
		.data(arcs)
		.enter()
		.append("text")
		.attr("transform", d => `translate(${labelArc.centroid(d)})`)
		.attr("dy", "0.35em")
		.attr("text-anchor", "middle")
		.text(d => d.data.category);
})();
/*
(function drawBar() {
	const margin = {top:20, right:20, botton:30, left:40};
	const width = 500 - margin.left - margin.right;
	const height = 550 - margin.top - margin.bottom;

	const svg = d3.select("#barChart")
		.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", `translate(${margin.left},${margin.top})`);
	
	const x = d3.scaleBand()
		.domain(aggData.map(d => d.category))
		.range([0, width])
		.padding(0.2);
	
	const y = d3.scaleLinear()
		.domain([0, d3.max(aggData, d => d.total)])
		.nice()
		.range([height, 0]);
	
	svg.append("g")
		.attr("class", "axis")
		.attr("transform", `translate(0,${height})`)
		.call(d3.axisBottom(x));
	
	svg.append("g")
		.attr("class", "axis")
		.call(d3.axisLeft(y));
	
	svg.selectAll(".bar")
		.data(aggData)
		.enter()
		.append("rect")
		.attr("class", "bar")
		.attr("x", d => x(d.category))
		.attr("y", d => y(d.total))
		.attr("width", x.bandwidth())
		.attr("height", d => height - y(d.total))
		.attr("fill", d => color(d.category));
	
	svg.selectAll(".bar-text")
		.data(aggData)
		.enter()
		.append("text")
		.attr("class", "bar-text")
		.attr("x", d => x(d.category) + x.bandwidth() / 2)
		.attr("y", d => y(d.total) - 5)
		.text(d => d.total);
})();
/*const x = d3.scaleBand()
	.domain(d3.rollups(entries, (xs) => d3.sum(xs, x => x.amount/100.0), (d) => d.category))
	.range([margin.left, width - margin.right])
	.padding(0.1);

const y = d3.scaleLinear()
	.domain([d3.min(entries, (d) => d.amount/100.0), d3.max(entries, (d) => d.amount/100.0)])
	.range([height - margin.bottom, margin.top]);

const barChart = d3.select("#barChart")
	.append("svg")
	.attr("width", width)
	.attr("height", height)
	.attr("viewBox", [0, 0, width, height])
	.attr("style", "max-width: 100%; height: auto;");

barChart.append("g")
	.attr("fill", "steelblue")
	.selectAll()
	.data(entries)
	.join("rect")
	.attr("x", function(d){console.log(d.category);return x(d.category);})
	.attr("y", function(d){ return y(d.amount/100.0);})
	.attr("height", (d) => y(0) - y(d.amount/100.0))
	.attr("width", x.bandwidth());

barChart.append("g")
	.attr("transform", `translate(0,${height - margin.bottom})`)
	.call(d3.axisBottom(x).tickSizeOuter(0))
	.selectAll("text")
		.style("text-anchor", "end")
		.attr("dx", "-0.8em")
		.attr("dy", "0.15em")
		.attr("transform", "rotate(-65)");

barChart.append("g")
	.attr("transform", `translate(${margin.left},0)`)
	.call(d3.axisLeft(y).tickFormat((y)=>(y*100).toFixed()))
	.call(g => g.select(".domain").remove())
	.call(g => g.append("text")
		.attr("x", -margin.left)
		.attr("y", 10)
		.attr("fill", "currentColor")
		.attr("text-anchor", "start")
		.text("Amount"));
/*const outerRadius = Math.min(width,height) / 2;
const innerRadius = outerRadius * 0.5;

const barChart = d3.select("#barChart")
	.append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom);

const g = barChart.append("g")
	.attr("transform", `translate(${margin.left}, ${margin.top})`); 

const color = d3.scaleOrdinal().domain(category).range(d3.schemeCategory10);

const xscale = d3.scaleLinear()
	.domain(category)
	.range([0, width]);
const yscale = d3.scaleLinear()
	.domain([d3.min(entries), d3.max(entries)])
	.range([height, 0]);

const xaxis = d3.axisBottom().scale(xscale);
const yaxis = d3.axisLeft().scale(yscale);

g.append("g").classed("x.axis", true).attr("transform", `translate(0,${height})`).call(xaxis);
g.append("g").classed("y.axis", true).call(yaxis);
const group = g.append("g");

const marks = group.selectAll("circle")
	.data(entries)
	.join(
	(enter) => {
		const marks_enter = enter.append("circle");
		marks_enter.attr("r", 5).append("title");
		return marks_enter;
	},
	(update) => update,
	(exit) => {
		exit.remove();
	});

marks.style("fill", (d) => color(d.category))
	.attr("cx", (d) => xscale(d.category))
	.attr("cy", (d) => yscale(d.amount));

marks.select("title").text((d) => d.name);*/
