function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

$(function() {
 let timerId = setInterval(function() {
     $.ajax({
            type: 'POST',
            url:  'waiting/' + getCookie('request_id'),
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            if(data['status'] == 'completed')
            {
                clearInterval(timerId);
                window.location = 'result';
            }
        }).fail(function(data){
            console.log('error!');
            clearInterval(timerId);
        });
  }, 1000);
    });

