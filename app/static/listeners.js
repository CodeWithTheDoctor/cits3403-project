var submitButton = document.getElementById("submitButton");
var solvedModal  = document.getElementById("solvedModal");

submitButton.addEventListener("click", function() {
    if (isSolved()) {
        // upload values to database
        // if solved then show leaderboard and stuff 
    } else {
        // show prompt that is not solved
        document.getElementById("demo").innerHTML = "Not Solved";
    }
});