$(document).ready(function() {
    $('#audio-submit').on('click', function(e) {
      e.preventDefault();
  
      // Get form data
      var form_data = new FormData($('#upload-form')[0]);
  
      // Send AJAX request to upload audio and get result
      $.ajax({
        type: 'POST',
        url: '/upload',
        data: form_data,
        contentType: false,
        processData: false,
        success: function(result) {
          // Update result on webpage
          $('#result').text(result);
        },
        error: function() {
          alert('Error uploading audio file!');
        }
      });
    });
  });
  