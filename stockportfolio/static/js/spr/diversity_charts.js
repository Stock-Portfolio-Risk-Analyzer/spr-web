// Data for the portfolio diversity donut chart
myDoughnut = null
myDoughnut2 = null
function loadDiversityGraphs() {
    stocks = user_portfolio.stocks;
    var doughnutDataForDiversity = []
    var arrayOfStocks = user_portfolio.stocks
    var arrayOfColors = ["#26B99A", "#3498DB", "#BDC3C7", "#455C73", "#9B59B6"];
    var numOfStocks = arrayOfStocks.length
    var totalValueOfStocks = 0
    var proportionOfStocks = []
    var valueOfStocks = []


    for (var i = 0; i < numOfStocks; i++) {
        totalValueOfStocks += arrayOfStocks[i].mkt_value
    }

    for (var i = 0; i < numOfStocks; i++) {

        proportionOfStocks[i] = arrayOfStocks[i].mkt_value / totalValueOfStocks

        var newStock = {
            value: proportionOfStocks[i],
            color: arrayOfColors[i]
        }

        doughnutDataForDiversity.push(newStock)
    }

    var table = document.getElementById("donut_diversity")
    $("#donut_diversity tr").remove()

    for (var i = 0; i < numOfStocks; i++) {
        var row = table.insertRow(i)
        var cell1 = row.insertCell(0)
        var cell2 = row.insertCell(1)

        cell1.innerHTML = "<p><i class=\"fa fa-square \"" + i + "\"></i>" + arrayOfStocks[i].ticker + "</p>"
        cell1.style.color = arrayOfColors[i % numOfStocks]
        cell2.innerHTML = (proportionOfStocks[i] * 100).toFixed(2) + "%";
    }

// Data for the portfolio sector diversity donut chart

    var valueOfSectors = {}
    var doughnutDataForSectorDiversity = []

    for (var i = 0; i < numOfStocks; i++) {

        if (valueOfSectors.hasOwnProperty(arrayOfStocks[i].sector))
            valueOfSectors[arrayOfStocks[i].sector] = valueOfSectors[arrayOfStocks[i].sector] + arrayOfStocks[i].mkt_value
        else
            valueOfSectors[arrayOfStocks[i].sector] = arrayOfStocks[i].mkt_value
    }


    var namesOfSectors = Object.keys(valueOfSectors)
    var numOfSectors = namesOfSectors.length

    for (var i = 0; i < numOfSectors; i++) {

        valueOfSector = valueOfSectors[namesOfSectors[i]]

        var newStock = {
            value: valueOfSector / totalValueOfStocks,
            color: arrayOfColors[i]
        }

        doughnutDataForSectorDiversity.push(newStock)
    }


    var table = document.getElementById("donut_sector_diversity")
    $("#donut_sector_diversity tr").remove()
    for (var i = 0; i < numOfSectors; i++) {

        valueOfSector = valueOfSectors[namesOfSectors[i]]

        var row = table.insertRow(i)
        var cell1 = row.insertCell(0)
        var cell2 = row.insertCell(1)

        cell1.innerHTML = "<p><i class=\"fa fa-square \"" + i + "\"></i>" + namesOfSectors[i] + "</p>"
        cell1.style.color = arrayOfColors[i % arrayOfStocks.length]
        cell2.innerHTML = (valueOfSector / totalValueOfStocks * 100).toFixed(2) + "%";
    }

//Create both the charts
    $("#canvas1").remove();
    $("#canvas2").remove();
    $("#canvas1-container").append('<canvas id="canvas1" height="140" width="140" style="margin: 15px 10px 10px 0"></canvas>');
    $("#canvas2-container").append('<canvas id="canvas2" height="140" width="140" style="margin: 15px 10px 10px 0"></canvas>');
    if(myDoughnut != null){
        myDoughnut.clear();
    }
    if(myDoughnut2 != null){
        myDoughnut2.clear();
    }
    myDoughnut = new Chart(document.getElementById("canvas1").getContext("2d")).Doughnut(doughnutDataForDiversity)
    myDoughnut2 = new Chart(document.getElementById("canvas2").getContext("2d")).Doughnut(doughnutDataForSectorDiversity)

//Make Portfolio Value/Risk dynamic
    var value_div = document.getElementById("portfolio_value")
    value_div.innerHTML = "$" + totalValueOfStocks.toFixed(2)

    var risk_div = document.getElementById("portfolio_risk")
    if(user_portfolio.risk_history.length > 0){
        risk_div.innerHTML = "" + user_portfolio.risk_history[0].risk_value.toFixed(2)
    } else {
        risk_div.innerHTML = "N/A"
    }

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

    $("#portfolio tr").bind("click",function() {
        var ticker = $(this).closest("tr").find(".symbol").text();
        var tickerUrl = "/api/" + ticker + "/details";
        $.ajax({
            url: tickerUrl,
            type: 'GET',
            success: function(data) {
                $('#stockInterface').html(data);
                $('#stockInterfaceModal').modal('show');
            }
        });
    
    //Load Rank
    if(user_portfolio.rank != null){
        $("#risk_rank").html(user_portfolio.rank)
    } else {
        $("#risk_rank").html("N/A")
    }
}


loadDiversityGraphs();