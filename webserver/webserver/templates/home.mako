<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Name That Episode</title>
        <meta name="viewport" content="width-device-width, initial-scale=1">
        <link href="static/style.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    </head>

    <body class="container">
        <main role="main" class="flex-shrink-0">
            <div class="container text-center">
                <input type="text" style="margin: 15px;" class="form-control form-control-lg" id="answer" placeholder="Episode name">

                <h4><span id="timer">60</span> seconds remaining.</h4>

                <a id="rules-link" href="#">Rules</a>
                <div id="rules" style="display:none;">
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Accepted answer is the exact episode name only.</li>
                        <li class="list-group-item">3 clues per episode are available, you lose one point per clue.</li>
                        <li class="list-group-item">You are given 60 seconds to answer correctly.</li>
                        <li class="list-group-item">NO CHEATING!</li>
                      </ul>
                </div>
                <hr>
                <div class="row">
                    <div class="col-sm">
                        <p class="text-muted">History</p>
                        <ul id="changelog" class="list-group">
                            
                            <li class="list-group-item"><span class="score minus">-1</span> Added new clue</li>
                            <li class="list-group-item"><span class="score minus">-1</span> 20 Seconds elapsed</li>
                            <li class="list-group-item"><span class="score plus">+2</span> Correctly answered Season 04 Episode 20 - The Nightwalker</li>
                            
                        </ul>
                    </div>

                    <div class="col-lg">
                        <audio controls id="audio" src=""></audio> <p>Eligible points: <span id="points">3</span></p>
                        <p>Total points accumulated: <span id="total">0</span>/<span id="maxPoints"></span></p>
                        <p><span id="correctAnswers">0</span> correct answers</p>
                        <button type="button" id="clue" class="btn btn-warning" name="Give me another clue">Give me another clue</button>
                        <button type="button" id="next" class="btn btn-danger" name="I give up, next episode">I give up, next episode</button>

                        <div style="margin-top: 10px;" class="form-check-inline form-switch">
                            <input class="form-check-input" type="checkbox" id="showDetailedInfo">
                            <label class="form-check-label" for="flexSwitchCheckDefault">Show detailed episode info</label>
                        </div>
                    </div>
                </div>
            </div>
        </main>

          
        <div class="modal fade" id="episodeModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="episodeTitle"></h5>
                    <h7 id="episodeNumber"></h7>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <img src="static/implant.jpg"/>
                        <p>Capt. Picard finds himself shifting continually into the past, future and present and must use that to discover a threat to humanity's existence.</p>
                        <p><a href="#">Thumbnail snapshot isn't a clear indicator of episode</a></p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button id="closeModal" type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
                </div>
            </div>
        </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>


    <script type="text/javascript">
        let data = ${data | n}
    </script>

    <script type="text/javascript" src="static/guessthatepisode.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
    </body>
</html>