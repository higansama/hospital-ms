BASE_URL = "http://localhost:8000"

function getDataFaskes(){
    $.ajax({
        type: "GET",
        url: BASE_URL + "/global/faskes/all",
        dataType: "JSON",
        success: function (response) {
            row = ""
            index = 0
            response.data.forEach((v, i) => {
                index += 1
                row += "<tr>"
                row += "<td>" + index.toString() + "</td>"
                row += "<td>"+ v.faskes +"</td>"
                row += "<td>" + v.kota + "</td>"
                row += "<td>" + v.status_faskes + "</td>"
                row += "<td>Action</td>"
                row += "</tr>"
            });
            $("#faskestable tbody").html(row);
        },
        error: function(response){
            row = "<tr colspan='5'>"
            row = "<td>"
            row =  response
            row = "</td>"
            row += "<tr>"
        } 
    });
}
getDataFaskes();
$("#btnsimpanfaskesbaru").on("click", function( event ) {
    event.preventDefault();
    token = localStorage.getItem('token');
    dataFaskes = $("form#addfaskes").serialize();
    $.ajax({
        type: "POST",
        url: BASE_URL + "/frontdesk/faskes/api/",
        data: dataFaskes,
        dataType: "dataType",
        headers: {
            "Authorization": "Bearer " + token
        },
        success: function (response) {
            Swal.fire(
                'Good job!',
                'You clicked the button!',
                'success'
              )
        }
    });
  });