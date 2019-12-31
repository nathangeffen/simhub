"use strict";

var X_INIT = 45;
var Y_INIT = 45;
var RADIUS = 20;
var DELAY = 150;
var CLUSTERS = 4;
var NEIGHBORS = 6;

var agents = [];
var occupied = [];
var stage = 0;
var clusters = 0;
var neighbours = 0;


var sleep = function(miliseconds) {
    var currentTime = new Date().getTime();

    while (currentTime + miliseconds >= new Date().getTime()) {
    }
}

var output = function(str)
{
    document.getElementById("action-desc").innerHTML = str;
}

var cluster = function(agent)
{
    return (Math.random() * 10).toFixed(1);
}

var compare = function(a, b)
{
    return a.weight < b.weight;
}

var undrawAgent = function(agent)
{
    var svgArea = document.getElementById("cluster-shuffle-svg");
    svgArea.removeChild(agent.shape);
    svgArea.removeChild(agent.weightText);
    svgArea.removeChild(agent.idText);
}

var drawAgentAtPos = function(agent, x, y, r)
{
    var svgArea = document.getElementById("cluster-shuffle-svg");

    if (agent.shape == null) {
	agent.shape = document.createElementNS("http://www.w3.org/2000/svg",
					       "circle");
	agent.weightText = document.createElementNS("http://www.w3.org/2000/svg",
						    "text");
	agent.idText = document.createElementNS("http://www.w3.org/2000/svg",
						"text");
    }
    svgArea.appendChild(agent.shape);
    svgArea.appendChild(agent.idText);
    svgArea.appendChild(agent.weightText);

    agent.shape.setAttribute("cx", x);
    agent.shape.setAttribute("cy", y);
    agent.shape.setAttribute("r",  r);
    agent.shape.setAttribute("fill", "red");
    setTimeout(function(){
	agent.shape.setAttribute("fill", "white");
    }, DELAY / 2);
    agent.shape.setAttribute("stroke", "black");
    agent.weightText.setAttribute("font-family", "sans-serif");
    agent.weightText.setAttribute("font-size", "12px");
    agent.weightText.setAttribute("x", x - 0.3 * r)
    agent.weightText.setAttribute("y", y + 0.3 * r);
    agent.weightText.textContent = agent.weight;
    agent.idText.setAttribute("font-family", "sans-serif");
    agent.idText.setAttribute("font-size", "12px");
    agent.idText.setAttribute("x", x - 0.3 * r)
    agent.idText.setAttribute("y", y - r - 5);
    agent.idText.textContent = agent.id;
}

var drawAgent = function(agent, position)
{
    if (occupied[position])  {
	undrawAgent(occupied[position]);
	drawAgentAtPos(agent, (position + 1) * X_INIT, Y_INIT, RADIUS);
	if (agent.position >= 0) {
	    drawAgentAtPos(occupied[position], (agent.position + 1) * X_INIT, Y_INIT, RADIUS);
	    occupied[position].position = agent.position;
	    occupied[agent.position] = occupied[position];
	}
    } else {
	drawAgentAtPos(agent, (position + 1) * X_INIT, Y_INIT, RADIUS);
    }
    occupied[position] = agent;
    agent.position = position;
}

var drawAgents = function(agents) {
    var j = 0;
    for (var i = 0; i < agents.length; ++i) {
	window.setTimeout(function() {
	    drawAgent(agents[j], j) ;
	    j = j + 1;
	}, i * DELAY);
    }
}

var clusterShuffle = function(numAgents)
{
    if (stage == 0) {
	agents = initialize(numAgents);
	document.getElementById("cluster-shuffle-button").value = "Sort";
    }
    else if (stage == 1) {
	sortAgents(agents);
	document.getElementById("cluster-shuffle-button").value = "Shuffle";
    } else if (stage == 2) {
	DELAY = 1000;
	shuffleClusters(agents);
	document.getElementById("cluster-shuffle-button").value = "Restart";
	stage = -1;
    }
    ++stage;
}

var initialize = function(numAgents)
{
    occupied = [];
    var agents = [];
    var svgArea = document.getElementById("cluster-shuffle-svg");

    output("Initialising");
    while (svgArea.firstChild) {
	svgArea.removeChild(svgArea.firstChild);
    }

    var j = 0;
    for (var i = 0; i < numAgents; ++i) {
	agents[i] = {
	    id: i,
	    weight: cluster(agents[i]),
	    position: -1
	};
    }
    drawAgents(agents);
    return agents;
}

var sortAgents = function(agents)
{
    output("Sorting");
    agents.sort(compare);
    drawAgents(agents);
}

var shuffle = function(agents, first, last)
{
    for (var i = (last - first) - 1; i > 0; --i) {
	var j = Math.floor(Math.random() * (i + 1));
	var tmp = agents[first + i];
	agents[first + i] = agents[first + j];
	agents[first + j] = tmp;
    }
}

var shuffleClusters = function(agents)
{
    var clusterSize = agents.length / CLUSTERS;

    output("Shuffling with cluster value = " + CLUSTERS + " and cluster size = " + clusterSize );

    for (var i = 0; i < CLUSTERS; ++i) {
	var first = i * clusterSize;
	var last = (i + 1) * clusterSize;
	shuffle(agents, first, last);
    }
    drawAgents(agents);
}
