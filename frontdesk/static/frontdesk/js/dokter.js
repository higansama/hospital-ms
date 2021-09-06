LoadFaskes()
$("#addDokter").click(function (e) { 
  e.preventDefault();
  $("#modalAddDokter").modal("show");
  listFaskes = LoadFaskes();
  $("#id_faskes").html(localStorage.getItem("listFaskes"));
});

$("#id_faskes").change(function (e) { 
  e.preventDefault();
  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/global/poli/" + $(this).val(),
    dataType: "JSON",
    success: function (response) {
        response.data.forEach((v, i) => {
            $("#id_poli").append(`<option value="${v.id}">${v.poli}</option>`);
        });
    }
});
});