$("#upload-portfolio").click(function(){
    $("#uploadPortfolioModal").modal("show");
});

$('#uploadportfolioform').submit(function(e){
    var data = new FormData($(this).get(0));
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('success');
        }
    });
    e.preventDefault();
});
