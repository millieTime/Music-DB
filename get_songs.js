/*
Copy it, open your profile => thumbs.
Inspect Element => console
Paste the script in the console at the bottom.
*/
(function() {
    var pageSize = 100;
    var stationPageSize = 250; // IMPORTANT: This script only gets the first page of stations. If you have more than 250 this may be a problem, sorry.
    var webname = location.pathname.split("/").pop(); // Seems to be a variation of the username, can be retrieved from the URL
    var includeThumbsDown = true;

    var allThumbs = [];

    // Step one, obtain the AuthToken and CsrfToken which will allow us to make requests to the Pandora API.
    var authToken = undefined;
    var csrfToken = undefined;

    var originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
    XMLHttpRequest.prototype.setRequestHeader = function(name, value) { // If I had more time maybe I wouldn't need to use this hook
        if(name === "X-AuthToken") {
            authToken = value;
        }
        if(name === "X-CsrfToken") {
            csrfToken = value;
        }
        originalSetRequestHeader.apply(this, arguments);
        if(authToken && csrfToken) { // We've got them both, let's get a move on
            XMLHttpRequest.prototype.setRequestHeader = originalSetRequestHeader; // Deregister our hook...
            getStations(); // ...and get to work
        }
    };
    window.scrollTo(0,document.body.scrollHeight); // Scroll to the bottom of the page to trigger a load so we can hook the event

    // Step two, get a list of all stations
    function getStations() {
        var req = new XMLHttpRequest();
        req.open('POST', "/api/v1/station/getStations", true);
        req.setRequestHeader("Content-Type", "application/json"); // Pandora API rejects requests without this content type set
        req.setRequestHeader("X-AuthToken", authToken);
        req.setRequestHeader("X-CsrfToken", csrfToken);
        req.onreadystatechange = function() {
            if(req.readyState == XMLHttpRequest.DONE && req.status == 200) {
                var data = JSON.parse(req.responseText);
                var stations = [];
                for(var i = 0; i < data.stations.length; i++) {
                    stations.push(data.stations[i].stationId);
                }
                getTracks(stations);
            }
        };
        req.send(JSON.stringify({
            pageSize: stationPageSize
        }));
    };
    
    // Step three, fetch the tracks
    function getTracks(stations) {
        function callback() {
            currentStationId++;
            if(currentStationId < stations.length) {
                console.log("Getting tracks for station", currentStationId+1, "of", stations.length);
                fetchPage(stations[currentStationId], true, 0, callback);
            } else {
                finalize();
            }
        };
        var currentStationId = -1;
        callback();
    };
    
    function fetchPage(stationId, positive, pageNumber, callback) {
        var req = new XMLHttpRequest();
        req.open('POST', "/api/v1/station/getStationFeedback", true);
        req.setRequestHeader("Content-Type", "application/json"); // Pandora API rejects requests without this content type set
        req.setRequestHeader("X-AuthToken", authToken);
        req.setRequestHeader("X-CsrfToken", csrfToken);
        req.onreadystatechange = function() {
            if(req.readyState == XMLHttpRequest.DONE && req.status == 200) {
                var data = JSON.parse(req.responseText);
                data.feedback = data.feedback.map(function(item) {
                    item.type = item.isPositive ? "Thumbs Up" : "Thumbs Down";
                    return item;
                });
                allThumbs = allThumbs.concat(data.feedback);
                if(data.feedback.length > 0) {
                    fetchPage(stationId, positive, pageNumber+1, callback);
                } else {
                    if(positive && includeThumbsDown) {
                        fetchPage(stationId, false, 0, callback);
                    } else {
                        callback();
                    }
                }
            }
        };
        req.send(JSON.stringify({
            pageSize: pageSize,
            positive: positive,
            startIndex: pageNumber * pageSize,
            stationId: stationId
        }));
    }

    // Step four, compile the output
    function finalize() {
        var string = "Artist\tAlbum\tSong\tStation\tType\tAmazon Link\tiTunes Link\tDisc Number\tTrack Number\tDuration (Seconds)";
        for(var i = 0; i < allThumbs.length; i++) {
            var thumb = allThumbs[i];
            string += "\n" +
                thumb.artistName.replace(/\t/g, "    ").replace(/\n|\r/g, "") + "\t" +
                thumb.albumTitle.replace(/\t/g, "    ").replace(/\n|\r/g, "") + "\t" +
                thumb.songTitle.replace(/\t/g, "    ").replace(/\n|\r/g, "") + "\t" +
                thumb.stationName.replace(/\t/g, "    ").replace(/\n|\r/g, "") + "\t" +
                thumb.type + "\t" +
                thumb.amazonUrl + "\t" +
                thumb.itunesUrl + "\t" +
                thumb.discNum + "\t" +
                thumb.trackNum + "\t" +
                thumb.trackLength;
        }
        console.log(string);
    }
})();