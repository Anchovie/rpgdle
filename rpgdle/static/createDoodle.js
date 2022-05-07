$( document ).ready(function() {
    console.log( "ready!" );
    $("#mdp").multiDatesPicker({
    	dateFormat: "yy/mm/dd",
      onSelect: function() {
        console.log("CHANGED: VAL");
        console.log($("#mdp").val());
        console.log($("#mdp").multiDatesPicker('value'));
        console.log($("#mdp").multiDatesPicker('getDates'));
        $("#hiddenDates").val($("#mdp").multiDatesPicker('value'));
      }
    });
});
