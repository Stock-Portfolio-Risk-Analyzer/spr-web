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
		    $clone.find("td.id").text(res['id'])
		    $clone.find("td.name").text(res['name'])
		    $clone.find("td.rri").text(res['rri'])
		    $clone.find("td.value").text(res['value'])
		    $("table#top_portfolio").append($clone)
		}

		$("#top_portfolio tr").bind("click",function() {

        	var selectedPortfolio = $(this).closest("tr").find(".id").text();

        	var selectedPortfolioUrl = "/api/top-ten/portfolio/" + selectedPortfolio;
       		 $.ajax({
            	url: selectedPortfolioUrl,
            	type: 'GET',
            	success: function(data) {
            		$('#top-portfolio-list-view').addClass('hidden');
                $('#top-portfolio-detail-view').removeClass('hidden');

                var $clone = $("table#top-portfolio-details-table").find('tr.hide.sample').remove().clone();
                $("table#top-portfolio-details-table tbody tr").remove()
                $("table#top-portfolio-details-table").append($clone)

                for (var i = 0; i < data.stocks.length; i++) {
                    var stock = data.stocks[i];
                    var $clone = $("table#top-portfolio-details-table").find('tr.hide.sample').clone(true).removeClass("hide")
                    $clone.find("td.company").text(stock.name)
                    $clone.find("td.symbol").text(stock.ticker)
                    $clone.find("td.sector").text(stock.sector)
                    $clone.find("td.quantity").text(stock.quantity)
                    $clone.find("td.last_price").text(stock.price)
                    $clone.find("td.market_value").text(stock.mkt_value)
                    $("table#top-portfolio-details-table").append($clone)
                }
            	}
        	});
		});

        },
        error: function(){
        }
    });
};



$("#top-portfolios").click(function() {
  $('#topPortfolios').modal('show');
});

$('#topPortfolios').on('show.bs.modal', function() {
  top_portfolio(0);
});

$('#topPortfolios').on('hide.bs.modal', function() {
  $('#top-portfolio-list-view').removeClass('hidden');
  $('#top-portfolio-detail-view').addClass('hidden');
});

$('#topPortfolios .btn-primary').on('click', function() {
  top_portfolio($(this).find('input').attr('id'));
});

$('.top-portfolio-back-btn').on('click', function() {
  $('#top-portfolio-list-view').removeClass('hidden');
  $('#top-portfolio-detail-view').addClass('hidden');
});
