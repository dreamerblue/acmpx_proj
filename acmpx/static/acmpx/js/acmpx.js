$(function () {
	if($(".messages.container").length > 0) {
		$.scrollTo("body");
	}
	if($(".loading-button").length > 0) {
		$(".loading-button").one("click", function () {
			$(this).data("loading-text", $(this).data("loading-text") + '<i class="fas fa-spinner fa-spin text-left-gap">');
			$(this).button('loading');
			$(this).click(function () {
				return false;
			});
		});
	}
	if($(".show-full-about").length > 0) {
		$(".show-full-about").one("click", function () {
			$(this).hide();
			$(".hidden-about").show();
		});
	}
});