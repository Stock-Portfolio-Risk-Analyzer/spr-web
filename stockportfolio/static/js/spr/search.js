  var price;
  var companyName;

  var search = function(){

    var search_text = document.getElementById('search_entry');
    search_text = search_text.value.toUpperCase();

        var tickerUrl = "/api/" + search_text + "/details";
        $.ajax({
            url: tickerUrl,
            type: 'GET',
            success: function(data) {
                $('#search-warning').addClass('hidden');
                $('#stockInterface').html(data);
                $('#stockInterfaceModal').modal('show');
            },
            error: function(data) {
                $('#search-warning').removeClass('hidden');
            },
        });
  };


