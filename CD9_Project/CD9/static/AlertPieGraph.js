var dataPie = [
    {
        value: 60,
        color: "#F7464A",
        highlight: "#FF5A5E",
        label: "Porn"
    },
    {
        value: 20,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "New Apps"
    },
    {
        value: 10,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "New contact"
    },
    {
        value: 10,
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Yellow"
    }
];

var optionsPie =
    {
        tooltipEvents: [],
    
        showTooltips: true,

        onAnimationComplete: function () {
                this.showTooltip(this.segments, true);
            },

        //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke : true,

        //String - The colour of each segment stroke
        segmentStrokeColor : "#fff",

        //Number - The width of each segment stroke
        segmentStrokeWidth : 2,

        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout : 0, // This is 0 for Pie charts

        //Number - Amount of animation steps
        animationSteps : 100,

        //String - Animation easing effect
        animationEasing : "easeOutBounce",

        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : true,

        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale : true,

        //String - A legend template
        legendTemplate : "<ul class=\"<\%=name.toLowerCase()\%>-legend\"><\% for (var i=0; i<segments.length; i++){\%><li><span style=\"background-color:<\%=segments[i].fillColor\%>\"></span><\%if(segments[i].label){\%><\%=segments[i].label\%><\%}\%></li><\%}\%></ul>"

    };

    var alertContext = document.getElementById("alert-catagory-graph").getContext("2d");
    //var appContext = document.getElementById("app-catagory-graph").getContext("2d");
    // For a pie chart
    var myAlertPieChart = new Chart(alertContext).Pie(dataPie,optionsPie);
