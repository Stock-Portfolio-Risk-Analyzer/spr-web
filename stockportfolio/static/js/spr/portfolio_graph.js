var globalTestJsonString =  {
                            "risk_history": [{"risk_date": "2015-02-13 01:25:57.174532+00:00", "risk_value": 2.0},
                                             {"risk_date": "2015-05-13 01:25:57.174532+00:00", "risk_value": 3.0},
                                             {"risk_date": "2015-06-18 01:25:57.174532+00:00", "risk_value": 8.0},
                                             {"risk_date": "2015-08-13 01:25:57.174532+00:00", "risk_value": 9.0},
                                             {"risk_date": "2015-11-13 01:25:57.174532+00:00", "risk_value": 9.3},
                                             {"risk_date": "2016-01-01 01:25:57.174532+00:00", "risk_value": 10.0},
                                             {"risk_date": "2016-03-10 01:25:57.174532+00:00", "risk_value": 9.1},
                                             {"risk_date": "2016-03-12 01:25:57.174532+00:00", "risk_value": 4.0},
                                             {"risk_date": "2016-03-16 01:25:57.174532+00:00", "risk_value": 2.1},
                                             {"risk_date": "2016-03-17 00:10:57.174532+00:00", "risk_value": 4.0},
                                             {"risk_date": "2016-03-17 00:25:57.174532+00:00", "risk_value": 10.0}],
                            "portfolio_id": 1,
                            "sector_allocations": {
                                "Technology": 1.0
                            },
                            "date_created": "2016-03-17 05:36:14.761809",
                            "stocks": [{
                                "sector": "Other",
                                "name": "Google",
                                "price": 736.09,
                                "mkt_value": 736.09,
                                "ticker": "GOOG",
                                "quantity": 1
                            }],
                            "portfolio_userid": 2
                        }
$.ajax({
    dataType: "json",
    url: "/api/portfolio/1", 
    success: function(data) {

        var jsonString = []
        jsonString = globalTestJsonString["risk_history"]

        //jsonString = globalTestJsonString
        //console.log(jsonString["risk_history"].length)
        var risks = [jsonString.length]
        //console.log(jsonString)
        for (i = 0; i<jsonString.length;i++){
            risk = jsonString[i]
            risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
            console.log(risks[i])
        }
    }
});

        var currentTime = new Date()
        var dayBefore = new Date()
        dayBefore.setDate(dayBefore.getDate()-1)

        var weekFun = function (){
            options["xaxis"]["minTickSize"] = [1, "day"]
            var currentTime = new Date()
            var oneWeekAgo = new Date();
            oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
            options["xaxis"]["min"] = oneWeekAgo.getTime()
            options["xaxis"]["max"] = currentTime.getTime()
            timeformat: "%a"
            $.ajax({
                dataType: "json",
                url: "/api/portfolio/1", 
                success: function(data) {

                    var jsonString = []
                    //jsonString = data["risk_history"]
                    jsonString = globalTestJsonString["risk_history"]
                    var risks = [jsonString.length]
                                //console.log(jsonString)        

                                console.log(jsonString)
                                for (i = 0; i<jsonString.length;i++){
                                    risk = jsonString[i]
                                    risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
                                }
                                console.log(risks)
                                $.plot($("#placeholder3xx3"),[{
                                    label: "Beta",
                                    data: risks,
                                    lines: {
                                        fillColor: "rgba(150, 202, 89, 0.12)"
                                    },
                                    points: {
                                        fillColor: "#fff"
                                    }
                                }], options);

                            }
                        });

}
var yearFun = function (){
    var currentTime = new Date()
    options["xaxis"]["min"] = (new Date(currentTime.getFullYear()-1,0,1)).getTime()
    options["xaxis"]["max"] = currentTime.getTime()
    options["xaxis"]["minTickSize"] =[1, "month"]

    $.ajax({
        dataType: "json",
        url: "/api/portfolio/1", 
        success: function(data) {

            var jsonString = []
            //jsonString = data["risk_history"]
            jsonString = globalTestJsonString["risk_history"]

            var risks = [jsonString.length]
            for (i = 0; i<jsonString.length;i++){
                risk = jsonString[i]
                risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
            }


            $.plot($("#placeholder3xx3"),[{
                label: "Beta",
                data: risks,
                lines: {
                    fillColor: "rgba(250, 202, 89, 0.12)"
                },
                points: {
                    fillColor: "#fff"
                }
            }], options);

        }
    });

}
var allFun = function (){


    $.ajax({
        dataType: "json",
        url: "/api/portfolio/1",  
        success: function(data) {

            var jsonString = []
            //jsonString = data["risk_history"]
            jsonString = globalTestJsonString["risk_history"]
           
            var risks = [jsonString.length]
            for (i = 0; i<jsonString.length;i++){
                risk = jsonString[i]
                risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
            }
            options["xaxis"]["min"] = (new Date(jsonString[0]["risk_date"])).getTime()
            options["xaxis"]["max"] = (new Date()).getTime()
            $.plot($("#placeholder3xx3"),[{
                label: "Beta",
                data: risks,
                lines: {
                    fillColor: "rgba(250, 202, 89, 0.12)"
                },
                points: {
                    fillColor: "#fff"
                }
            }], options);

        }
    })

}
var options = {
    series: {
        curvedLines: {
            apply: true,
            active: true,
            monotonicFit: true
        }
    },
    colors: ["#26B99A"],
    grid: {
        borderWidth: {
            top: 0,
            right: 0,
            bottom: 1,
            left: 1
        },
        borderColor: {
            bottom: "#7F8790",
            left: "#7F8790"
        }
    },
    label: "Beta",
    xaxis: {
        minTickSize: [1, "hour"],
        min: dayBefore.getTime(),
        max: currentTime.getTime(),
        twelveHourClock: true,
        mode: "time",
                    tickLength: 0, // hide gridlines
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
                    axisLabelPadding: 5
                }
            }


            $.ajax({
                dataType: "json",
                url: "/api/portfolio/1", 
                success: function(data) {

                    var jsonString = []
                 //   jsonString = data["risk_history"]\
                    jsonString = globalTestJsonString["risk_history"]
                    var risks = [jsonString.length]
                    for (i = 0; i<jsonString.length;i++){
                        risk = jsonString[i]
                        risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
                    }


                    $.plot("#placeholder3xx3",[{
                        label: "Beta",
                        data: risks,

                        lines: {
                            fillColor: "rgba(250, 202, 89, 0.12)"
                        },
                        points: {
                            fillColor: "#fff"
                        }
                    }], options);

                }
            });