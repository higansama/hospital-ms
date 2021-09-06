const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString)
const idfaskes = urlParams.get('faskes')
let LatestDate;

$.ajax({
  type: "GET",
  url: "http://localhost:8000/global/poli/" + idfaskes,
  dataType: "JSON",
  success: function (response) {
    poli = ""
    response.data.forEach((v, i) => {
      namapoli = +"#" + v.poli.toLowerCase().replace(" ", "-")
      if (i == 0) {
        // loadDataDokter(v.id)
        poli += "<a href='" + namapoli + "' data-toggle='pill' class='nav-link active' data-idpoli='" + v.id + "'>" + v.poli + "</a>"
      } else {
        poli += "<a href='" + namapoli + "' data-toggle='pill' class='nav-link' data-idpoli='" + v.id + "'>" + v.poli + "</a>"
      }
    });
    $("#titlePoli").html(poli);
  }
});

// function loadDataDokter(idpoli) {
//   var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
//   var haris = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
//   var bulans = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
//   today = new Date()
//   dd = String(today.getDate()).padStart(2, '0')
//   mm = String(today.getMonth()).padStart(2, '0')
//   YYYY = String(today.getFullYear())
//   hariIni = mm + "/" + dd + "/" + YYYY

//   var dateArray = getDates(new Date(), (new Date()).addDays(6));

//   $.ajax({
//     type: "GET",
//     url: "http://localhost:8000/pasien/list/jadwal/dokter/" + idpoli + "/all",
//     dataType: "JSON",
//     "headers": {
//       "Authorization": "Bearer " + TOKEN,
//     },
//     success: function (response) {
//       dataJadwal = OlahResponJadwal(response.data)
//       console.log(dataJadwal);
//       thead = "";
//       tdjadwal = ""
//       dateArray.forEach(tgl => {
//         thead += "<td>"
//         thead += haris[tgl.getDay()] + ",<br>" + String(tgl.getDate()).padStart(2, '0') + " " + bulans[tgl.getMonth()] + " " + tgl.getFullYear()
//         thead += "</td>"
//         LatestDate = tgl;


//         tglDktr = String(tgl.getDate()).padStart(2, 0)
//         blnDktr = String(tgl.getMonth()).padStart(2, 0)
//         tahunDktr = String(tgl.getFullYear())
//         titimangsa = tahunDktr + "-" + blnDktr + "-" + tglDktr 
//         tdjadwal += "<tr>"
//         dataJadwal.forEach((v, i) => {
//           tdjadwal += "<td>"
//           if (v.hari == tgl.getDay()) {
//             if (v.data.length != 0) {
//               v.data.forEach(el => {
//                 tdjadwal +=  "["+ el.id +"]<a href='' class='detailjadwal' data-idjadwal='" + el.id + "' data-titimangsa='" + titimangsa + "'><p class='text-sm-start'>" + el.namadokter
//                 tdjadwal += "[" + el.jam_mulai + "-" + el.jam_selesai + "]</p></a>"
//               });
//             }
//           } else {
//             tdjadwal += ""
//           }
//           tdjadwal += "</td>"
//         });
//         tdjadwal += "</tr>"

//       });

//       $("table#calendar thead").html(thead)
//       $("table#calendar tbody").html("<tr>" + tdjadwal + "</tr>")
//     }
//   });

//   // clean up table
// }

// function OlahResponJadwal(dataResponse) {
//   datahasil = [
//     { "hari": 0, "data": [] },
//     { "hari": 1, "data": [] },
//     { "hari": 2, "data": [] },
//     { "hari": 3, "data": [] },
//     { "hari": 4, "data": [] },
//     { "hari": 5, "data": [] },
//     { "hari": 6, "data": [] }
//   ]

//   dataResponse.forEach((v, i) => {
//     // console.log(i);
//     if (v.jadwal_praktek == "0") {
//       datahasil[0].data.push(v)
//     } else if (v.jadwal_praktek == "1") {
//       datahasil[1].data.push(v)
//     } else if (v.jadwal_praktek == "2") {
//       datahasil[2].data.push(v)
//     } else if (v.jadwal_praktek == "3") {
//       datahasil[3].data.push(v)
//     } else if (v.jadwal_praktek == "4") {
//       datahasil[4].data.push(v)
//     } else if (v.jadwal_praktek == "5") {
//       datahasil[5].data.push(v)
//     } else {
//       datahasil[6].data.push(v)
//     }
//   });
//   return datahasil
// }


$(document).on("click", "a.nav-link", function () {
  idpoli = $(this).data("idpoli");
  loadDataDokter(idpoli)
});

$(document).on("click", "a.detailjadwal", function (e) {
  e.preventDefault()
  idjadwal = $(this).data("idjadwal");
  titimangsa = $(this).data("titimangsa");
  console.log(idjadwal);
  console.log(titimangsa);

  $.ajax({
    type: "POST",
    url: "http://localhost:8000/pasien/detail/jadwal/dokter",
    dataType: "JSON",
    "headers": {
      "Authorization": "Bearer " + TOKEN,
    },
    "data":{
      "idjadwal": idjadwal,
      "titimangsa": titimangsa,
    },
    success: function (response) {

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
