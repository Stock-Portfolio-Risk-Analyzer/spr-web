$("#upload-portfolio").click(function(){
    $("#uploadPortfolioModal").modal("show");
});

$('#uploadportfolioform').submit(function(e){
    data = new FormData();
    data.append("file", $(this).find("#id_file").input.files[0])

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