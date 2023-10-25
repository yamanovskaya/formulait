function showPreview(event){
if(event.target.files.length > 0){

 var mime_types = [ 'image/jpeg', 'image/png', 'image/tif'];
		// check if user has selected file OR not
    var selected_file = $('#uploadform');
    if(selected_file.length == 0) {
        alert('Please select file to upload.');
        return;
    }
    // Get the file uploaded
    var file = selected_file[0][0];

    // validate MIME type
    var ext = file.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
      break;
    default:
      alert('Not allowed');
      return;
	}


	 var form_data = new FormData($('#uploadform')[0]);
        $.ajax({
            type: 'POST',
            url: '/get_preview',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'text'
        }).done(function(result, textStatus, jqXHR){
            $("#file-ip-1-preview").attr("src",'data:image/png;base64,' + result);
            $("#file-ip-1-preview").css("display","block");
        }).fail(function(result){
            $("#file-ip-1-preview").attr("src",'data:image/png;base64,' + result.responseText);
            $("#file-ip-1-preview").css("display","block");
            console.log('error!');
        });
}
}

$(function() {
    $('#btn_process').click(function() {
		
		var mime_types = [ 'image/jpeg', 'image/png', 'image/tif'];
		// check if user has selected file OR not
    var selected_file = $('#uploadform');
    if(selected_file.length == 0) {
        alert('Please select file to upload.');
        return;
    }
    // Get the file uploaded
    var file = selected_file[0][0];
    
    // validate MIME type
    var ext = file.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
      break;
    default:
      alert('Not allowed');
      return;
	}
 
     
	 var form_data = new FormData($('#uploadform')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log('Success!');
            document.cookie = "request_id="+data['request_id'];
            window.location = 'processing';
        }).fail(function(data){
            console.log('error!');
        });
	 
    });
});

