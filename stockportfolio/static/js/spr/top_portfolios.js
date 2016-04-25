var var_results;
var top_portfolio = function(option){
	    $.ajax({
        url: "/api/top-ten/" + option,
        success: function (results) {
        	var_results = results

		var $clone = $("table#top_portfolio").find('tr.hide.sample').clone();
		$("table#top_portfolio tbody tr").remove()
		$("table#top_portfolio").append($clone)


		for (var i = 0; i < var_results.length; i++) {
		    var res = var_results[i];
		    var $clone = $("table#top_portfolio").find('tr.hide.sample').clone(true).removeClass("hide")
		    $clone.find("td.rank").text(res['rank'])
		    $clone.find("td.name").text(res['name'])
		    $clone.find("td.rri").text(res['rri'])
		    $clone.find("td.value").text(res['value'])
		    $("table#top_portfolio").append($clone)
		}
    
        },
        error: function(){
        } 
    });
};