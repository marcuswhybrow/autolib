
var pageRealtimeTwitterReactionsHTML = [];
var pageRealtimeTwitterReactionsTimeStamps = [];

(function($) {
	/*
		jquery.page-realtime-twitter-reactions.js v1.0
		Last updated: 27 November 2009

		Created by Chico Charlesworth
		http://blog.niteviva.com/development/realtime-twitter-reactions-using-jquery
		
		Licensed under a Lesser General Public License
		http://creativecommons.org/licenses/LGPL/2.1/
	*/

	$.fn.getPageRealtimeReactions = function(options) {
		var o = $.extend({}, $.fn.getPageRealtimeReactions.defaults, options);
	
		// hide container element
		$(this).hide();
		
		// add heading to container element
		if (o.showHeading) {
			$(this).append('<h2>'+o.headingText+'</h2>');
		}

		// add twitter list to container element
		$(this).append('<ul id="twitter_update_list"></ul>');

		// hide twitter list
		$("ul#twitter_update_list").hide();

		// add preLoader to container element
		var pl = $('<p id="'+o.preloaderId+'">'+o.loaderText+'</p>');
		$(this).append(pl);

		// show container element
		$(this).show();
	
		// twitter search only supports queries up to 130 characters,
		// so call it as many times is needed by splitting up the
		// query into queries of 130 characters or less.
		var searches = o.query.split(" OR ");
		var query = "";
		for (var i=0; i < searches.length; i++) {
			if ((query + " OR " + searches[i]).length < 130) {
				if (i > 0)
					query += " OR ";
				query += searches[i];
			} else {
				searchTwitter(pl, query, o.numTweets, o.slideIn, false);
				query = searches[i];
			}
		}
		searchTwitter(pl, query, o.numTweets, o.slideIn, true);		
	};

	// plugin defaults
	$.fn.getPageRealtimeReactions.defaults = {
		userName: null,
		numTweets: 5,
		query: "",
		preloaderId: "preloader",
		loaderText: "Loading tweets...",
		slideIn: false,
		showHeading: true,
		headingText: "Latest Tweets",
		showProfileLink: true
	};
	
})(jQuery);

function searchTwitter(pl, query, numTweets, slideIn, lastCall) {
	$.getScript("http://search.twitter.com/search.json?callback=pageRealtimeReactionsCallback&q=" + query + "&rpp=" + numTweets, function() {
		if (lastCall) {
			for (var i=0; i < pageRealtimeTwitterReactionsTimeStamps.length; i++) {
				if (i == numTweets) {
					break;
				}
				var nextMostRecentArrayIndex = 0;
				var nextMostRecentTimestamp = 0;
				for (var k=0; k < pageRealtimeTwitterReactionsTimeStamps.length; k++) {
					if (pageRealtimeTwitterReactionsTimeStamps[k] > nextMostRecentTimestamp) {
						nextMostRecentTimestamp = pageRealtimeTwitterReactionsTimeStamps[k];
						nextMostRecentArrayIndex = k;
					}					
				}
				$('#twitter_update_list').append(pageRealtimeTwitterReactionsHTML[nextMostRecentArrayIndex]);
				pageRealtimeTwitterReactionsTimeStamps[nextMostRecentArrayIndex] = 0;				
			}
			
			// remove preLoader from container element
			$(pl).remove();
	
			// show twitter list
			if (slideIn) {
				$("ul#twitter_update_list").slideDown(1000);
			}
			else {
				$("ul#twitter_update_list").show();
			}
	
			// give first list item a special class
			$("ul#twitter_update_list li:first").addClass("top");
	
			// give last list item a special class
			$("ul#twitter_update_list li:last").addClass("last");
		}
	});
}

function pageRealtimeReactionsCallback(response) {
  var tweets = response.results;
  for (var i=0; i<tweets.length; i++) {  	
    var username = tweets[i].from_user;
    var status = tweets[i].text.replace(/((https?|s?ftp|ssh)\:\/\/[^"\s\<\>]*[^.,;'">\:\s\<\>\)\]\!])/g, function(url) {
      return '<a href="'+url+'">'+url+'</a>';
    }).replace(/\B@([_a-z0-9]+)/ig, function(reply) {
      return  reply.charAt(0)+'<a href="http://twitter.com/'+reply.substring(1)+'">'+reply.substring(1)+'</a>';
    });
    var realtimeReaction = '<li class="tweet"><a href="http://twitter.com/'+username+'/statuses/'+tweets[i].id+'" class="username">'+username+'</a> <span>'+status+'</span> <a style="font-size:85%" href="http://twitter.com/'+username+'/statuses/'+tweets[i].id+'" class="time">' + prettyDate(tweets[i].created_at) + '</a></li>';
    // Avoid duplicates
    if ($.inArray(realtimeReaction, pageRealtimeTwitterReactionsHTML) < 0) {
    	pageRealtimeTwitterReactionsHTML.push(realtimeReaction);
    	var date = new Date((tweets[i].created_at || "").replace(/-/g,"/").replace(/[TZ]/g," "));
	    pageRealtimeTwitterReactionsTimeStamps.push(date.getTime());
    }
  }
}

// prettyDate function borrowed from http://ejohn.org/files/pretty.js :)
function prettyDate(time){
	if (!time)
		return "sometime ago";
	
	var date = new Date((time || "").replace(/-/g,"/").replace(/[TZ]/g," ")),
		diff = (((new Date()).getTime() - date.getTime()) / 1000),
		day_diff = Math.floor(diff / 86400);
			
	if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
		return "sometime ago";
			
	return day_diff == 0 && (
			diff < 60 && "just now" ||
			diff < 120 && "1 minute ago" ||
			diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
			diff < 7200 && "1 hour ago" ||
			diff < 86400 && Math.floor( diff / 3600 ) + " hours ago") ||
		day_diff == 1 && "Yesterday" ||
		day_diff < 7 && day_diff + " days ago" ||
		day_diff == 7 && " 1 week ago" ||
		day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago";
}
