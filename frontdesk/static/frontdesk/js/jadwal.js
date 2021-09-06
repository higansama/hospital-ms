var aktifpoli = "all"
var idfaskes = objToken["id_faskes"]
var basedate = 0
var haris = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
var bulans = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

$.ajax({
  type: "GET",
  url: BASE_URL_GLOBAL + "/global/poli/" + idfaskes,
  dataType: "JSON",
  success: function (response) {
    localStorage.setItem("poli", JSON.stringify(response.data))
    var poli = "<option value='all' selected>Semua Poli</option>"
    response.data.forEach((v, i) => {
      var namapoli = v.poli
      if (i == 0) {
        poli += "<option value='" + v.id + "'>" + namapoli + "</option>"
        aktifPoli = v.id
        // loadDataDokter(aktifPoli, 0)
      } else {
        poli += "<option value='" + v.id + "'>" + namapoli + "</option>"
      }
    });
    LoadJadwalDokter()
    $("#listpoli").html(poli)
  }
});


$("#listpoli").change(function (e) {
  aktifpoli = $(this).val()
  LoadJadwalDokter()
});

$("#addJadwal").click(function (e) {
  e.preventDefault();
  $("#modalTambahJadwal").modal("show");

  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/global/poli/" + objToken["id_faskes"],
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN
    },
    success: function (response) {
      $("#datapoli").html("");
      polis = response["data"]
      select = ""
      $.each(polis, function (i, v) {
        if (i == 0) {
          select += "<option value='" + v.id + "' selected>" + v.poli + "</option>"
          loadDokter(v.id)
        } else {
          select += "<option value='" + v.id + "'>" + v.poli + "</option>"
        }
      });
      $("#datapoli").html(select);
    }
  });
});


function loadDokter(idpoli) {
  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/frontdesk/dokter/list/" + objToken["id_faskes"] + "/" + idpoli,
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN
    },
    success: function (response) {
      $("#dokter").html("");
      polis = response["data"]
      select = ""
      $.each(polis, function (i, v) {
        if (i == 0) {
          select += "<option value='" + v.id + "' selected>dr. " + v.nama + "</option>"
        } else {
          select += "<option value='" + v.id + "'>dr. " + v.nama + "</option>"
        }
      });
      $("#dokter").html(select);
    }
  });
}


$("#datapoli").change(function (e) {
  e.preventDefault();
  loadDokter($(this).val())
});


function LoadJadwalDokter() {
  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/frontdesk/jadwal/utama/dokter/" + aktifpoli + "?base=" + basedate,
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN
    },
    success: function (response) {
      data = JSON.parse(response.data)
      result = []
      $.each(data, function (i, v) {
        tmp = {
          "dokter": []
        }
        tmp["tanggal"] = v["tanggal"]
        // tmp["hari"] = haris[Object.keys(v)[0]]
        if (v["dokter"].length != 0) {
          $.each(v["dokter"], function (w, j) {
            objDokter = JSON.parse(j)
            tmp["dokter"].push(objDokter)
          });
          result.push(tmp)
        }
      });

      var tbl = ""
      result.forEach((v, i) => {
        tglserver = new Date(v["tanggal"])
        tglDktr = String(tglserver.getDate()).padStart(2, 0)
        blnDktr = String(tglserver.getMonth() + 1).padStart(2, 0)
        tahunDktr = String(tglserver.getFullYear())
        titimangsa = tglDktr + " " + bulans[tglserver.getMonth()] + " " + tahunDktr
        tbl += "<table class='table table-bordered text-center pb-4'>"
        tbl += "<tr>"
        tbl += "<th>Hari</th>"
        tbl += "<td colspan='4' class='text-center'>" + haris[tglserver.getDay()] + ", &nbsp;" + titimangsa + "</td>"
        tbl += "</tr>"
        tbl += "<tr>"
        tbl += "<th>Nama Dokter</th>"
        tbl += "<th>Poli</th>"
        tbl += "<th>Jam Praktek</th>"
        tbl += "<th>Jumlah Pasien</th>"
        tbl += "<th>Action</th>"
        tbl += "</tr>"
        if (v["dokter"].length != 0) {
          $.each(v["dokter"], function (w, j) {
            tbl += ListDokterGenerator(j)
          });
        }
        tbl += "</table><br>"
      });
      $("div#jadwal").html(tbl)

      // $("#dokter").html(opt);
    }
  });
}

function ListDokterGenerator(dataDokter) {
  var tbl = ""
  tbl += "<tr>"
  tbl += "<td>" + dataDokter["namadokter"] + "</td>"
  tbl += "<td>" + dataDokter["namapoli"] + "</td>"
  tbl += "<td>" + dataDokter["jam_mulai"] + " - " + dataDokter["jam_selesai"] + "</td>"
  tbl += "<td>" + dataDokter["jumlahpasien"] + "</td>";
  if (basedate != 0) {
    tbl += "<td><button class='btn btn-primary checkinDokter' data-idjadwal='" + dataDokter.id + "' disabled><span class='fa fa-check'></span></button></td>"
  } else {
    tbl += "<td><button class='btn btn-primary checkinDokter' data-idjadwal='" + dataDokter.id + "'><span class='fa fa-check'></span></button></td>"
  }
  tbl += "</tr>"
  return tbl;
};

$("#addJadwalDokter").submit(function (e) {
  e.preventDefault();
  $("#idfaskes").val(objToken["id_faskes"])

  dataJadwal = $(this).serialize();
  $.ajax({
    type: "POST",
    url: BASE_URL_GLOBAL + "/frontdesk/add/jadwal/dokter/" + $("#dokter").val(),
    data: dataJadwal,
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN
    },
    success: function (response) {
      $("#msg").html("Berhasil");
    },
    fail: function (response) {
      $("#msg").html("Terjadi Kesalahan, Silahkan Periksa Kembali Data Yang Anda Isi");
    }
  });
  $("#modalTambahJadwal").modal("hide");
  $("#msg").show();
  loadDokter(aktifpoli)


});


$(document).on("click", ".checkinDokter", function (e) {
  e.preventDefault();
  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/frontdesk/checkin/dokter/" + $(this).data("idjadwal"),
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN
    },
    success: function (response) {
      alert("Dokter Berhasil Checkin")
    },
    fail: function (response) {
      alert(JSON.parse(response)["error"])
    }
  });
})


$(".btnWeek").click(function (e) {
  if ($(this).data("week") == "prev") {
    basedate -= 7
  } else if ($(this).data("week") == "next") {
    basedate += 7
  } else {
    basedate = 0
  }
  LoadJadwalDokter()
});
