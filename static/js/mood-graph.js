var randomScalingFactor = function () {
    return Math.round(Math.random() * 5);
};
var randomColorFactor = function () {
    return Math.round(Math.random() * 255);
};
var randomColor = function (opacity) {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
};

var config = {
    type: 'line',
    data: {
        labels: ["1", "2", "3", "4", "5", "6", "7"],
        datasets: [{
            label: "My First dataset",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
            fill: false,
            borderDash: [5, 5],
        }]
    },
    options: {
        responsive: true,
        legend: {
            position: 'bottom',
        },
        hover: {
            mode: 'label'
        },
        scales: {
            x: {
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Month'
                }
            },
            y: {
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                },
                ticks: {
                    min: 0,
                    max: 5,
                    stepSize: 1,
                    suggestedMin: 0.5,
                    suggestedMax: 5.5,
                    callback: function (label, index, labels) {
                        switch (label) {
                            case 0:
                                return 'Happy';
                            case 1:
                                return 'Sad';
                            case 2:
                                return 'Neutral';
                            case 3:
                                return 'Anxious';
                            case 4:
                                return 'Angry';
                            case 5:
                                return 'Tired';
                            case 6:
                                return 'Depressed';
                            case 7:
                                return 'Emotional'
                            case 8:
                                return 'Sickly'
                        }
                    }
                },
                gridLines: {
                    display: false
                }
            }
        }
    }
};

$.each(config.data.datasets, function (i, dataset) {
    var background = randomColor(0.5);
    dataset.borderColor = background;
    dataset.backgroundColor = background;
    dataset.pointBorderColor = background;
    dataset.pointBackgroundColor = background;
    dataset.pointBorderWidth = 1;
});
var ctx = document.getElementById("canvas").getContext("2d");
window.myLine = new Chart(ctx, config);