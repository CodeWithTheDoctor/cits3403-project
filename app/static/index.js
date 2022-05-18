$(document).ready(function(){
    var totalSeconds = 0;



    $("#submitButton").click(function() {
        if (isSolved()) {   
            // stop timer
                // clearInterval(timer)
           
            // upload values to database
                /*$.ajax({
                    url  : '/api/puzzle/submit',
                    type : 'POST',
                    data : {'user_id' : ,
                            'puzzle_id' : ,
                            'time' : totalSeconds},
                    dataType : 'json',
                }) */

            // if solved then show leaderboard and stuff 
        } else {
            // show prompt that is not solved
            $("#demo").text("Not Solved");
        }
    });
});