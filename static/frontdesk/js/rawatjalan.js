$("#jadwaljam").hide();
$("input#namafaskes").attr("value", objToken["nama_faskes"]);
$("input#namafaskes").data("id_faskes", objToken["id_faskes"]);

$.ajax({
	type: "GET",
	url: BASE_URL + "/global/poli/" + objToken["id_faskes"].toString(),
	dataType: "JSON",
	success: function (response) {
		response.data.forEach((v, i) => {
			$("#listpoli").append(`<option value="${v.id}">${v.poli}</option>`);
		});
	}
});

$("div#fkeluarga").hide();
$("input#berobatchkd").change(function () {
	$("div#fkeluarga").toggle();
});

function Distinct(listData){
	result = []
	listData.forEach((v,i) =>{
		isExist = false
		if (result.length == 0){
			result.push(v)
		} else {
			result.forEach((w, j) => {
				if (w.no_reg_dokter == v.no_reg_dokter) {
					isExist = true
				}
			});
		}
		if (isExist){
			result.push(v)
		}
		
	});
	return result
}

$("#listpoli").change(function (e) { 
	idpoli = $("select#listpoli").val();
	hariini = HARIBAHASA;
	e.preventDefault();
	$.ajax({
		type: "GET",
		url: "/pasien/list/jadwal/dokter/"+ idpoli+"/all/",
		dataType: "JSON",
		headers: {
			"Authorization": "Bearer " + TOKEN
		},	
		success: function (response) {
			cleanData = Distinct(response.data)
			response.data.forEach((v, i) => {
				let o = new Option(v.namadokter, v.id_dokter)
				$("#listdokter").append(o);
			});
		}
	});
});

$("#listdokter").change(function (e) { 
	e.preventDefault();
	iddokter = $("#listdokter").val()
	$.ajax({
		type: "GET",
		url: "/pasien/list/jadwal/dokter/byid/" + iddokter,
		dataType: "JSON",
		headers: {
			"Authorization": "Bearer " + TOKEN
		},	
		success: function (response) {
			$("#jadwaljam").show();
			row = "";
			response.data.forEach((v, i) => {
				$("#cbjadwal").html("");
				row += "<div class='form-check'>"
				row += "<input class='form-check-input' type='radio' name='jadwal' value='"+ v.id +"' >"
				row += "<label class='form-check-label'>"
				row += v.jam_mulai + " " + v.jam_selesai
				row += "</label>"
				row += "</div>"
				$("#cbjadwal").html(row);
			})
		}
	});
});



$("#registerrawatjalan").submit(function (e) {
	e.preventDefault();
	data = {}
	nama = $("input#nama").val();
	ktp = $("input#ktp").val();
	nohp = $("input#nohp").val();
	email = $("input#email").val();
	namafaskes = $("input#namafaskes").val();
	idpoli = $("select#listpoli").val();

	data = {
		"nama": nama,
		"nohp": nohp,
		"ktp": ktp,
		"email": email,
		"namafaskes": namafaskes,
		"idpoli": idpoli,
		"berobatchkd": true,
	}

	knama = $("input#knama").val();
	ktempatlahir = $("input#ktempatlahir").val();
	ktgllahir = $("input#ktgllahir").val();
	khubungan = $("input#khubungan").val();
	if ($("input#berobatchkd") != "checked") {
		data["knama"] = knama
		data["ktempatlahir"] = ktempatlahir
		data["ktgllahir"] = ktgllahir
		data["khubungan"] = khubungan
		berobatchkd["berobatchkd"] = false
	}


	$.ajax({
		type: "POST",
		url: BASE_URL + "/frontdesk/rawatjalan/otomatis/",
		data: data,
		dataType: "JSON",
		headers: {
			// "Content-Type": "application/x-www-form-urlencoded",
			"Authorization": "Bearer " + TOKEN
		},
		success: function (response) {
			console.log(response);
		}
	});

});