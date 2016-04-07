/**
 * Created by enriqueespaillat on 4/6/16.
 */
function populate_table(data) {
    var stocks = data.stocks;
    var currentCount = parseInt($("#stock-modify-count").val())
    for (var i = 0; i < stocks.length; i++) {
        var stock = stocks[i];
        var $clone = $("#portfolio-table").find('tr.clone').clone(true).removeClass("hide").removeClass('clone')
        $clone.find("input#symbol").val(stock.ticker).attr("readonly", "readonly")
        $clone.find("input#symbol").attr("name", "symbol_" + currentCount)
        $clone.find("input#quantity").val(stock.quantity)
        $clone.find("input#quantity").attr("name", "quantity_" + currentCount)
        $("#portfolio-table").append($clone)
        currentCount += 1
    }
    $("#stock-modify-count").val(currentCount)
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

$("#save-button").click(function(e) {
    $clone = $('#modify-portfolio-form')
    $clone.find("tr.hide.clone").remove()
    var form = {};
    form["symbols"] = {}
    form["quantities"] = {}
    $.each($clone.serializeArray(),
        function(i, field) {
            var dict = ""
            if(field.name.indexOf("symbol") > -1){
                var i = field.name.split("_").pop()
                form["symbols"][i] = field.value
            } else if (field.name.indexOf("quantity") > -1) {
                var i = field.name.split("_").pop()
                form["quantities"][i] = field.value
            }
        });
    var csrfToken = $clone.find("#csrf-token").val()
    $.ajax({
        url : "/api/portfolio/"+ user_portfolio.portfolio_id +"/modify",
        type: "post",
        data : {
            "data": JSON.stringify(form),
            'csrfmiddlewaretoken': csrfToken
        },
        dataType: "json",
        success: function(results){
            window.location.href = "/dashboard";
        },
        error: function(data) {
            $("#modify-error #text").text(data.responseJSON.message)
            $("#modify-error").show()
        }
    })
    e.preventDefault();
});

populate_table(user_portfolio);