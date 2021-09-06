console.log(objprofile);

function GetListFaskes(kota) {
  kota = $("#inptkota").val();
  if (kota == "") {
    kota = "all"
  }
  $.ajax({
    type: "GET",
    url: "http://localhost:8000/global/faskes/" + kota,
    dataType: "JSON",
    success: function (response) {
      row = "";
      index = 1
      response.data.forEach((v, i) => {
        row += "<tr>"
        row += "<td>" + index.toString() + "</td>";
        row += "<td><a href='/pasien/faskes/poli/page?faskes=" + v.id_faskes + "'>" + v.faskes + "</td>";
        row += "<td>" + v.alamat + "</td>";
        row += "<td>" + v.kota + "</td>";
        row += "<td>" + v.status_faskes + "</td>";
        row += "</tr>"
        index++;
      });
      $("#tablefaskes tbody").html(row);
    }
  });
}


$("#inptkota").change(function (e) {
  e.preventDefault();
  GetListFaskes($(this).val());
});

GetListFaskes("all")