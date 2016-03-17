
// Data for the portfolio diversity donut chart

var doughnutDataForDiversity = []
var arrayOfStocks = user_portfolio.stocks
var xkcd = [
                    {"name": "Apple Inc", "ticker": "AAPL", "value": 100, "risk": 2.1, "quantity": 2, "type": "Equity"}, 
                    {"name": "Yahoo Inc", "ticker": "YHOO", "value": 50, "risk": 3.2, "quantity": 2, "type": "Equity"},
                    {"name": "Chesapeake", "ticker": "CHK", "value": 20, "risk": 4.3, "quantity": 1, "type": "Equity"},
                    {"name": "MasterCard", "ticker": "MA", "value": 40, "risk": 5.4, "quantity": 3, "type": "Equity"}
                    ]

var arrayOfColors = ["#26B99A","#3498DB","#BDC3C7","#455C73","#9B59B6"];
var numOfStocks = arrayOfStocks.length
var totalValueOfStocks = 0
var proportionOfStocks = []
var valueOfStocks = []


for (var i =0; i<numOfStocks;i++) {
    totalValueOfStocks += arrayOfStocks[i].mkt_value
}

for (var i =0; i<numOfStocks;i++) {   
    
    proportionOfStocks[i] = arrayOfStocks[i].mkt_value/totalValueOfStocks

    var newStock = { 
        value: proportionOfStocks[i],                
        color: arrayOfColors[i]
    }

    doughnutDataForDiversity.push(newStock)
}

var table = document.getElementById("donut_diversity")

for (var i = 0; i < numOfStocks; i++) {
    var row = table.insertRow(i)
    var cell1 = row.insertCell(0)
    var cell2 = row.insertCell(1)

    cell1.innerHTML = "<p><i class=\"fa fa-square \"" +i+"\"></i>" + arrayOfStocks[i].ticker + "</p>"
    cell1.style.color = arrayOfColors[i%numOfStocks]
    cell2.innerHTML = (proportionOfStocks[i]*100).toFixed(2)+"%";
}

// Data for the portfolio sector diversity donut chart

var valueOfSectors = {}
var doughnutDataForSectorDiversity = []

for (var i =0; i<numOfStocks;i++) {
    
    if (valueOfSectors.hasOwnProperty(arrayOfStocks[i].sector))
        valueOfSectors[arrayOfStocks[i].sector] = valueOfSectors[arrayOfStocks[i].sector] + arrayOfStocks[i].mkt_value
    else
        valueOfSectors[arrayOfStocks[i].sector] = arrayOfStocks[i].mkt_value
}


var namesOfSectors = Object.keys(valueOfSectors)
var numOfSectors = namesOfSectors.length

for (var i =0; i<numOfSectors;i++) {   
    
    valueOfSector = valueOfSectors[namesOfSectors[i]]
   
    var newStock = { 
        value: valueOfSector/totalValueOfStocks,
        color: arrayOfColors[i]
    }
    
    doughnutDataForSectorDiversity.push(newStock)
}


var table = document.getElementById("donut_sector_diversity")

for (var i = 0; i < numOfSectors; i++) {

    valueOfSector = valueOfSectors[namesOfSectors[i]]

    var row = table.insertRow(i)
    var cell1 = row.insertCell(0)
    var cell2 = row.insertCell(1)

    cell1.innerHTML = "<p><i class=\"fa fa-square \"" +i+"\"></i>" + namesOfSectors[i] + "</p>"
    cell1.style.color = arrayOfColors[i%arrayOfStocks.length]
    cell2.innerHTML = (valueOfSector/totalValueOfStocks*100).toFixed(2)+"%";
}

//Create both the charts
var myDoughnut = new Chart(document.getElementById("canvas1").getContext("2d")).Doughnut(doughnutDataForDiversity);
var myDoughnut2 = new Chart(document.getElementById("canvas2").getContext("2d")).Doughnut(doughnutDataForSectorDiversity);

//Make Portfolio Value/Risk dynamic
var value_div = document.getElementById("portfolio_value")
value_div.innerHTML = "$" + totalValueOfStocks.toFixed(2)

var risk_div = document.getElementById("portfolio_risk")
risk_div.innerHTML = "N/A"

//Make Portfolio Table dynamic
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
