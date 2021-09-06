let BASE_URL_PASIEN = window.location.origin + "/frontdesk";
let BASE_URL_GLOBAL = window.location.origin;
let TOKEN = localStorage.getItem("token")

function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

objToken = parseJwt(TOKEN)
if (objToken["jenis_anggota"] != 4) {
    a
    window.location.replace(BASE_URL_GLOBAL + "/logout/all")
}


var dateObj = new Date()
var DAY_NOW = dateObj.toLocaleString("default", { weekday: "long" })

function hariniconverter(DAY_NOW) {
    if (DAY_NOW == "Monday") {
        return "Senin"
    }
    else if (DAY_NOW == "Tuesday") {
        return "Selasa"
    }
    else if (DAY_NOW == "Wednesday") {
        return "Rabu"
    }
    else if (DAY_NOW == "Thursday") {
        return "Kamis"
    }
    else if (DAY_NOW == "Friday") {
        return "Jumat"
    }
    else if (DAY_NOW == "Saturday") {
        return "Sabtu"
    }
    else (DAY_NOW == "Sunday")
    {
        return "Minggu"
    }
}

var HARIBAHASA = hariniconverter(DAY_NOW)


function LoadFaskes() {
    var result = ""
    $.ajax({
        type: "GET",
        url: BASE_URL_GLOBAL + "/global/faskes/all",
        dataType: "JSON",
        success: function (response) {
            let opt = ""
            response.data.forEach((v, i) => {
                opt += "<option value='" + v.id_faskes + "'>" + v.faskes + "</option>"
            });
            localStorage.setItem('listFaskes', opt)
        }
    });
}

function GetProvinsi(obj) {
    $.ajax({
        type: "GET",
        url: BASE_URL + "/global/provinsi",
        dataType: "json",
        success: function (response) {
            obj.html("");
            var opt = "";
            $.each(response, function (i, v) {
                opt += "<option value='" + v.id_provinsi + "'>" + v.provinsi + "</option>"
            });
            obj.html(opt);
        }
    });
}


function LoadKota(objList, idprovinsi) {
    console.log("terpanggil loadkota");
    $.ajax({
        type: "GET",
        url: BASE_URL + "/global/kota?idprovinsi="+idprovinsi,
        dataType: "json",
        success: function (response) {
            objList.html("");
            var opt = "";
            $.each(response, function (i, v) {
                opt += "<option value='" + v.id_kota + "'>" + v.kota + "</option>"
            });
            objList.html(opt);
        }
    });
}

function LoadKecamatan(objList, idkota) {
    console.log("terpanggil LoadKecamatan");
    $.ajax({
        type: "GET",
        url: BASE_URL + "/global/kecamatan?idkota="+idkota,
        dataType: "json",
        success: function (response) {
            objList.html("");
            var opt = "";
            $.each(response, function (i, v) {
                opt += "<option value='" + v.id_kecamatan + "'>" + v.kecamatan + "</option>"
            });
            objList.html(opt);
        }
    });
}


function LoadKelurahan(objList, idkecamatan) {
    $.ajax({
        type: "GET",
        url: BASE_URL + "/global/kelurahan?idkecamatan="+idkecamatan,
        dataType: "json",
        success: function (response) {
            objList.html("");
            var opt = "";
            $.each(response, function (i, v) {
                opt += "<option value='" + v.id_kelurahan + "'>" + v.kelurahan + "</option>"
            });
            objList.html(opt);
        }
    });
}



function LoadPoli(objList) {
    $.ajax({
        type: "GET",
        url: BASE_URL_GLOBAL + "/global/poli/" + objToken["id_faskes"].toString(),
        dataType: "JSON",
        success: function (response) {
            response.data.forEach((v, i) => {
                $("objList").append(`<option value="${v.id}">${v.poli}</option>`);
            });
        }
    });
}



function LoadDivisi(objList){
        $.ajax({
            type: "GET",
            url: BASE_URL + "/global/kelurahan?idkecamatan="+idkecamatan,
            dataType: "json",
            success: function (response) {
                objList.html("");
                var opt = "";
                $.each(response, function (i, v) {
                    opt += "<option value='" + v.id_kelurahan + "'>" + v.kelurahan + "</option>"
                });
                objList.html(opt);
            }
        });
}