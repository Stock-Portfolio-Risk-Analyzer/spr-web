/**
 * Created by enriqueespaillat on 4/6/16.
 */
function populate_table() {
    clear_table();
    var stocks = user_portfolio.stocks;
    var currentCount = parseInt($("#stock-modify-count").val())
    for (var i = 0; i < stocks.length; i++) {
        var stock = stocks[i];
        var $clone = $("#portfolio-table").find('tr.clone').clone(true).removeClass("hide").removeClass('clone').addClass("perishable")
        $clone.find("input#symbol").val(stock.ticker).attr("readonly", "readonly")
        $clone.find("input#symbol").attr("name", "symbol_" + currentCount)
        $clone.find("input#quantity").val(stock.quantity)
        $clone.find("input#quantity").attr("name", "quantity_" + currentCount)
        $("#portfolio-table tbody").append($clone)
        currentCount += 1
    }
    $("#stock-modify-count").val(currentCount)
}

function clear_table() {
    //clear all rows except empty hidden row used to clone.
    $("#portfolio-table tbody tr.perishable").remove()
    //clear title
    $("#pname").val(user_portfolio.name)
    $("#stock-modify-count").val(0)
}

$("#add-row").click(function () {
    var currentCount = parseInt($("#stock-modify-count").val())
    var $clone = $("#portfolio-table").find('tr.clone').clone(true).removeClass("hide").removeClass('clone')
    $clone.find("input#symbol").attr("name", "symbol_" + currentCount)
    $clone.find("input#quantity").attr("name", "quantity_" + currentCount)
    $("#portfolio-table").append($clone)
    $("#stock-modify-count").val(currentCount+1)
});
$("#delete-row").click(function () {
    $(this).closest("tr").find("#quantity").val(0)
    $(this).closest("tr").hide()
});

$("#delete-portfolio-button").click(function() {
    $.ajax({
        url: "/api/portfolio/" + user_portfolio.portfolio_id + "/delete",
        success: function (results) {
            getDefaultPortfolio()
            if(user_portfolio != null){
                refreshToPortfolio(user_portfolio.portfolio_id)
            }
            $("#modifyPortfolio").modal('hide');
        }
    });
});

$("#save-button").click(function(e) {
    $clone = $('#modify-portfolio-form')
    var form = {};
    form["symbols"] = {}
    form["quantities"] = {}
    $.each($clone.serializeArray(),
        function(i, field) {
            var dict = ""
            if(field.name.split("_").pop() == "symbol"){
                return true;
            }
            if(field.name.indexOf("symbol") > -1){
                var i = field.name.split("_").pop()
                form["symbols"][i] = field.value
            } else if (field.name.indexOf("quantity") > -1) {
                var i = field.name.split("_").pop()
                form["quantities"][i] = field.value
            } else if (field.name.indexOf("pname") > -1) {
                form["name"] = field.value
            }
        });
    form = JSON.stringify(form)
    var csrfToken = $clone.find("#csrf-token").val()
    $.ajax({
        url : "/api/portfolio/"+ user_portfolio.portfolio_id +"/modify",
        type: "post",
        data : {
            "data": form,
            'csrfmiddlewaretoken': csrfToken
        },
        dataType: "json",
        success: function(results){
            refreshToPortfolio(user_portfolio.portfolio_id)
            $('#modifyPortfolio').modal('hide');
        },
        error: function(data) {
            $("#modify-error #text").text(data.responseJSON.message)
            $("#modify-error").show()
        }
    })
    e.preventDefault();
});

$('#modifyPortfolio').on('hidden.bs.modal', function() {
    clear_table();
    $("#modify-error").hide()
});

$('#modifyPortfolio').on('show.bs.modal', function() {
    populate_table();
});
