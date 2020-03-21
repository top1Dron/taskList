$(document).ready(function(){
    $(document).on('click', '.remove', function(){
        $(this).parent().remove();
    });

    $(document).on('click', '.checkbox', function(){
        $(this).parent().addClass('completed');
        $(this).attr('disabled', true);
        var totalIncomplete = $("#total-incomplete");
        var oldValue = parseInt(totalIncomplete.text());
        if(oldValue > 1){
            totalIncomplete.html(" " + --oldValue);
        }else{
            console.log("here");
            $("#total-incompleted").html("");
        }
        

        uid = $(this).attr('data-uid');
        $.get("/api/complete/" + uid);
    });
});