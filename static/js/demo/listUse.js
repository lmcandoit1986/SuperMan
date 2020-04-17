$(function () {
    var all = eval('(' + '{{ person|safe }}' + ')');
    var rateAndroid = all.rate.android
    console.log(rateAndroid)
    var lineData = {
        labels: ["1", "2", "3", "4", "5", "6", "7"],

        datasets: [

            {
                label: "android",
                backgroundColor: 'rgba(26,179,148,0.5)',
                borderColor: "rgba(26,179,148,0.7)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: rateAndroid
            }
            // },{
            //     label: "Data 2",
            //     backgroundColor: 'rgba(220, 220, 220, 0.5)',
            //     pointBorderColor: "#fff",
            //     data: [65, 59, 80, 81, 56, 55, 40]
            // }
        ]
    };

    var lineOptions = {
        responsive: true
    };


    var ctx = document.getElementById("lineChart").getContext("2d");
    new Chart(ctx, {type: 'line', data: lineData, options:lineOptions});

    var ctx1 = document.getElementById("lineChart1").getContext("2d");
    new Chart(ctx1, {type: 'line', data: lineData, options:lineOptions});

});