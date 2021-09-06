$(".edit").hide();
$("#btnAddAdmin").click(function (e) {
  e.preventDefault();
  $("#mdlAddAdmin").modal("show");
});


$("form#addAdmin").submit(function (e) {
  e.preventDefault();
  let form = $(this).serialize();
  var sqSetting = {
    "url": "localhost:8000/frontdesk/account/",
    "method": "POST",
    "timeout": 0,
    "headers": {
      "Cookie": "csrftoken=BcYXh8sPxv6oe0j5dGWoZhYkfB5n6xoX80BXGw9YJ5rBDsnNa6Z1zgOB2loOb3Ez; sessionid=ygge0rfeffbtxa9aerlewahm1l27257e"
    },
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
  }
  $.ajax({
    sqSetting,
    success: function (response) {
      console.log(response);
    }
  });


});