function repopulateListOfPortfolios(selectedId) {
    var portfolioList = getListOfPortfolios();
    var html = "";
    for (var i = 0; i < portfolioList.length; i++) {
        var id = portfolioList[i].id;
        var name = portfolioList[i].name;
        html += "<li data-portfolioid=" + id + " "
        if(id == selectedId){
            html+= "class=\"current-page\""
        }
        html+= "><a href=\"#\">" + name + "</a></li>";
    }

    $(".portfolio-list").html(html)
    $(".portfolio-list").slideDown().addClass('active');
    $(".portfolio-list li").click(function(){
        refreshToPortfolio($(this).data("portfolioid"));
    });
}

function getListOfPortfolios(){
    var user_portfolio_list = null
        var url_portfolio_list = "/api/user/" + currentUser_id + "/getportfoliolist";
        $.ajax({
            url: url_portfolio_list,
            success: function (data) {
                user_portfolio_list = data.portfolio_list;
            },
            async:false
        });
    return user_portfolio_list;
}

$("#add-portfolio").click(function(){
    var url_portfolio_list = "/api/portfolio/create/" + currentUser_id
    var portfolio_id
    $.ajax({
            url: url_portfolio_list,
            success: function (data) {
                portfolio_id = data.id;
            },
            dataType: "json",
            async:false
        });
    refreshToPortfolio(portfolio_id);
    $("#modifyPortfolio").modal("show")
})
repopulateListOfPortfolios(user_portfolio.portfolio_id);
