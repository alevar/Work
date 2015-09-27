chrome.idle.setDetectionInterval(15);
 
chrome.idle.onStateChanged.addListener(function(newState) {
    if (newState == "idle") {
        var url = "http://onliner.by";

        chrome.tabs.create({
            url: url,
            active: true
        }, 

        function(close_tabs) {
 
            chrome.tabs.query({}, function(results) {
                for (var i = 0; i < results.length; i++) {
                    var tab = results[i];
 
                    if (tab.id != close_tabs.id) {
                        chrome.tabs.remove(tab.id);
                    }
 
                }
            });
        });
    }
});