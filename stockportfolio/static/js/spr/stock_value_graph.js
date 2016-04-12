var overalValue;
function loadAllGraphs() {

    var currentTime = new Date()
    var dayBefore = new Date()
    dayBefore.setDate(dayBefore.getDate() - 1)

    function parseStringToArray(string){
        string = string.substring(1,string.length-1)
        string = string.split(", ")
        for (i = 0; i<string.length; i +=2){
            string[i] = new Date(string[i].substring(15,string[i].length-6))
        }
        return string
    }
    plotValues = function (id, timePeriod) {
        switch (timePeriod) {
            case "week" :
                var data = weekly_values;
                break;
            case "month" :
                var data = monthly_values;
                break;
            case "year" :
                var data = annual_values;
                break;
        }
        data = parseStringToArray(data)
        options["xaxis"]["min"] = (data[0].getTime())
        options["xaxis"]["max"] = (new Date()).getTime()
        tupledData = []
        var j = 0;
        for (i = 0; i< data.length; i+=2){
            tupledData[j] = new Array(data[i].getTime(),parseFloat(data[i+1]))
            j++;
        }
        console.log(tupledData)
        id = '#' + id
        $(id).empty();
        $.plot($(id), [{
            label: "Stock value in $",
            data: tupledData,
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
}

// Need to get these functions back out as global variables
loadAllGraphs();

