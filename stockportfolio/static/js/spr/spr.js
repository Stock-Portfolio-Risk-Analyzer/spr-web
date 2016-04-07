window.onload = sprInit
function sprInit() {
    attachEvents()
}

bigAssJSON = {
    "stable": [{
        "stock_id": 1,
        "stock_quantity": 0,
        "stock_name": "ABC Corporation",
        "stock_beta": 1.5,
        "stock_sector": "Consumer Goods"
    }, {
        "stock_id": 2,
        "stock_quantity": 0,
        "stock_name": "Real Good Goods",
        "stock_beta": 0.8,
        "stock_sector": "Finances"
    }, {
        "stock_id": 88,
        "stock_quantity": 0,
        "stock_name": "Generic LLC",
        "stock_beta": 1.1,
        "stock_sector": "LMAO"
    }, {
        "stock_id": 12,
        "stock_quantity": 0,
        "stock_name": "Big Guys",
        "stock_beta": 1.9,
        "stock_sector": "asgsgasd"
    }],
    "low": [{
        "stock_id": 1,
        "stock_quantity": 0,
        "stock_name": "ABC Corporation",
        "stock_beta": 1.5,
        "stock_sector": "Consumer Goods"
    }, {
        "stock_id": 2,
        "stock_quantity": 0,
        "stock_name": "Real Good Goods",
        "stock_beta": 0.8,
        "stock_sector": "Finances"
    }, {
        "stock_id": 88,
        "stock_quantity": 0,
        "stock_name": "Generic LLC",
        "stock_beta": 1.1,
        "stock_sector": "LMAO"
    }, {
        "stock_id": 12,
        "stock_quantity": 0,
        "stock_name": "Big Guys",
        "stock_beta": 1.9,
        "stock_sector": "asgsgasd"
    }],
    "diverse": [{
        "stock_id": 1,
        "stock_quantity": 0,
        "stock_name": "ABC Corporation",
        "stock_beta": 1.5,
        "stock_sector": "Consumer Goods"
    }, {
        "stock_id": 2,
        "stock_quantity": 0,
        "stock_name": "Real Good Goods",
        "stock_beta": 0.8,
        "stock_sector": "Finances"
    }, {
        "stock_id": 88,
        "stock_quantity": 0,
        "stock_name": "Generic LLC",
        "stock_beta": 1.1,
        "stock_sector": "LMAO"
    }, {
        "stock_id": 12,
        "stock_quantity": 0,
        "stock_name": "Big Guys",
        "stock_beta": 1.9,
        "stock_sector": "asgsgasd"
    }],
    "high": [{
        "stock_id": 1,
        "stock_quantity": 0,
        "stock_name": "ABC Corporation",
        "stock_beta": 1.5,
        "stock_sector": "Consumer Goods"
    }, {
        "stock_id": 2,
        "stock_quantity": 0,
        "stock_name": "Real Good Goods",
        "stock_beta": 0.8,
        "stock_sector": "Finances"
    }, {
        "stock_id": 88,
        "stock_quantity": 0,
        "stock_name": "Generic LLC",
        "stock_beta": 1.1,
        "stock_sector": "LMAO"
    }, {
        "stock_id": 12,
        "stock_quantity": 0,
        "stock_name": "Big Guys",
        "stock_beta": 1.9,
        "stock_sector": "asgsgasd"
    }]
}

function attachEvents() {
    //TODO: pull from back-end
    var json = bigAssJSON
    var modals = document.getElementsByClassName("rec-modal")
    for (i=0; i < modals.length; i++) {
        var modal = modals[i]
        var k = modal.id.replace(/Modal/g, "")
        modal.addEventListener("click", function(){updateStockRec(k)})
        /*var k = modal.id.replace(/Modal/g, "")
        var stocks = json[k] 
        var modalBody = document.getElementById(k+"-rec-body")
        var list = document.createElement("ul")
        for (j=0; j < stocks.length; j++) {
            var item = document.createElement("li")   
            var name = document.createTextNode(stocks[j]["stock_name"])
            item.appendChild(name)
            list.appendChild(item)
        }
        modalBody.appendChild(list)*/       
    }
}

function updateStockRec(recType) {
    var json = bigAssJSON
    var modalBody = document.getElementById(recType+"-rec-body")
    var list  document.createElement("ul")
    var stocks = json[k]
    for(i=0;i<stocks.length;i++){
        var item = document.createElement("li")
        var name = document.createTextNode(stocks[i]["stock_name"]
        item.appendChild(name)
        list.appendChild(item)
    }
    modalBody.appendChild(list) 
}
