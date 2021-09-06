Token = localStorage.getItem("token")


function getDetailRawatJalan(id) {
  $.ajax({
    type: "GET",
    url: BASE_URL_PASIEN + "/rawatjalan/list?id=" + id,
    dataType: "JSON",
    "headers": {
      "Authorization": "Bearer " + TOKEN,
    },
    success: function (response) {
      $("#dtlRawatJalan").modal("show");
      antri = response.antrian
      adm = response.data_rawat_jalan
      $("#idadmission").html(adm.admission_rawat_jalan_id)
      status = ""
      Object.keys(adm).forEach(function (key) {
        $("div#" + key).html(adm[key]);
        if (adm["status"] == 1) {
          status = "Terdaftar"
        } else if (adm["status"] == 4) {
          status = "Batal"
        } else {
          status = adm["key"]
        }
        

        $("#status").html(status)
        $("button#batalkan").attr("data-id", adm.id)

      });
      if (status != "Baru") {
        $("button#batalkan").attr("hidden", true)
      }
      $("#no_antrian").html(antri["nomerantrian"])
    }
  })
}


$("button#batalkan").click(function (e) {
  if (confirm("Anda yakin ingin membatalkan jadwal ini? Jadwal yang sudah dibatalkan tidak dapat dikembalikan")) {
    $.ajax({
      type: "GET",
      url: BASE_URL_PASIEN + "/rawatjalan/cancel/" + $(this).data("id"),
      dataType: "JSON",
      "headers": {
        "Authorization": "Bearer " + TOKEN,
      },
      success: function (response) {
        console.log("sukses");
      },
      fail: function (response) {
        console.log(response["error"]);
      }
    });
  }
  $("#dtlRawatJalan").modal("hide");
  location.reload()
});
