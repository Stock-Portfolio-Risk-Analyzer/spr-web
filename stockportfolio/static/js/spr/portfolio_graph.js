var portfolio = ["AAPL", "YHOO"];  
var getPortfolioSize = function(){
    return portfolio.length;
}
                  
var jsonString =   { "timetags": [ "Thu Mar 6 2014 20:08:26 GMT-0600 (CST)",
                                   "Fri Mar 6 2015 20:08:26 GMT-0600 (CST)",
                                   "Sun Sep 6 2015 20:08:26 GMT-0600 (CST)",
                                   "Mon Mar 6 2016 20:08:26 GMT-0600 (CST)",
                                   "Tue Mar 7 2016 20:08:26 GMT-0600 (CST)",
                                   "Wed Mar 8 2016 20:08:26 GMT-0600 (CST)",
                                   "Thu Mar 9 2016 20:08:26 GMT-0600 (CST)",
                                   "Fri Mar 10 2016 20:08:26 GMT-0600 (CST)",
                                   "Sat Mar 11 2016 20:08:26 GMT-0600 (CST)",
                                   "Sun Mar 12 2016 20:08:26 GMT-0600 (CST)"
                                   //"Tue Apr 12 2016 20:08:26 GMT-0600 (CST)"
                                  ],
                      "risk": [0.8,
                               10.1,
                               2.1,
                               5.1,
                               1.0,
                               2.0,
                               8.0,
                               7.7,
                               10.5,
                               1.1
                               ]
                    }
var risks = [jsonString["timetags"].length]
for (i = 0; i < jsonString["timetags"].length; i++){
    risks[i] = new Array(new Date(jsonString["timetags"][i]).getTime(),jsonString["risk"][i])
}
var weekFun = function (){
    options["xaxis"]["minTickSize"] = [1, "day"]
    var currentTime = new Date()
    var oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    options["xaxis"]["min"] = oneWeekAgo.getTime()
    options["xaxis"]["max"] = currentTime.getTime()
    timeformat: "%a"
}
var yearFun = function (){
    var currentTime = new Date()
    options["xaxis"]["min"] = (new Date(currentTime.getFullYear()-1,0,1)).getTime()
    options["xaxis"]["max"] = currentTime.getTime()
    options["xaxis"]["minTickSize"] =[1, "month"]

}
var allFun = function (){
    options["xaxis"]["min"] = (new Date(jsonString["timetags"][0])).getTime()
    options["xaxis"]["max"] = (new Date()).getTime()

}
var currentTime = new Date()
var dayBefore = new Date()
dayBefore.setDate(dayBefore.getDate()-1)

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
    $("#week").click(function () {
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
    });

    $("#year").click(function () {
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
    });
    $("#all").click(function () {
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
    });

