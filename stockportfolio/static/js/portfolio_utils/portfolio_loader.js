stocks = user_portfolio.stocks;
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