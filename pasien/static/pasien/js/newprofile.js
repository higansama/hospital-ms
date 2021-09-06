TOKEN = localStorage.getItem("token")
$("#successMsg").show();
$("#failMsg").hide();

function LoadProfile(params) {
    $.ajax({
        type: "GET",
        url: BASE_URL_PASIEN + "/account/detail/",
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            v = response;
            $("input#nama_provinsi_utama").val(v.nama_provinsi_utama)
            $("input#nama_kota_utama").val(v.nama_kota_utama)
            $("input#nama_kecamatan_utama").val(v.nama_kecamatan_utama)
            $("input#nama_kelurahan_utama").val(v.nama_kelurahan_utama)
            $("input#nama_provinsi_domisili").val(v.nama_provinsi_domisili)
            $("input#nama_kota_domisili").val(v.nama_kota_domisili)
            $("input#nama_kecamatan_domisili").val(v.nama_kecamatan_domisili)
            $("input#nama_kelurahan_domisili").val(v.nama_kelurahan_domisili)
            $("input#username").val(v.username)
            $("input#email").val(v.email)
            $("input#no_telepon").val(v.no_telepon)
            $("input#no_ponsel").val(v.no_ponsel)
            $("input#tingkat_pendidikan").val(v.tingkat_pendidikan)
            $("input#kodepos_utama").val(v.kodepos_utama)
            $("input#kodepos_domisili").val(v.kodepos_domisili)
            $("input#alamat_utama").val(v.alamat_utama)
            $("input#alamat_domisili").val(v.alamat_domisili)
            $("input#tempat_lahir").val(v.tempat_lahir)
            $("input#tgl_lahir").val(v.tgl_lahir)
            $("input#jenis_kelamin").val(v.jenis_kelamin)
            $("input#no_asuransi").val(v.no_asuransi)
            $("input#foto_identitas").val(v.foto_identitas)
            $("input#nama").val(v.nama)
            $("input#no_reg_member").val(v.no_reg_member)
            $("input#profesi").val(v.profesi)
            $("input#no_ktp").val(v.no_ktp)
            $("input#kelurahan_utama").val(v.kelurahan_utama)
            $("input#kecamatan_utama").val(v.kecamatan_utama)
            $("input#kota_utama").val(v.kota_utama)
            $("input#provinsi_utama").val(v.provinsi_utama)
            $("input#kelurahan_domisili").val(v.kelurahan_domisili)
            $("input#kecamatan_domisili").val(v.kecamatan_domisili)
            $("input#kota_domisili").val(v.kota_domisili)
            $("input#provinsi_domisili").val(v.provinsi_domisili)
        }
    });

}

LoadProfile()

function UpdateProfile(e, tipe) {
    formData = JSON.parse(JSON.stringify($("form#frmProfile").serialize()));
    $.ajax({
        type: "PUT",
        url: BASE_URL_PASIEN + "/account/detail/",
        data: formData,
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            switch (tipe) {
                case "personal":
                    $("input.personal").toggleClass("form-control-plaintext form-control")
                    $("input.personal").attr("readonly", false)
                    $("#successMsg").show();
                    $(".bareng").hide();
                    $("#successMsg").html("<h5>Berhasil Update Data Pribadi</h5>")
                    setTimeout(function () { $("#successMsg").hide(); }, 5000);

            }
            LoadProfile();
        },
        error: function (response) {
            switch (tipe) {
                case "personal":
                    LoadProfile();
                    $("input.personal").toggleClass("form-control-plaintext form-control")
                    $("input.personal").attr("readonly", false)
                    $("#simpanPersonal").toggle();
                    $("#personalEdit").toggle();
                    $("#successMsg").show();
                    $("#successMsg").html("<h5>Mohon Maaf Terjadi Kesalahan</h5>")
                    $(".bareng").hide()
                    setTimeout(function () { $("#failMsg").hide(); }, 5000);
            }
        }
    });
}


// data personal flow
$(".bareng").hide();
$("#personalEdit").click(function (e) {
    e.preventDefault();
    $("input.personal").toggleClass("form-control-plaintext form-control")
    $("input.personal").attr("readonly", false)
    $(".bareng").show();
    $(this).hide();
});

$("#simpanPersonal").click(function (e) {
    e.preventDefault();
    $("#personalEdit").show();
    $(".bareng").hide();
    UpdateProfile(e, "personal");
});

$("#cancelPersonal").click(function (e) {
    e.preventDefault();
    $(".bareng").hide();
    $("input.personal").toggleClass("form-control-plaintext form-control")
    $("input.personal").attr("readonly", false)
    $("#personalEdit").show()
});
// data personal flow
// data domisili flow
$("#domisilEdit").click(function (e) {
    e.preventDefault();

    $("#modalAlamat").modal("show");
    dataProvinsi = GetProvinsi();
    $("#listkelurahan").select2({
        ajax: {
            url: 'http://localhost:8000/global/cari/kelurahan/',
            dataType: 'json',
        }
    });
});
// data domisili flow stop

var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
var haris = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
var bulans = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

$("a#gethistorypoint").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: BASE_URL_PASIEN + "/points/all",
        data: "data",
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            console.log(response);
            $("#modalPoints").modal("show");
            $("table#historyPoint tbody").html("")
            row = ""
            $.each(response, function (i, v) {
                var waktu = new Date(v.date_created);
                var dd = waktu.getDate();
                var mm = bulans[waktu.getMonth()];
                var yyyy = waktu.getFullYear();
                pointday = haris[waktu.getDay()] + ", " + dd + ' ' + mm + ' ' + yyyy;

                let point = v.get_point
                if (point == 0) {
                    point = "-" + String(v.minus_point)
                }
                row += "<tr>"
                row += "<td>" + pointday + "</td>"
                row += "<td>" + v.service + "</td>"
                row += "<td>" + point + "</td>"
                row += "<td>" + v.total_point + "</td>"
                row += "</tr>"
            });
            $("table#historyPoint tbody").html(row)
        }
    });
});

$("a.detailrm").click(function (e) {
    id = $(this).data("id");
    e.preventDefault();
    $("#modalDetailRekamMedis").modal('show');
    $.ajax({
        type: "GET",
        url: "/pasien/rekammedis/detail/" + id,
        data: "data",
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            rm = response["rekammedis"];
            adm = response["admission"];
            $("h5#admssionID").html(adm.admission_rawat_jalan_id);
            $("td#dokter").html(adm.namadokter);
            $("td#diagnosa").html(rm.diagnosa);
            $("td#tindakan").html(rm.tindakan_pengobatan);
            $("td#tglAdmision").html(adm.tgl_kunjungan);
            $("td#faskes").html(adm.faskes);
            $("td#poli").html(adm.poli);
            $("td#gejala").html(adm.gejala);

        }
    });
});

// $('#myModal').on('shown.bs.modal', function () {
//   $('#myInput').trigger('focus')
// })

// flow akun edit start
$("#saveAkun").hide();
$("#batalSave").hide();
$("#editAkun").click(function (e) {
    e.preventDefault();
    $(this).toggle();
    $("#saveAkun").toggle();
    $("#batalSave").toggle();
    $("input.account").toggleClass("form-control-plaintext form-control")
    $("input.account").attr("readonly", false)
});

$("#batalSave").click(function (e) {
    e.preventDefault();
    $(this).hide();
    $("#editAkun").toggle();
    $("#saveAkun").toggle();
    $("input.account").toggleClass("form-control-plaintext form-control")
    $("input.account").attr("readonly", true)
});

$("#saveAkun").click(function (e) {
    e.preventDefault();
    formData = JSON.parse(JSON.stringify($("form#frmAkun").serialize()));
    $.ajax({
        type: "PUT",
        url: BASE_URL_PASIEN + "/account/detail/ue",
        data: formData,
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            $("#editAkun").toggle();
            $("#saveAkun").toggle();
            $("input.account").toggleClass("form-control-plaintext form-control")
            $("input.account").attr("readonly", true)
            $("#successMsg").show();
            $("#successMsg").html("<h5>Berhasil Update Data Pribadi</h5>")
            setTimeout(function () { $("#successMsg").hide(); }, 5000);
        },
        error: function (response) {
            $("#successMsg").show();
            $("#successMsg").html("<h5>Mohon Maaf Periksa Kembali Username Dan Email Anda </h5>")
            setTimeout(function () { $("#failMsg").hide(); }, 5000);
        }
    });
})
// flow akun edit stop


// Update password
$("#gantiPassword").click(function (e) {
    e.preventDefault();
    $("#modalUpdatePassword").modal("show")
});
// Update password

// keluarga
function loadDataKeluarga() {
    $.ajax({
        type: "GET",
        url: BASE_URL_PASIEN + "/keluarga",
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            row = ""
            $(".timeline").html("")
            $.each(response, function (i, v) {
                gmbr = "/media/default-profile.jpg"
                row += "<div class='col-lg-12'>"
                row += "<div class='timeline-panel p-4 mb-4'>"
                row += "<div class='media mr-4'>"
                row += "<img src='" + gmbr + "' width='45' src=''>"
                row += "</div>"
                row += "<div class='media-body'>"
                row += "<a href='#'><h4 class='mb-2'>" + v.nama + "</h4></a>"
                row += "<p class='mb-2 text-primary'>" + v.hubungan_keluarga + "</p>"
                row += "</div>"
                row += "</div>"
                row += "</div>"
            });
            $(".timeline").html(row);
        }
    });
}

$("#btnkeluarga").click(function (e) {
    e.preventDefault();
    loadDataKeluarga();
});

$("#btnAddKeluarga").click(function () {
    $("#mdlTambahKeluarga").modal("show");
})
$("#simpanDataKeluarga").click(function (e) {
    e.preventDefault();
    formData = JSON.parse(JSON.stringify($("form#tmbhKeluarga").serialize()));
    $.ajax({
        type: "POST",
        url: BASE_URL_PASIEN + "/keluarga/",
        dataType: "JSON",
        data: formData,
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        success: function (response) {
            $("#mdlTambahKeluarga").modal("hide");
            alert("Keluarga Berhasil Ditambahkan");
            loadDataKeluarga();
        },
        error: function (response) {
            console.log(response);
        }
    });
});

// keluarga
$("#konfpass").hide();
$("#konf_password").keyup(function (e) {
    if ($(this).val() != $("#newpassword").val()) {
        $("#konfpass").show();
    } else {
        $("#konfpass").html("konfirmasi berhasil");
    }
});

$("#btn-updatepassword").click(function (e) {
    e.preventDefault();
    dataPassword = $("form#gantiPassword").serialize();
    $.ajax({
        type: "POST",
        url: BASE_URL_PASIEN + "/update/password/",
        dataType: "JSON",
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        data: dataPassword,
        success: function (response) {
            alert("Berhasil");
            location.reload()
        },
        fail: function (response) {
            alert(response["error"])
        }
    });
});


$("#gantiphoto").click(function () {
    $("#editPoto").modal("show");
});

$("form#updatePoto").submit(function (e) {
    var form = new FormData();
    form.append("foto_identitas", $('#poto')[0].files[0]);

    var settings = {
        "url": BASE_URL_PASIEN + "/account/upload/poto",
        "method": "PUT",
        "timeout": 0,
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": form
    };

    $.ajax(settings).done(function (response) {
        console.log(response);
    });
})