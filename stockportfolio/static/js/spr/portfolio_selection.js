function repopulateListOfPortfolios() {
    var portfolioList = getListOfPortfolios();
    var html = "";
    for (var i = 0; i < portfolioList.length; i++) {
        id = portfolioList[i].id;
        name = portfolioList[i].name;
        html += "<li data-portfolioid=" + id + "><a href=\"#\">" + name + "</a></li>";
    }
    $(".portfolio-list").html(html);
    $(".portfolio-list li").click(function(){
        console.log($(this).data("portfolioid"))
    });

}

function getListOfPortfolios(){
    var user_portfolio_list = null
        url_portfolio_list = "/api/user/" + currentUser_id + "/getportfoliolist";
        $.ajax({
            url: url_portfolio_list,
            success: function (data) {
                user_portfolio_list = data.portfolio_list;
            },
            async:false
        });
    return user_portfolio_list;
}

repopulateListOfPortfolios();
