  var price;
  var companyName;

  var search = function(){

    var search_text = document.getElementById('search_entry');

    $.ajax({
      url : "/api/"+search_text.value,
      type: "get",
      dataType: "json",
      success: function(results){
        price = results;
        getCompanyName();
      },      
      error: function(data) {
        alert("fail")
      }     
    });

    var getCompanyName = function(){

      $.ajax({
        url : "/api/name/"+search_text.value,
        type: "get",
        success: function(results){
          companyName = results;
          render();
        },
        error: function(data) {
        }  
      });   
    }        
  }

  var render = function(){
    var result_div =  document.getElementById('result');
    result_div.innerHTML ="<div class='well'><h3>"+companyName+'&nbsp;&nbsp;&nbsp;'+price+"</h3><br><button class='btn btn-primary'>Compare</button><div>";
    $("#search_stock").modal("show")
  }


