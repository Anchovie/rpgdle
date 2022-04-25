$( document ).ready(function() {
  const locale = "fi-FI";
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  console.log( "ready!" );

  var dateArr = dates.split(",");
  console.log(dateArr);

  var startDate = dateArr[0];
  var startDate = Date.parse(startDate);
  console.log(new Date(startDate).toLocaleDateString("en-ZA", options));

  currentdate = new Date();
  var oneJan = new Date(currentdate.getFullYear(),0,1);
  var numberOfDays = Math.floor((currentdate - oneJan) / (24 * 60 * 60 * 1000));
  var result = Math.ceil(( currentdate.getDay() + 1 + numberOfDays) / 7);

  //console.log("days between the start "+ startDate +" and end "+ dateArr[dateArr.length-1] +" = " + getDayDiff(startDate, dateArr[dateArr.length-1]));

  //console.log("The monday of the week of the startdate ("+new Date(startDate).toDateString()+") is " + getMonday(startDate));

  let daysBetween = getDayDiff(startDate, dateArr[dateArr.length-1]);
  let $row1 = "<div class='daterow'>";
  let $row2 = "<div class='dayrow'>";

  let $column = $("<div class='column row_header'></div>");
  let header = "<div class='col_header'>";
  header += "<div class='calendar_date'> Date </div>";
  header += "<div class='calendar_day'> Day </div>";
  header += "</div>";
  $column.append($(header));

  for (let j = 0; j<users.length; j++) {
    let curUser = users[j];
    let activeString = "";
    if (curUser.name == loggedIn) {
      activeString = "active";
    }
    let $attendCell = $("<div class='calendar_cell calendar_name "+ activeString +"' data-for='"+ curUser.id +"'>"+ curUser.name +"</div>");
    $column.append($attendCell);
  }
  $("#calendar").append($column);

  for (let i = 0; i<=daysBetween; i++) {
    let newDate = addDays(startDate, i);
    let choosable = false;
    if (dates.includes(newDate.toLocaleDateString("en-ZA", options))){
      console.log("the date "+ newDate.toLocaleDateString("en-ZA", options) +" is in dates : " + dates);
      choosable = true;
    }
    let $column = $("<div class='column' data-choosable='" + choosable+ "' data-index='"+i+"' data-time='"+ newDate.toLocaleDateString("en-ZA", options) +"'></div>");
    let header = "<div class='col-header'>";
    header += "<div class='calendar_date' data-index='"+i+"'>" + newDate.toLocaleDateString(locale, options) + "</div>";
    header += "<div class='calendar_day'>" + newDate.toLocaleDateString("en-US", { weekday: 'long' }) + "</div>";
    header += "</div>";
    $column.append($(header));

    for (let j = 0; j<users.length; j++) {
      let curUser = users[j];
      let $attendCell = $("<div class='calendar_cell' data-for='"+ curUser.id +"' data-index='"+i+"' data-time='"+ newDate.toLocaleDateString("en-ZA", options) +"' data-choosable='" + choosable+ "'></div>");

      $attendCell.click(function(self) {
        console.log(self);
        console.log(self.target);
        console.log("Clicked a cell!");
        toggleCellState($(self.target));
      });
      $column.append($attendCell);
    }

    $("#calendar").append($column);
  }

  for (p of participations){
    console.log(p); // data-time='"+ p.date +"'
    console.log("user for participation = " + p.user);
    $("div[data-for='"+ p.user+"']","div[data-time='"+ p.date +"']").addClass(p.status=="okay"?"okay":"maybe");
    let s = p.status=="okay"? "" : "?"
    if (p.user == loggedInId) {
      console.log(p.user +" == " + loggedInId);
      if (! $("#hiddenDays").val().includes( $("#hiddenDays").val() + p.date + s + ",") ) {
        $("#hiddenDays").val( $("#hiddenDays").val() + p.date + s + ",");
      }
    }
    //$("#hiddenDays").val( $("#hiddenDays").val() +$("div[data-for='"+ loggedInId+"']","div[data-time='"+ p.date +"']").attr("data-time")+ s +",");
  }
  $("#hiddenDays").val($("#hiddenDays").val().replaceAll(",,",","));
  console.log($("#hiddenDays").val());

  //$elem.append($row1);
  //$elem.append($row2);

  function toggleCellState($elem) {
    console.log("checking " + $elem.attr("data-for") + " == " + loggedInId);
    if ($elem.attr("data-for") == loggedInId && $elem.attr("data-choosable")=="true") {
      if ($elem.hasClass("okay")){
        $elem.removeClass("okay");
        $elem.addClass("maybe");
        $("#hiddenDays").val( $("#hiddenDays").val().replace($elem.attr("data-time")+",", ""));
        if (!$("#hiddenDays").val().includes($elem.attr("data-time")+"?,")){
          $("#hiddenDays").val( $("#hiddenDays").val() +$elem.attr("data-time")+"?,");
        }
      } else if ($elem.hasClass("maybe")) {
        $elem.removeClass("maybe");
        $("#hiddenDays").val( $("#hiddenDays").val().replace($elem.attr("data-time")+"?,", ""));
      } else {
        $elem.addClass("okay");
        if (!$("#hiddenDays").val().includes($elem.attr("data-time")+",")){
          $("#hiddenDays").val( $("#hiddenDays").val() +$elem.attr("data-time")+",");
        }
      }
    }
    $("#hiddenDays").val($("#hiddenDays").val().replaceAll(",,",","));
    console.log($("#hiddenDays").val());
  }


  function getMonday(d) {
    d = new Date(d);
    var day = d.getDay(), diff = d.getDate() - day + (day == 0 ? -6:1);
    return new Date(d.setDate(diff));
  }

  function getDayDiff(d1, d2) {
    d1 = new Date(d1)
    d2 = new Date(d2)
    var diffTime = d2.getTime() - d1.getTime();
    return Math.ceil(diffTime / (1000 * 3600 * 24));
  }

  function addDays(d, days) {
    var result = new Date(d);
    result.setDate(result.getDate() + days);
    return result;
  }

});
