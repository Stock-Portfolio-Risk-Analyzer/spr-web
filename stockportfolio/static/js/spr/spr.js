window.onload = function sprInit() {
    attachEvents() 
}

function attachEvents() {
    // for some reason, addEventListener will only attach an event listener 
    // to the first element in a loop. that's the reason for this monstrosity 
    document.getElementById("stableModal").onclick=getRecs("stable")
    document.getElementById("highModal").onclick=getRecs("high")
    document.getElementById("lowModal").onclick=getRecs("low")
    document.getElementById("diverseModal").onclick=getRecs("diverse")
    
}

function getRecs(recType) {
    var portfolios = document.querySelectorAll('[data-portfolioid]');
    var curr;
    for (i=0; i < portfolios.length; i++) {
        var id = portfolios[i]
        if (id.className.indexOf("current-page") > -1) {
            curr = id.getAttribute("data-portfolioid")
            break
        }
    }
    var request = new XMLHttpRequest()
    request.rec = recType
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            updateStockRec(this.responseText, this.rec)
        }
    }
    request.open("GET", 
                 window.location.protocol+"//"+window.location.host+
                 "/api/portfolio/"+curr+"/stock_rec")
    request.send()
}

function updateStockRec(json, recType) {
    var recs = JSON.parse(json)
    var modalBody = document.getElementById(recType+"-rec-body")
    var list  = document.createElement("ul")
    list.className += "list-unstyled top_profiles scroll-view"
    var stocks = recs[recType]
    console.log(stocks)
    if (stocks === undefined || stocks.length === 0) {
        var item = newElem("p", "", "")
        item.innerHTML = "No recommendations right now. Check again later!"
        list.appendChild(item)
    } else {
        for(i=0;i<stocks.length;i++){
            var item = stockElement(stocks[i])
            list.appendChild(item)
        }
    }
    modalBody.appendChild(list) 
}

function newElem(type, html, classN) {
    var e = document.createElement(type)
    e.innerHTML = html
    e.className = classN
    return e
}

function stockElement(stock) {
    var elem = newElem("li", "", "media-event")
    var div  = newElem("div", "", "media-body")
    var name = newElem("h4", stock["stock_name"], "")
    div.appendChild(name)
    var info = stock["stock_ticker"] + " | " +
               stock["stock_sector"] + " | " + stock["stock_beta"]
    var p = newElem("p", info, "")
    div.appendChild(p)
    elem.appendChild(div)
    return elem
}
