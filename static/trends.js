 var $j = jQuery.noConflict();
 $j(function() {
     $j("#start_date").datepicker({
         dateFormat: 'yy-mm-dd',
         showButtonPanel: true
     });
 });
 $j(function() {
     $j("#end_date").datepicker({
         dateFormat: 'yy-mm-dd',
         showButtonPanel: true
     });
 });


 var selectedID = [];

 function searchBeers(value) {
     var myURL = "/beerdata/search_beers?q=" + value;
     $.ajax({
         url: myURL,
         type: 'GET',
         dataType: "json",
         success: function(resp) {
             document.getElementById("suggestions").style = "display:block";
             var i = 0;

             for (id in resp) {
                 document.getElementById("suggestion" + i).innerHTML = resp[id];
                 selectedID[i] = id;
                 i++;
             }
         },
         error: function(jqXHR, textStatus, errorThrown) {
             console.log(textStatus + ' ' + errorThrown);
         }
     });

 }

 function getBeerId(id) {
     for (var i = 0; i < 5; i++) {
         document.getElementById("suggestion" + i).style = "background-color:white";
     }
     document.getElementById("suggestion" + id).style = "background-color:lightgreen";
     document.getElementById("beer_id").value = selectedID[id];
 }



 function drawTrends(xDatas, yDatas) {
     var xData = xDatas;
     var yData = yDatas;

     //BubbleSort by Date
     for (var i = 0; i < xData.length - 1; i++) {
         for (var j = 0; j < xData.length - 1; j++) {
             if (xData[j] > xData[j + 1]) {
                 //Sort the xData
                 var temp = xData[j];
                 xData[j] = xData[j + 1];
                 xData[j + 1] = temp;
                 //Sort the yData Accordingly
                 var temp = yData[j];
                 yData[j] = yData[j + 1];
                 yData[j + 1] = temp;
             }
         }
     }

     //Used for rolling average
     var avgData = [];
     avgData[0] = yData[0];
     for (var i = 1; i < yData.length; i++) {
         avgData[i] = parseFloat(avgData[i - 1]) + parseFloat(yData[i]);
     }

     //Divide each entry by number of entries to get rolling Avg
     for (var i = 1; i < yData.length; i++) {
         avgData[i] = avgData[i] / (i + 1);
     }

     var data = [{
         x: xData,
         y: avgData,
         type: 'scatter',
         mode: 'lines',
         name: 'Average Ratings'
     }]

     var data2 = [{
         x: xData,
         y: yData,
         type: 'dot',
         name: 'Users Ratings'
     }]

     var layout = {
          title: 'Beer Trends Over Time',
          xaxis: {
            title: 'Dates',
            titlefont: {
              family: 'Arial, monospace',
              size: 20,
              color: '#1779ba'
            }
          },
          yaxis: {
            range: [0, 5],
            title: 'Ratings',
            titlefont: {
              family: 'Arial, monospace',
              size: 20,
              color: '#1779ba'
            }
          }
        };
     Plotly.newPlot('myDiv', data, layout);
     Plotly.plot('myDiv', data2, layout);
     document.getElementById("myDiv").style = "display:block;";
 }


 window.addEventListener("DOMContentLoaded", function() {
     var form = document.getElementById("form");
     document.getElementById("suggestions").addEventListener("click", function() {
         form.submit();
     })
 });