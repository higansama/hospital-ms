function loadProfile(){
  $.ajax({
    type: "GET",
    url: "http://localhost:8000/pasien/account/detail/",
    dataType: "JSON",
    "headers": {
      "Authorization": "Bearer " + TOKEN,
    },
    success: function (response) {
      console.log(response);
      $("input[name=no_ktp]").val(response.no_ktp)
      $("input[name=nama]").val(response.nama)
      $("input[name=no_telepon]").val(response.no_telepon)
      $("input[name=profesi]").val(response.profesi)
      $("input[name=tingkat_pendidikan]").val(response.tingkat_pendidikan)
      $("input[name=alamat_utama]").val(response.alamat_utama)
      $("input[name=provinsi_utama]").val(response.provinsi_utama)
      $("input[name=kota_utama]").val(response.kota_utama)
      $("input[name=kecamatan_utama]").val(response.kecamatan_utama)
      $("input[name=kelurahan_utama]").val(response.kelurahan_utama)
      $("input[name=kodepos_utama]").val(response.kodepos_utama)
      $("input[name=provinsi_domisili]").val(response.provinsi_domisili)
      $("input[name=kota_domisili]").val(response.kota_domisili)
      $("input[name=kecamatan_domisili]").val(response.kecamatan_domisili)
      $("input[name=kelurahan_domisili]").val(response.kelurahan_domisili)
      $("input[name=kodepos_domisili]").val(response.kodepos_domisili)
    }
  });
}
loadProfile()