window.onload = sprInit()
function sprInit() {
    var url = "http://" + window.location.host + "/api/";
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
