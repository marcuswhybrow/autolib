/* 
 * Shadow Labels (0.1)
 * by Marcus Whybrow (marcuswhybrow.net)
 * marcus@marcuswhybrow.net
 *
 * NOTE: This script requires jQuery to work.  Download jQuery at www.jquery.com
 *
 */

(function($) {

	$.fn.shadowLabels = function() {
	
		$(this).each(function(options) {
			
			var form = $(this);
			
			var criteria = '';
			criteria += "input[type='text']";
			criteria += ", input[type='password']";
			criteria += ", textarea";
			
			form.find(criteria).each(function() {
				
				var input = $(this);
				var label = form.find("label[for='" + input.attr('id') + "']");
				
				input.val(label.text());
				input.addClass('default');
				input.attr('default', 'true');
				
				input.focus(function() {
					
					if (input.attr('default') == 'true') {
						input.val('');
						input.removeClass('default');
						input.attr('default', 'false');
					}
					
				});
				
				input.blur(function() {
					
					if (input.val() == '') {						
						input.val(label.text());
						//addedVal = true;
						input.attr('default', 'true');
						input.addClass('default');
						
					} else {
						input.attr('default', 'false');
					}
					
					
				})
				
				label.remove();
				
			});
			
			form.submit(function() {
				form.find('input').each(function() {
					if ($(this).attr('default') == 'true') {
						$(this).val('');
					}
				});
			});
			
		});
		
	}
	
})(jQuery);