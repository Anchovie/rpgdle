$( document ).ready(function() {
    console.log( "ready!" );
    $("#mdp").multiDatesPicker({
    	dateFormat: "yy/mm/dd",
      onSelect: function() {
        /*
        console.log("CHANGED: VAL");
        console.log($("#mdp").val());
        */
        console.log($("#mdp").multiDatesPicker('value'));
        //console.log($("#mdp").multiDatesPicker('getDates'));
        $("#hiddenDays").val($("#mdp").multiDatesPicker('value'));
        console.log($("#hiddenDays").val());
      }
    });
});
