
//Make Portfolio Table dynamic
    //remove all elements on reload, except hidden sample row.
    var $clone = $("table#portfolio").find('tr.hide.sample').remove().clone();
    console.log($clone)
    $("table#portfolio tbody tr").remove()
    $("table#portfolio").append($clone)

    for (var i = 0; i < stocks.length; i++) {
        var stock = stocks[i];
        var $clone = $("table#portfolio").find('tr.hide.sample').clone(true).removeClass("hide")
        $clone.find("td.company").text(stock.name)
        $clone.find("td.symbol").text(stock.ticker)
        $clone.find("td.sector").text(stock.sector)
        $clone.find("td.quantity").text(stock.quantity)
        $clone.find("td.last_price").text(stock.price)
        $clone.find("td.market_value").text(stock.mkt_value)
        $("table#portfolio").append($clone)
    }
    //Load Rank
    if(user_portfolio.rank != null){
        $("#risk_rank").html(user_portfolio.rank)
    } else {
        $("#risk_rank").html("N/A")
    }

