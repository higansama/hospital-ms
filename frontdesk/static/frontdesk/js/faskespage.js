BASE_URL = "http://localhost:8000"
function getDataFaskes() {
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
                row += "<td>" + v.faskes + "</td>"
                row += "<td>" + v.alamat + "</td>"
                row += "<td>" + v.kota + "</td>"
                row += "<td>"
                row += "<div class='btn-group' role='group' aria-label='Basic example'>"
                row += "<button data-toggle='tooltip' data-placement='left' title='Detail Faskes' type='button' class='btn btn-success dtlFaskes' data-idfaskes='" + v.id_faskes + "' ><span class='fa fa-eye'></span></button>"
                row += "<button data-toggle='tooltip' data-placement='top' title='Tambah Poli' type='button' class='btn btn-secondary addPoli' data-idfaskes='" + v.id_faskes + "'><span class='fa fa-plus'></span></button>"
                row += "<button data-toggle='tooltip' data-placement='right' title='Ubah Status Faskes' type='button' class='btn btn-secondary'><span class='fa fa-info'></span></button>"
                row += "</div>"
                row += "</td>"
                row += "</tr>"
            });
            $("#faskestable tbody").html(row);
        },
        error: function (response) {
            row = "<tr colspan='5'>"
            row = "<td>"
            row = response
            row = "</td>"
            row += "<tr>"
        }
    });
}
getDataFaskes();
$("#btnsimpanfaskesbaru").on("click", function (event) {
    event.preventDefault();
    token = localStorage.getItem('token');
    dataFaskes = $("form#addfaskes").serialize();
    $.ajax({
        type: "POST",
        url: BASE_URL + "/frontdesk/faskes/api/",
        data: dataFaskes,
        dataType: "JSON",
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

$(document).on("click", ".dtlFaskes", function (e) {
    idfaskes = $(this).data("idfaskes");
    window.location.replace(BASE_URL_GLOBAL + "/frontdesk/faskes/" + idfaskes)
});


$("#btnAddFaskes").click(function (e) { 
    e.preventDefault();
    $("#formTambahFaskes").modal("show");
    GetProvinsi($("select#provinsi"))
});


$(document).on("click", "select#provinsi", function (e){
    e.preventDefault();
    console.log("loadKota");
    LoadKota($("select#kota"), $(this).val());
});

$(document).on("click", "select#kota", function (e){
    e.preventDefault();
    LoadKecamatan($("select#kecamatan"), $(this).val());
});

$(document).on("click", "select#kecamatan", function (e){
    e.preventDefault();
    LoadKelurahan($("select#kelurahan"), $(this).val());

});


function listPoliTable(idfaskes) {
    $.ajax({
        type: "GET",
        url: BASE_URL_GLOBAL + "/global/faskes/detail/" + idfaskes,
        data: "data",
        dataType: "JSON",
        success: function (response) {
            dataFaskes = response["faskes"]
            poli = ""
            $("#poliFaskes tbody#listPoliFaskes").html("");
            $.each(response["poli"], function (i, v) {
                poli += "<tr>"
                poli += "<td>" + v.id + "</td>"
                poli += "<td>" + v.poli + "</td>"
                poli += "<td><button class='btn btn-success'><span class='fa fa-info' ></span></button></td>"
                poli += "</tr>"
            });
            $("#poliFaskes tbody#listPoliFaskes").html(poli);
        }
    });
}

let FaskesBaru;

$(document).on("click", ".addPoli", function (e) {
    e.preventDefault()
    $("#modalAddPoli").modal("show");
    idfaskes = $(this).data("idfaskes");
    // console.log(idfaskes);
    FaskesBaru = idfaskes;
});

$("#submitNewPoli").click(function (e) {
    e.preventDefault();
    urlSend = BASE_URL_GLOBAL + "/global/poli/" + FaskesBaru 
    console.log("LOL ", urlSend);
    $.ajax({
        type: "POST",
        url: urlSend,
        data: {
            "id_faskes": FaskesBaru,
            "poli": $("#poliname").val()
        },
        dataType: "JSON",
        success: function (response) {
            listPoliTable(FaskesBaru)
        },
        error: function (response) {
            console.log(response);
        }

    });
});

