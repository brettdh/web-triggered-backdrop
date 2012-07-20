$(document).ready(function() {
    $("#makefire").click(function() {
        console.log("Clicked fire");
        $.get("/trigger", function(data) {
            console.log("Got: " + data);
        }).error(function() {
            console.log("Error!");
        });
    });
});
