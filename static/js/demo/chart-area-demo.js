// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'radar',
  data: {
    labels: [
    "Alcoolique",
    "Etheré",
    "Fruité",
    "Floral",
    "Houblonné",
    "Résineux",
    "Noix",
    "Herbeux",
    "Céréales",
    "Caramel",
    "Brulé"
    ],
    datasets: [{
      label: "",
      lineTension: 0.1,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: [
        Math.round({{ beer.alcoolique }}),
        Math.round({{ beer.ethere }}),
        Math.round({{ beer.fruite }}),
        Math.round({{ beer.floral }}),
        Math.round({{ beer.houblonne }}),
        Math.round({{ beer.resineux }}),
        Math.round({{ beer.noix }}),
        Math.round({{ beer.herbeux }}),
        Math.round({{ beer.cereales }}),
        Math.round({{ beer.caramel }}),
        Math.round({{ beer.brule }})
      ],
    }],
  },
  options: {
    legend: {
      display: false
    },
    maintainAspectRatio: true,
    layout: {
      padding: {
        left: 5,
        right: 5,
        top: 5,
        bottom: 0
      }
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 5,
      yPadding: 5,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 5,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel;
        }
      }
    }
  }
});
