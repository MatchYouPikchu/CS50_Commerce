

function addToWatchlist(){

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    
        var data = $("#watchListBtn").val()
        $.ajax({
            type: 'POST',
            url: '/addItemToWatchlist',
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: JSON.stringify(data),
            processData:false,
            contentType:JSON,
            success: function(json){
                $("#watchListRemove").removeAttr("hidden");
                $("#watchListAdd").attr("hidden", true);
            }
        });
    
}

function removeWatchList(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    
    var data = $("#watchListBtn").val();
    $.ajax({
        type: 'POST',
        url: '/removeItemFromWatchlist',
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: JSON.stringify(data),
        processData:false,
        contentType:JSON,
        success: function(json){
            $("#watchListRemove").attr('hidden', true);
            $("#watchListAdd").removeAttr('hidden');
        }
    });
}



function listen(){

$("#closeListing").click(function(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
var data = $("#watchListBtn").val();

$.ajax({

        type: 'POST',
        url: '/closeListing',
        headers:{"X-CSRFToken": csrftoken},
        data: JSON.stringify(data),
        processData:false,
        contentType:JSON,
        success: function(json){
        window.location.reload();
        }
});
});


$("#submitBid").click(function(){

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    var data =[];
    data.push($("#watchListBtn").val(), $("#id_bid").val());
    $.ajax({
        type: 'POST',
        url: '/submitBid',
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: JSON.stringify(data),
        processData:false,
        contentType:JSON,
        success: function(data){
            alert(data.Status);
        }
    });
});

$("#submitComment").click(function(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
var data =[];
data.push($("#watchListBtn").val(), $("#id_comment").val());

$.ajax({
type: "POST",
url: "/submitComment",
headers: {
    "X-CSRFToken": csrftoken
},
contentType: JSON,
data: JSON.stringify(data),
processData: false,
success: function(json){
window.location.reload();
}


});

});

};
document.addEventListener("DOMContentLoaded", listen);