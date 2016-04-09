window.onload = function sprInit() {
    attachEvents()

}

function attachEvents() {
    // for some reason, addEventListener will only attach an event listener 
    // to the first element in a loop. that's the reason for this monstrosity 
    document.getElementById("stableModal").onclick=updateStockRec("stable")
    document.getElementById("highModal").onclick=updateStockRec("high")
    document.getElementById("lowModal").onclick=updateStockRec("low")
    document.getElementById("diverseModal").onclick=updateStockRec("diverse")
    
}

function updateStockRec(recType) {
    var json = undefined // TODO: pull this from back-end
    var modalBody = document.getElementById(recType+"-rec-body")
    var list  = document.createElement("ul")
    list.className += "list-unstyled top_profiles scroll-view"
    var stocks = json[recType]
    for(i=0;i<stocks.length;i++){
        item = stockElement(stocks[i])
        list.appendChild(item)
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
