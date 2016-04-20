/**
 * Created by enriqueespaillat on 4/6/16.
 */
function getDefaultPortfolio() {
    url_getportfolio = "/api/user/" + currentUser_id + "/getportfolio";
    $.ajax({
        url: url_getportfolio,
        success: function (data) {
            user_portfolio = data;
        },

        async: false
    });
}
function refreshToPortfolio(portfolioId) {
        url_getportfolio = "/api/portfolio/" + portfolioId;
        $.ajax({
            url: url_getportfolio,
            success: function (data) {
                user_portfolio = data;
            },

            async: false
        });
        loadDiversityGraphs();
        loadAllGraphs();
        repopulateListOfPortfolios(portfolioId);
        populate_table();
        setDownloadLink();
}
getDefaultPortfolio();
