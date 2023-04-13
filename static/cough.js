$(document).ready(function() {
  $('#audio-submit').on('click', function(e) {
      e.preventDefault();
  
      // Get form data
      var form_data = new FormData($('#upload-form')[0]);

      // Add additional parameters to the form data
      form_data.append('param1', $('#param1').val());
      form_data.append('param2', $('#param2').is(':checked') ? 1 : 0);
      form_data.append('gender', $('input[name=gender]:checked').val());
      form_data.append('param4', $('#param4').is(':checked') ? 1 : 0);
  
      // Send AJAX request to upload audio and get result
      $.ajax({
          type: 'POST',
          url: '/',
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

function handleFormSubmit(event) {
  event.preventDefault();
}
