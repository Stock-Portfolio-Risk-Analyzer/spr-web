window.onload = sprInit()

function sprInit() {
    fetchStock()
    loadStockRec() 
}

function fetchStock() {
    var url = location.protocol +"//"+ window.location.host + "/api/";
    var stocks = document.body.getElementsByTagName('stock-price');
    var requests={};
    for (var idx = 0; idx < stocks.length; idx++) {
        var symbol = stocks[idx].getAttribute("data-stock"); 
        requests[symbol] = new XMLHttpRequest();
        requests[symbol].symbol = symbol
        requests[symbol].open("GET", url + symbol + "/", true);
        requests[symbol].send();
        requests[symbol].onreadystatechange = function(){
            if(this.readyState == 4) {
                document.getElementById(this.symbol).innerHTML = this.responseText;
            }
        }
    }
}

function loadStockRec(portfolioId) {
    // somehow get current portfolio
    var url = "/api/" + portfolioId + "/stock_rec";
    request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.send();
    request.onreadystatechange = updateRecs 
}

function updateRecs() {
}
