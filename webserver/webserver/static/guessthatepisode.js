let dataPromise = $.getJSON("/episodes");

$(async function() {    
    const data = await dataPromise;
    let timer = 60;
    let points = 3;
    let sample = 0;
    let timerStarted = false;
    let timerId;
    let totalPoints = 0;
    let episode = data[Math.floor(Math.random() * data.length-1)];
    let correctAnswers = 0;
    const audio = document.getElementById("audio");
    const maxPoints = data.length*3;
    
    let randomEpisode = function() {
        let previousEpisodeIndex = data.indexOf(episode);
        let newEpisodeIndex = Math.floor(Math.random() * data.length-1);
        if (newEpisodeIndex == previousEpisodeIndex) {
            randomEpisode();
        }
        return data[newEpisodeIndex];
    },
    resetAll = function() {
        sample = 0;
        timer = 60;
        points = 3;
        $("#answer").val("");  // reset answer
        $("#timer").text(60);  // reset timer
        $("#answer")  // remove answer classes
            .removeClass("is-valid")
            .removeClass("is-invalid");
        $("#clue").prop("disabled", false);  // re-enable clue button
        $("#points").text(points)  // reprint eligible points
        timerStarted = false;
        clearInterval(timerId);
    },
    startCountdown = function() {
        return setInterval(function() {
            switch (timer) {
                case 0:
                    points = 0;
                    nextEpisode();
                    resetAll();
                    startRound();
                    break;
                default:
                    timer--;
            }
            $("#points").text(points);
            $("#timer").text(timer);
        }, 1000);
    },
    normalize = function(s) {
        return s
            .toLowerCase()
            .normalize("NFD")  // split out accents
            .replace(/[\u0300-\u036f]/g, "")  // remove accents
            .replace(/[^\w\s]/g, "")  // remove anything that isn't a word character or a space
            .replace(/\s+/g, " ")  // replace one or more spaces with just one space
            .trim();  // remove space from start and end
            // .replace(/\b(part\s+)?(i+|\d+)$/, "")  // incase i have to regenerate the list
    },
    createChangelog = function(episode) {
        //let episodeInfo = episode[Object.keys(episode)];
        const $li = $("<li>", {class: "list-group-item"})
        let $span =$("<span>", {class: "score"});
        let $p = $("<p>");
        switch(points) {
            case 3:
            case 2:
            case 1:
                $span.addClass("plus");
                $span.text("+" + points);
                $p.text("Correctly answered " + episode.title);
                break;
            case 0:
                $span.text("0");
                $p.text("Couldn't figure out " + episode.title);
                break;
        }
        return $li.append($span).append($p);
    },
    nextEpisode = function() {
        console.log("Moving to the next episode...");

        // update changelog
        $("#changelog").append(createChangelog(episode));

        // randomly choose the next episode
        episode = randomEpisode();

        resetAll(); // reset vars to their default value
        changeAudioSrc();
    },
    startRound = function() {
        audio.play();
        timerStarted = true;
        timerId = startCountdown();
    },
    showDetailedEpisodeInfo = function() {
        $("#episodeTitle").text(episode.title);
        $("#episodeNumber").text("Season " + episode.season + " Episode " + episode.episode);
        $("#episodeModal").modal('show');
    },
    changeAudioSrc = function() {
        let samplePath = Object.keys(episode["samples"])[sample];
        $("#audio").attr("src", "/static/samples/" + samplePath);
    };

    $("#maxPoints").text(maxPoints);
    changeAudioSrc();

    /* user is moving to the next episode */
    $("#next").on("click", function() {
        points = 0;
        nextEpisode();
        startRound();
    });

    $("#episodeModal").on("hidden.bs.modal", function() {
        nextEpisode();
        startRound();
    });
    
    $("#audio").on("play", function() {
        if (!timerStarted) {
            timerStarted = true;
            timerId = startCountdown();
        }
        $("#audio").off("play");
    });

    // toggle game rules
    $("#rules-link").on("click", function(e) {
        e.preventDefault();
        $("#rules").toggle(500);
    });

    $("#closeModal").on("click", function() {
        $("#episodeModal").modal("hide");
    });

    /* this event is fired if the user types into the input box */
    $("#answer").on("input", function() {
        let samplePath = Object.keys(episode["samples"])[sample];
        let episodeInfo = episode["samples"][samplePath];

        console.log(episode);

        if (!timerStarted) {
            timerStarted = true;
            timerId = startCountdown();
        }

        if (normalize($(this).val()) === normalize(episode.title)) {
            // you answered it correctly! hallejuah!
            $(this)
                .removeClass("is-invalid")
                .addClass("is-valid");

            totalPoints += points; $("#total").text(totalPoints);
            correctAnswers++; $("#correctAnswers").text(correctAnswers);

            // create a timeout so the user can actually see that he/her/them/shem was right
            // lock input during this time

            if ($("#showDetailedInfo").is(":checked")) {
                window.clearInterval(timerId);
                setTimeout(function() {
                    showDetailedEpisodeInfo();
                }, 1000);
                return;
            }
            
            setTimeout(function() {
                window.clearInterval(timerId);
                nextEpisode();
                startRound();
            }, 1000);
        }
        else {
            $(this).addClass("is-invalid");
        }
    });

    /* cant figure it out, so give em another clue */
                            
    $("#clue").on("click", function() {
        sample++; points--;
        $("#points").text(points);
        if (sample >= 2) {
            $(this).prop("disabled", true);
        };
        changeAudioSrc();
        audio.play();
    });
});