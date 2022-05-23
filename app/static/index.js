/**
 * JS that handles game page styling and db connection
 */

// init seconds for timer globally
let totalSeconds = 0;

/**
 * Timer Functions
 */

function startTimer() {
  timer = setInterval(setTime, 1000);
}


function setTime() {
  ++totalSeconds;
  $("#seconds").html(pad(totalSeconds % 60));
  $("#minutes").html(pad(parseInt(totalSeconds / 60)));
}


/**
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
 * Table generation
 */

/**
 * create a table with fastest 5 times
 * @param leaderboard 
 */
function generateTable(leaderboard) {
  for(let result = 0; result < 5; result++) {
    try {
      var position = result + 1;
      var username = leaderboard[result].username;
      var time     = leaderboard[result].time;
    } catch (error) {
      var username = "- -";
      var time     = "- -";    
    } finally {
      let markup = `<tr><td>${position}</td><td>${username}</td><td>${time}</td></tr>`;
      $("#table-body").append(markup);
    }
  }
}


function generateShare() {
  // add share message
  let shareMessage = `I completed Akari puzzle ${puzzle_id} in ${$("#minutes").html()}:${$("#seconds").html()}mins\nPlay here: http://localhost:5000`;
  $("#game-results").attr("value", shareMessage);
  $("#game-results").attr("placeholder",shareMessage);


  /**
   * event handlers for share buttons
   */
  let shareUrl = shareMessage.replace("\n", "%0A");
  // tweet
  $('#twitterButton').click(function() {
    window.open(`https://twitter.com/intent/tweet?text=${shareUrl}`);
  });

  // post to facebook
  $('#facebookButton').click(function() {
    window.open(`https://twitter.com/intent/tweet?text=${shareUrl}`);
  });

  // copy to clipboard
  $('#copyButton').click(function myFunction() {
    // Copy the text inside the text field
    navigator.clipboard.writeText(shareMessage);

    // Alert that text is copied
    $("#copied").text("Copied!");
  });
}


/**
 * API calls
 */

/**
 * uploads result to db
 * @param {*} result 
 * @returns response
 */
async function postResult(result) {
  const response = await $.ajax({
    url  : "/api/puzzle/submit",
    type : "POST",
    data : JSON.stringify(result),
    contentType: "application/json",
    success: function(response, data) {
      console.log(response)
    },
    error: function(xhr, response, error) {
      console.log(xhr.responseText)
      console.log(xhr.statusText)
      console.log(response)
      console.log(error)
    }
  })

  return response;
}

/**
 * fetches leaderboard
 * @param {*} puzzle_id 
 * @returns 
 */
async function getLeaderboard(puzzle_id) {
  const response = await $.ajax({
    url: `api/leaderboard/${puzzle_id}`,
    type: "GET",
    dataType: "json",
    success: function (data) {
      console.log(data);
    },
    error: function(xhr, response, error) {
      console.log(xhr.responseText)
      console.log(xhr.statusText)
      console.log(response)
      console.log(error)
    }
  })

  return response;
}


 /**
  * select and render puzzle once start is clicked
  */
 $("#startButton").on("click", function () {
  $.ajax({
    url: `/api/puzzle/${user_id}`,
    type: "GET",
    dataType: "json",
    success: function (data) {
      console.log(data);
    }
  }).done(function (data) {
    let puzzleString = data.config;
    puzzle_id = data.puzzle_id;

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
    $("#grid-box").fadeIn();
    $("#gameOverlay").fadeOut();
  })
})


/**
*  check and submit puzzle when button clicked
*/
$("#submitButton").click(async function () {
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
    await postResult(submission)
    // get leaderboard data
    let leaderboard = await getLeaderboard(puzzle_id);

    console.log(leaderboard);

    /*
     * generate results content
    */
    
    // display time on modal
    $( ".timer" ).clone().appendTo( "#modal-time" );

    // update leaderboard title
    $("#table-title").html(`Top 5 Leaderboard - Puzzle ${puzzle_id}`)
    // generate rows of table
    generateTable(leaderboard);
    // generate share function of modal
    generateShare();


    // open modal
    $("#results-modal").modal("show");

    // show results button
    $("#results-container").show();

  } else {
    // show prompt that is not solved
    $("#wrong-text").text("Not Solved");
  }
});


/**
 * loads rendergrid on document ready
 */
$(document).ready(function () {
  // render blank grid - with no click
  renderGrid();
});