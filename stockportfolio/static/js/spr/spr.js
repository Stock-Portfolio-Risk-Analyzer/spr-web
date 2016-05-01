window.onload = function sprInit() {
    attachEvents() 
    setDownloadLink()
    var img = document.createElement('img');
    img.style.width = '1120px';
    img.style.height = '4800px';
    img.src = "/api/user/" + currentUser_id  +"/simulateportfolio";
    $('#simPortfolioContent').append(img);
    document.getElementById("simulate-portfolio").onclick=function() {
        $('#simPortfolio').modal('show'); 
    }
}

function setDownloadLink() {
    var l = document.getElementById("portfolio-download-form")
    var url = "/api/portfolio/"+user_portfolio.portfolio_id+"/download"
    l.setAttribute("action", url)
}

function attachEvents() {
    document.getElementById("stableTile").onclick=getRecs("stable", "stableContent")
    document.getElementById("highTile").onclick=getRecs("high_risk", "highContent")
    document.getElementById("lowTile").onclick=getRecs("low_risk", "lowContent")
    document.getElementById("diverseTile").onclick=getRecs("diverse", "diverseContent")
}

function loadGenPortfolio() {
    var request = new XMLHttpRequest()
    $('#genPortfolio').modal('show'); 
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("genPortfolioContent").insertAdjacentHTML('beforeend', this.responseText);
            console.log(this.responseText)
        }
    }
    request.open("GET", 
                 window.location.protocol+"//"+window.location.host+
                 "/api/portfolio/generate_portfolio")
    request.send()
}

function getRecs(recType, contentId) {
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
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById(contentId).insertAdjacentHTML('beforeend', this.responseText);
        }
    }
    request.open("GET", 
                 window.location.protocol+"//"+window.location.host+
                 "/api/portfolio/"+curr+"/"+recType+"/recommendation")
    request.send()
}