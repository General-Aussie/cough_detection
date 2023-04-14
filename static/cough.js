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

    const resclass = document.getElementById('news');
    // Send AJAX request to upload audio and get result
    $.ajax({
      type: 'POST',
      url: '/home',
      data: form_data,
      contentType: false,
      processData: false,
      success: function(response) {
          var result = response.result;
          if (result == "Covid-19"){
            resclass.classList.add('covid');
            resclass.classList.remove('healthy');
            resclass.classList.remove('symptom');
          }
          else if (result == "Healthy"){
            resclass.classList.add('healthy');
            resclass.classList.remove('covid');
            resclass.classList.remove('symptom');
          }
          else if (result == "Symptomatic"){
            resclass.classList.add('symptom');
            resclass.classList.remove('healthy');
            resclass.classList.remove('covid');
          }
      
          // Display result on HTML page
          $('#news').text(result);
      },
      error: function() {
          alert('Error uploading audio file!');
      }
  });
    // Send AJAX request to upload audio and get result
    // ...
  });
});

function handleFormSubmit(event) {
  event.preventDefault();
}

var images = document.querySelectorAll('.disp img');
var index = 0;

// show the first image
images[index].classList.add('active');

function prevImage() {
  // hide the current image
  images[index].classList.remove('active');
  // get the index of the previous image
  index = (index - 1 + images.length) % images.length;
  // show the previous image
  images[index].classList.add('active');
}

function nextImage() {
  // hide the current image
  images[index].classList.remove('active');
  // get the index of the next image
  index = (index + 1) % images.length;
  // show the next image
  images[index].classList.add('active');
}
