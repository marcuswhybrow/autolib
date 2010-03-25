/*
var SAVE_COLLECTION = "/api/save/collection";
var SAVE_PROFILE = "/api/save/profile";

var GET_COLLECTION = "/api/get/collection";
var GET_PROFILE = "/api/get/profile";
var GET_BOOK = "/api/get/book";

var DELETE_COLLECTION = "/api/delete/collection";
var DELETE_PROFILE = "/api/delete/profile";
*/

function overlay(message)
{
	$.blockUI(
	{ 
		fadeIn:  200,
		fadeOut: 200,
		css: 
		{ 
			border: 'none',
			opacity: 1,
			'-webkit-border-radius': '10px',
			'-moz-border-radius': '10px',
			backgroundColor: 'none'
        },
    	message: message
    });
}

function connection(url, data, f, last, type, async)
{
	if (type === undefined) {
		type = 'POST';
	}
	
	if (last === undefined) {
		last = function() {};
	}
	
	if (async === undefined) {
		async = true;
	}
	
	$.ajax(
	{
		url: url,
		data: data,
		dataType: 'json',
		type: type,
		async: async,
		success: function(data)
		{
			if (data.meta.success == true)
			{
				f(data);
			}
			else
			{
				$('#accept-overlay').find('h1.target').text('There Was An Error');
				$('#accept-overlay').find('p.target').text(data.meta.error);
				$.blockUI(
				{ 
					fadeIn:  200,
					fadeOut: 200,
					css:
					{ 
						border: 'none',
						opacity: 1,
						'-webkit-border-radius': '10px',
						'-moz-border-radius': '10px',
						backgroundColor: 'none'
			        },
		        	message: $('#accept-overlay')
		        });
			}
			
			last();
		},
		error: function()
		{
			$('#accept-overlay').find('h1.target').text('Something Went Wrong!');
			$('#accept-overlay').find('p.target').text('This is completely our fault, something has gone wrong on our end. We are probably trying to fix it, so try again in a few seconds.');
			$.blockUI(
			{ 
				fadeIn:  200,
				fadeOut: 200,
				css:
				{ 
					border: 'none',
					opacity: 1,
					'-webkit-border-radius': '10px',
					'-moz-border-radius': '10px',
					backgroundColor: 'none'
		        },
	        	message: $('#accept-overlay')
	        });
	        
	        last();
		}
	});
}