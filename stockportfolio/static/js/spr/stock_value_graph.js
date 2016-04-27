var overalValue;
var price_history;
var risk_history;
var lbl;
function loadAllGraphs() {
    var currentTime = new Date()
    var dayBefore = new Date()
    dayBefore.setDate(dayBefore.getDate() - 1)
    function getValues(price_history, daysBack){
        price_values = [daysBack]
        var j = 0
        for (i = price_history.length-1; i>=price_history.length-daysBack ; i--){

            price_values[j] = new Array((new Date(price_history[i]["price_date"])).getTime(), price_history[i]["price_value"])
            j++

        }
        return price_values
    }


    function getRisks(risk_history, daysBack){
        risks = [daysBack]
        var j = 0
        for (i = risk_history.length-1; i>=risk_history.length-daysBack ; i--){
            risks[j] = new Array((new Date(risk_history[i]["risk_date"])).getTime(), risk_history[i]["risk_value"])
            j++
        }
        return risks
    }

    plotValues = function (id, timePeriod) {
        try{

            switch (timePeriod) {
                case "week" :
                    var data = getValues(price_history,7)
                    lbl = "Stock value in $";
                    break;
                case "month" :
                    var data = getValues(price_history,30)
                    lbl = "Stock value in $";
                    break;
                case "year" :
                    var data = getValues(price_history,price_history.length)
                    lbl = "Stock value in $";
                    break;
                case "rri_month" :
                    var data = getRisks(risk_history,risk_history.length);
                    lbl = "Stock risk variation";
                    break;
                case "rri_week" :
                    var data = getRisks(risk_history,7);
                    lbl = "Stock risk variation";
                    break;
            }
            options["xaxis"]["min"] = (data[0][data.length-1])
            options["xaxis"]["max"] = (new Date()).getTime()
            id = '#' + id
            $(id).empty();
            $.plot($(id), [{
                label: lbl,
                data: data,
                lines: {
                    fillColor: "rgba(250, 202, 89, 0.12)"
                },
                points: {
                    fillColor: "#fff"
                }
            }], options);
        }
        catch(err) {
            return
        }


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
}

// Need to get these functions back out as global variables
loadAllGraphs();
