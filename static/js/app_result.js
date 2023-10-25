function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

$(function() {
  $.ajax({
            type: 'POST',
            url:  'get_result/' + getCookie('request_id'),
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
             $("#value_clusters").html(data['clusters']);
        }).fail(function(data){
            console.log('error!');
        });

    $.ajax({
            type: 'GET',
            url:  'get_image/' + getCookie('request_id'),
            contentType: "image/png",
        }).done(function(result){
             $("#image_clusters").attr("src",'data:image/png;base64,' + result);
        }).fail(function(data){
            console.log('error!');
        });
    });

