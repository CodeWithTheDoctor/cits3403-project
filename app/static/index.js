$(document).ready(function(){
  // init seconds for timer
  var totalSeconds = 0;

  // render blank grid - with no click
  renderGrid();

  // select and render puzzle once start is clicked
  $("#startButton").on("click",function() {
    $.ajax({
      url: "http://127.0.0.1:5000/api/puzzle/2",
      success: function(result) {
        $("#div1").html(result.config)

      }
    }).done(function(response) {
      console.log(response)

      // hide start button
      $("#startButton").hide(400);

      // start timer

      // remove child elements of grid box then render puzzle
      $("#grid-box").empty();
      parseGrid(exampleLevel);
      $("#grid-box").hide();
      renderGrid();
      $("#grid-box").show(200, "swing");
      $("#gameOverlay").hide(400);
    })
  })

  // check and submit puzzle when button clicked
  $("#submitButton").click(function() {
    if (isSolved()) {

      // stop timer
        // clearInterval(timer)
      
      // upload values to database
        $.ajax({
          url  : '/api/puzzle/submit',
          type : 'POST',
          data : {'user_id' : user_id,
              'puzzle_id' : 1,
              'time' : totalSeconds},
          dataType : 'json',
        })

      // if solved then show leaderboard and stuff 
    } else {
      // show prompt that is not solved
      $("#demo").text("Not Solved");
    }
  });
});