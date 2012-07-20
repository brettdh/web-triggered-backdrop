var get_published_text = function() {
    $.get("/published_text", function(data) {
        if (data.match(/quit/)) {
            console.log("Done.");
        } else {
            console.log("Got data: " + data);
            // $("#published").append(data);
            
            audio = $("audio").get(0);
            video = $("video").get(0);
            audio.currentTime = 0;
            video.currentTime = video.duration;

            audio.play();
            video.play();

            get_published_text();
        }
    }).error(function() {/* ignore */});
};

$(document).ready(get_published_text);
