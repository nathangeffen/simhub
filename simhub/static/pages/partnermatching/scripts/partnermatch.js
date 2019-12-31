"use strict";

var numAgents = 16;
var ndrawn = false;
var nsqdrawn = false;

var drawCircle = function(Root, i, j)
{
    var prevCircle = document.getElementById("c" + j + "_" + (i - 1) );
    var newCircle = prevCircle.cloneNode(true);
    var prevText = document.getElementById("t" + j + "_" + (i - 1) );
    var newText = prevText.cloneNode(true);
    newCircle.id = "c" + j + "_" + i;
    newText.id = "t" + j + "_" + i;
    var move="translate(" + (35*i) + "," + 0 + ")";
    newCircle.setAttribute("transform",move);
    newText.setAttribute("transform",move);
    Root.appendChild(newCircle);
    Root.appendChild(newText);
    document.getElementById(newText.id).textContent = i;
}

var run_nEvent = function()
{
    var i = 0;
    jQuery.whileAsync({
	delay: 400,
	bulk: 0,
	test: function() { return i < numAgents; },
	loop: function()
	{
	    var circle = document.getElementById("c0_" + i);
	    if (i > 0) {
		document.getElementById("c0_" + (i - 1) ).
		    setAttribute("stroke", "black");
		document.getElementById("c0_" + (i - 1) ).
		    setAttribute("stroke-width", "2");
	    }
	    circle.setAttribute("stroke", "red");
	    circle.setAttribute("stroke-width", "6");
	    ++i;
	},
	end: function()
	{
	    document.getElementById("c0_" + (numAgents-1) ).
		setAttribute("stroke", "black");
	    document.getElementById("c0_" + (numAgents-1) ).
		setAttribute("stroke-width", "2");
	    document.getElementById("nevent-button").disabled = false;
	}
    });
}


var nEvent = function()
{
    document.getElementById("nevent-button").disabled = true;
    var Root=document.getElementById("svg1");
    Root.style.display = "block";
    var i = 1;
    if (ndrawn == false) {
	ndrawn = true;
	jQuery.whileAsync({
	    delay: 50,
	    bulk: 0,
	    test: function() { return i < numAgents; },
	    loop: function()
	    {
		drawCircle(Root, i, 0);
		++i;
	    },
	    end: function() {
		run_nEvent();
	    }
	});
    } else {
	run_nEvent();
    }
}

var run_nsqEvent = function()
{
    var i = 0, j = 1;
    var circle = document.getElementById("c1_0");
    circle.setAttribute("stroke", "red");
    circle.setAttribute("stroke-width", "6");
    jQuery.whileAsync({
	delay: 200,
	bulk: 0,
	test: function() { return i < numAgents; },
	loop: function()
	{
	    if (j == numAgents) {
		++i;
		document.getElementById("c1_" + (j - 1) ).
		    setAttribute("stroke", "black");
		document.getElementById("c1_" + (j - 1) ).
		    setAttribute("stroke-width", "2");
		circle = document.getElementById("c1_" + i);
		if (i > 0) {
		    document.getElementById("c1_" + (i - 1) ).
			setAttribute("stroke", "black");
		    document.getElementById("c1_" + (i - 1) ).
			setAttribute("stroke-width", "2");
		}
		if (i < numAgents) {
		    circle.setAttribute("stroke", "red");
		    circle.setAttribute("stroke-width", "6");
		}
		j = i + 1;
	    } else {
		circle = document.getElementById("c1_" + j);
		if (j > i + 1) {
		    document.getElementById("c1_" + (j - 1) ).
			setAttribute("stroke", "black");
		    document.getElementById("c1_" + (j - 1) ).
			setAttribute("stroke-width", "2");
		}
		circle.setAttribute("stroke", "blue");
		circle.setAttribute("stroke-width", "6");
		++j;
	    }
	},
	end: function()
	{
	    document.getElementById("c1_" + (numAgents-1) ).
		setAttribute("stroke", "black");
	    document.getElementById("c1_" + (numAgents-1) ).
		setAttribute("stroke-width", "2");
	    document.getElementById("nsqevent-button").disabled = false;
	}
    });
}


var nsqEvent = function()
{
    document.getElementById("nsqevent-button").disabled = true;
    var Root=document.getElementById("svg2");
    Root.style.display = "block";
    var i = 1;
    if (nsqdrawn == false) {
	nsqdrawn = true;
	jQuery.whileAsync({
	    delay: 50,
	    bulk: 0,
	    test: function() { return i < numAgents; },
	    loop: function()
	    {
		drawCircle(Root, i, 1);
		++i;
	    },
	    end: function() {
		run_nsqEvent();
	    }
	});
    } else {
	run_nsqEvent();
    }
}
