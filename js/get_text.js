var fireball = null;
var bomb = null;

function setProgress(text) {
    $("#progress").html(text);
}

function fadeProgress() {
    $("#progress").fadeOut(1000);
}

var get_published_text = function() {
    $.get("/published_text", function(data) {
        if (data.match(/quit/)) {
            console.log("Done.");
        } else {
            console.log("Got data: " + data);
            // $("#published").append(data);
    
            
            fireball.jPlayer("play", 0);
            bomb.jPlayer("play", 0);
            
            get_published_text();
        }
    }).error(function() {/* ignore */});
};

function load_fireball() {
    fireball.jPlayer({
        ready: function () {
            $(this).jPlayer("setMedia", {
                m4v: "/media/fireball.mp4"
            });
        },
        supplied: "m4v",
        swfPath: "/js",
        fullScreen: true,
        preload: "auto",
        loadeddata: function() {
            setProgress("Done");
            fadeProgress();
        }
    });
}

$(document).ready(function () {
    fireball = $("#fireball");
    bomb = $("#bomb");
    
    bomb.jPlayer({
        ready: function() {
            $(this).jPlayer("setMedia", {
                mp3: "/media/bomb.mp3"
            });
        },
        supplied: "mp3",
        swfPath: "/js",
        preload: "auto",
        loadeddata: load_fireball
    });
    
    get_published_text();
});
