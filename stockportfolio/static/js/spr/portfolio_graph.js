var weekFun, yearFun, allFun;
function loadAllGraphs() {
    var jsonString = []
    jsonString = user_portfolio["risk_history"]
    var risks = [jsonString.length]
    for (i = 0; i < jsonString.length; i++) {
        risk = jsonString[i]
        risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
        console.log(risks[i])
    }

    var currentTime = new Date()
    var dayBefore = new Date()
    dayBefore.setDate(dayBefore.getDate() - 1)

     weekFun = function () {
        options["xaxis"]["minTickSize"] = [1, "day"]
        var currentTime = new Date()
        var oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
        options["xaxis"]["min"] = oneWeekAgo.getTime()
        options["xaxis"]["max"] = currentTime.getTime()
        timeformat: "%a"

        jsonString = user_portfolio["risk_history"]
        var risks = [jsonString.length]

        console.log(jsonString)
        for (i = 0; i < jsonString.length; i++) {
            risk = jsonString[i]
            risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
        }
        $("#placeholder3xx3").empty();
        $.plot($("#placeholder3xx3"), [{
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
    yearFun = function () {
        var currentTime = new Date()
        options["xaxis"]["min"] = (new Date(currentTime.getFullYear() - 1, 0, 1)).getTime()
        options["xaxis"]["max"] = currentTime.getTime()
        options["xaxis"]["minTickSize"] = [1, "month"]

        jsonString = user_portfolio["risk_history"]

        var risks = [jsonString.length]
        for (i = 0; i < jsonString.length; i++) {
            risk = jsonString[i]
            risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
        }

        $("#placeholder3xx3").empty();
        $.plot($("#placeholder3xx3"), [{
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
    allFun = function () {

        jsonString = user_portfolio["risk_history"]

        var risks = [jsonString.length]
        for (i = 0; i < jsonString.length; i++) {
            risk = jsonString[i]
            risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
        }
        options["xaxis"]["min"] = (new Date(jsonString[0]["risk_date"])).getTime()
        options["xaxis"]["max"] = (new Date()).getTime()

        $("#placeholder3xx3").empty();
        $.plot($("#placeholder3xx3"), [{
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


    jsonString = user_portfolio["risk_history"]
    var risks = [jsonString.length]
    for (i = 0; i < jsonString.length; i++) {
        risk = jsonString[i]
        risks[i] = new Array(new Date(risk["risk_date"]).getTime(), risk["risk_value"])
    }

    $("#placeholder3xx3").empty();
    $.plot("#placeholder3xx3", [{
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

// Need to get these functions back out as global variables
loadAllGraphs();

