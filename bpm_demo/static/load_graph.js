$(document).ready(function() {
        var element = document.getElementById('graph-914')
        var options = {
            width: parseFloat(getComputedStyle(element, null).width.replace("px", "/")),
            height: 1000,
            layout: 'LR',
            resizeHeight: true,
        };

        /* only once definition from console */
        var definition = JSON.parse(document.getElementById('definition').innerText);
        var elementId = '#graph-914';
        /* sample of recurring events from output from java program */
        var events =  JSON.parse(document.getElementById('events').innerText);
        var graph = new sfn.StateMachineExecutionGraph(definition, events, elementId, options);
        graph.render();
});