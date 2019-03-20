
$(document).ready(function(){
	$(".btn").click(function(){
		$(this).toggleClass('btn-success');
		$(this).toggleClass('btn-danger');
		var x = $(this).css('backgroundColor');
	});
});