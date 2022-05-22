/**
 * JS that handles game page styling and db connection
 */

// init seconds for timer globally
let totalSeconds = 0;

function startTimer() {
  timer = setInterval(setTime, 1000);
}

/**
 * 
 */
function setTime() {
  ++totalSeconds;
  $("#seconds").html(pad(totalSeconds % 60));
  $("#minutes").html(pad(parseInt(totalSeconds / 60)));
}

/**
 * 
 * @param val value of total seconds 
 * @returns returns val in formatted string form
 */
function pad(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}


/**
 * 
 */
$(document).ready(function(){
  // render blank grid - with no click
  renderGrid();

  // select and render puzzle once start is clicked
  $("#startButton").on("click",function() {
    $.ajax({
      url: `/api/puzzle/${user_id}`,
      type: "GET",
      dataType: "json",
      success: function(data) {
        console.log(data);
      }
    }).done(function(data) {
      let puzzleString = data.config;
      puzzle_id        = data.puzzle_id;

      // start timer
      startTimer();

      // hide start button
      $("#startButton").hide(400);
      // enable Submit button
      $("#submitButton").removeAttr("disabled");

      // remove child elements of grid box then render puzzle
      $("#grid-box").empty();
      parseGrid(puzzleString);
      $("#grid-box").hide();
      renderGrid();
      $("#grid-box").show(200, "swing");
      $("#gameOverlay").hide(400);
    })
  })

  // check and submit puzzle when button clicked
  $("#submitButton").click(function() {
    if (isSolved()) {
      // hide wrong text after submit
      $("#wrong-container").hide();

      // disable submit button
      $("#submitButton").attr("disabled", "");

      // stop timer
      clearInterval(timer);

      // create puzzle submission obj
      submission  = {
        user_id: user_id,
        puzzle_id: puzzle_id,
        time: totalSeconds
      };
      
      // upload submission to database
        $.ajax({
          url  : "/api/puzzle/submit",
          type : "POST",
          data : JSON.stringify(submission),
          dataType : "json",
          contentType: "application/json",
          success: function(response, data) {
            console.log(response)
            console.log(data)
          },
          error: function(xhr, response, error) {
            console.log(xhr.responseText)
            console.log(xhr.statusText)
            console.log(response)
            console.log(error)
          },
        })

      // if solved then show leaderboard and stuff
      $("#solvedModal").modal("show");

    } else {
      // show prompt that is not solved
      $("#wrong-text").text("Not Solved");
    }
  });
});