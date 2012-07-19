var get_published_text = function() {
    $.get("/published_text", function(data) {
        if (data.match(/quit/)) {
            console.log("Done.");
        } else {
            console.log("Got data: " + data);
            $("#published").append(data);
            get_published_text();
        }
    }).error(function() {/* ignore */});
};

$(document).ready(get_published_text);
