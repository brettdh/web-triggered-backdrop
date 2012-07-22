function fillScreen() {
    $("#makefire").width($(document).width());
    $("#makefire").height($(document).height());
}

function make_fire(makefire) {
    console.log("Clicked fire");
    makefire.css('background-color', 'red');
    $.get("/trigger", function(data) {
        console.log("Got: " + data);
        makefire.css('background-color', 'black');
    }).error(function() {
        console.log("Error!");
        makefire.css('background-color', 'black');
    });
}

function register_event_handler(event_name) {
    $(document).ready(function() {
        fillScreen();
        
        $("#makefire").bind(event_name, function() {
            make_fire($(this));
        });
    });
}
