var aktifPoli = "all";
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;
hariIni = $("#basedate").html(today)
baseDate = 0
$("#divError").hide();
// get poli
$.ajax({
  type: "GET",
  url: BASE_URL_GLOBAL + "/global/poli/" + objToken["id_faskes"],
  dataType: "JSON",
  success: function (response) {
    poli = ""
    poli += "<option value='all'>Semua</option>"
    response.data.forEach((v, i) => {
      poli += "<option value='" + v.id + "'>" + v.poli + "</option>"
    });
    $("#titlePoli").html(poli);
    loadDataDokter("all", 0);
  }
});

$("#titlePoli").change(function (e) {
  e.preventDefault();
  aktifPoli = $(this).val()
  loadDataDokter($(this).val(), baseDate);
});

function LinkGenerator(objDokter, titimangsa, jammulai, objData) {
  str = ""
  str += "<li class='list-group-item' style='padding-botom:0.3rem;padding-right:0rem;padding-left:0rem'>"
  str += "<div class='row'>"
  // pasien queue
  str += "<div class='col-2 text-center pt-4 pr-1'>"
  str += "<span style='cursor:pointer' class='fa fa-calendar-check-o fa-2x dtlJadwal' data-titimangsa='" + titimangsa + "' data-idjadwal='" + objDokter.id + "'></span>"
  str += "</div>"
  // dokter checkin button
  str += "<div class='col-8'>"
  str += "[" + objDokter.id + "]dr. " + NamaPanggilan(objDokter.namadokter) + "<br>"
  str += objDokter.jam_mulai + " - " + objDokter.jam_selesai + " <br> Pasien Terdaftar: " + objDokter.jumlahpasien
  str += "</div>"
  str += "</div>"
  str += "</li>"
  return str
}

function loadDataDokter(idpoli, baseDate) {
  var haris = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
  var bulans = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

  var dateArray = getDates(new Date(), (new Date()).addDays(6));

  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/pasien/list/jadwal/dokter/" + idpoli + "/all?base=" + baseDate,
    dataType: "JSON",
    "headers": {
      "Authorization": "Bearer " + TOKEN,
    },
    success: function (response) {
      data = JSON.parse(response.data)
      result = []
      $.each(data, function (i, v) {
        tmp = {
          "dokter": []
        }
        tmp["tanggal"] = v["tanggal"]
        tmp["hari"] = haris[Object.keys(v)[0]]
        if (v["dokter"].length != 0) {
          $.each(v["dokter"], function (w, j) {
            objDokter = JSON.parse(j)
            tmp["dokter"].push(objDokter)
          });
          result.push(tmp)
        }
      });

      let thead = "";
      let tdjadwal = ""

      let row = ""
      result.forEach((v, i) => {
        let tglserver = new Date(v["tanggal"])
        let tglDktr = String(tglserver.getDate()).padStart(2, 0)
        let blnDktr = String(tglserver.getMonth() + 1).padStart(2, 0)
        let tahunDktr = String(tglserver.getFullYear())
        let titimangsa = tahunDktr + "-" + blnDktr + "-" + tglDktr
        row += "<div class='col-md-6 col-xs-12'>"
        row += "<div class='card'>"
        if (baseDate == 0 && i == 0) {
          row += "<div class='card-header bg-success' style='padding-top:1rem; padding-bottom:1rem'>"
        } else {
          row += "<div class='card-header' style='padding-top:1rem; padding-bottom:1rem'>"
        }
        row += "<h5>" + haris[tglserver.getDay()] + "</h5><h6 class='pull-right' style='font-size:small'>" + String(tglserver.getDate()) + " " + bulans[tglserver.getMonth()] + ", " + tglserver.getFullYear() + "</h6>"
        row += "</div>"
        row += "<div class='card-body pl-3 pt-0' style='font-size:normal'>"
        row += "<ul class='list-group list-group-flush' >"
        if (v["dokter"].length != 0) {
          $.each(v["dokter"], function (w, j) {
            row += LinkGenerator(j, titimangsa, j["jam_mulai"], j)
          });
        }
        row += "</ul>"
        row += "</div>"
        row += "</div>"
        row += "</div>"
      });

      $("div#calendar").html(row);
    },
    fail: function (response) {
      console.log(response);
    }
  });



  // clean up table
}

function getWeek(wkt) {
  if (wkt == 'prev') {
    // dikurangi waktu 1 minggu yang lalu
    baseDate = baseDate - 7
  } else if (wkt == 'next') {
    // ditambah waktu 1 minggu yang akan datang
    baseDate = baseDate + 7
  } else {
    baseDate = 0
  }
  loadDataDokter(aktifPoli, baseDate)
}

function GantiFormattglPython(tgl) {
  spl = tgl.split("/")
  tgl = new Date(spl[2], spl[0], spl[1])
  var dd = String(tgl.getDate()).padStart(2, '0');
  var mm = String(tgl.getMonth()).padStart(2, '0'); //January is 0!
  var yyyy = tgl.getFullYear();
  result = yyyy + '-' + mm + '-' + dd;
  return result
}

function FormatToDateTime(tgl) {
  var dd = String(tgl.getDate()).padStart(2, '0');
  var mm = String(tgl.getMonth()).padStart(2, '0');
  var yyyy = tgl.getFullYear();
  result = yyyy + '-' + mm + '-' + dd;
  return result
}

function NamaPanggilan(nama) {
  spl = nama.split(" ");
  if (spl.length <= 2) {
    return spl[0]
  } else {
    return spl[1]
  }
}

function OlahResponJadwal(datearray, dataResponse) {
  dataHasil = []
  datearray.forEach((v, i) => {
    dayNumber = v.getDay()
    tmp = {
      "day": v,
      "daynumber": dayNumber,
      "dokters": []
    }
    dataResponse.forEach((w, j) => {
      if (w["jadwal_praktek"] == String(dayNumber)) {
        tmp["dokters"].push(w)
      }
    });
    dataHasil.push(tmp);
  });
  return dataHasil
}

usedidpoli = ""
$(document).on("click", "a.nav-link", function () {
  idpoli = $(this).data("idpoli");
  usedidpoli = idpoli;
  loadDataDokter(idpoli)
});

$(document).on("click", ".dtlJadwal", function (e) {
  idjadwal = $(this).data("idjadwal");
  titimangsa = $(this).data("titimangsa");
  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/frontdesk/list/antrian/" + $(this).data("idjadwal") + "/" + $(this).data("titimangsa"),
    dataType: "JSON",
    "headers": {
      "Authorization": "Bearer " + TOKEN,
    },
    success: function (response) {
      $("#mdlDetailRawatJalan").modal("show");
      data = response;
      let tr = "";
      $("#antrian tbody").html("");
      $.each(data, function (i, v) {
        console.log(v["status_checkin"]);
        let checkin = "Belum";
        if (v["status_checkin"]) {
          checkin = "Sudah";
        }
        tr += "<tr>"
        tr += "<td>" + v["nomerantrian"] + "</td>"
        tr += "<td>" + v["admission_rawat_jalan_id"] + "</td>"
        tr += "<td>" + v["nama_pasien"] + "</td>"
        tr += "<td>" + checkin + "</td>"
        tr += "<td> "
        tr += "<div class='btn-group' role='group' aria-label='Basic example'>"
        tr += "<button type='button' class='btn btn-primary BtnCheckinPasien' data-idantrian='" + v["id"] + "'>Checkin Pasien</button>"
        tr += "</div>"
        tr += "</td>"
        tr += "</tr>"
      });
      tr += "<tr>"
      tr += "<td colspan='5'>"
      tr += "<button class='btn btn-success pull-right addRawatJalan' data-titimangsa='" + titimangsa + "' data-idjadwal='" + idjadwal + "'>Tambah Rawat Jalan</button>"
      tr += "</td>"
      tr += "</tr>"

      // addRawatJalan
      $("table#antrian tbody").html(tr);
    },
    fail: function (response) {
      $("#divError").show();
      li = ""
      dr = response["responseJSON"]
      for (prop in dr) {
        li += "<li>" + prop + " => " + dr[prop] + "</li>";
      }
      $("ul#ermsg").html(li);
    }
  });





});

// make looping for display calendar
Date.prototype.addDays = function (days) {
  var date = new Date(this.valueOf());
  date.setDate(date.getDate() + days);
  return date;
}

function getDates(startDate, stopDate) {
  var dateArray = new Array();
  var currentDate = startDate;
  while (currentDate <= stopDate) {
    dateArray.push(new Date(currentDate));
    currentDate = currentDate.addDays(1);
  }
  return dateArray;
}

usedTitimangsa = ""
usedidjadwal = ""


// Checkin Dokter
function CheckinDokter(dokter) {
  console.log(dokter);
}


// save pendaftaran
$(document).on("click", "#registerRawatJalan", function (e) {
  e.preventDefault()
  var form = new FormData();
  form.append("tgl_kunjungan", $("input[name=tgl_kunjungan]").val());
  form.append("id_jadwal", $("input[name=id_jadwal]").val());
  form.append("gejala", $("textarea[name=gejala]").val());
  form.append("jam_kunjungan", $("input[name=jam_kunjungan]").val());
  form.append("id_poli", $("input[name=id_poli]").val());
  form.append("id_faskes", $("input[name=id_faskes]").val());

  $.ajax({
    url: "http://localhost:8000/pasien/rawatjalan/list/",
    method: "POST",
    timeout: 0,
    dataType: "JSON",
    "headers": {
      "Authorization": "Bearer " + TOKEN,
    },
    processData: false,
    mimeType: "multipart/form-data",
    contentType: false,
    data: form,
    success: function (response) {
      $("#mdldetailJadwal").modal("hide");
      adm = response["admissiondata"]
      antrian = response["antriandata"]
      $("#idRawatJalan").html(adm["admission_rawat_jalan_id"])
      $("#dokter").html(adm["namadokter"])
      $("#waktukunjungan").html(adm["tgl_kunjungan"], adm["jam_kunjungan"])
      $("#namafaskes").html(adm["faskes"])
      $("#namapoli").html(adm["poli"])
      $("#gejalaResult").html(adm["gejala"])
      $("#noantrian").html(antrian["nomerantrian"])
      loadDataDokter(aktifPoli, baseDate)
    },
  });
});

// tambah data rawatjalan
$(document).on("click", ".addRawatJalan", function (e) {
  var titimangsa = $(this).data("titimangsa");
  var idjadwal = $(this).data("idjadwal");
  $("#inpt_id_jadwal").val(idjadwal);
  $("#inpt_titimangsa").val(titimangsa);
  $("#mdlDetailRawatJalan").modal("hide");
  $("#addRawatJalan").modal("show");
  $("#addRawatJalan").modal("show");
});

$("#FrmAddRawatJalan").submit(function (e) {
  e.preventDefault();
  console.log($(this).serialize());
  $.ajax({
    type: "POST",
    url: BASE_URL_GLOBAL + "/frontdesk/rawatjalan/otomatis/",
    data: $(this).serialize(),
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN,
    },
    success: function (response) {
      alert("Berhasil");
      loadDataDokter(aktifPoli, baseDate);
    },
    fail: function (response) {
      console.log(response);
    }
  });
});

// pasien checkin
$(document).on("click", ".BtnCheckinPasien", function (e) {
  $.ajax({
    type: "GET",
    url: BASE_URL_GLOBAL + "/frontdesk/checkin/pasien/" + $(this).data("idantrian"),
    dataType: "JSON",
    headers: {
      "Authorization": "Bearer " + TOKEN,
    },
    success: function (response) {
      alert("Pasien Checkin")
    }
  });
})