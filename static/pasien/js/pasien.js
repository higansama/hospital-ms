BASE_URL = "/pasien/"


function ajaxsetting(url, data) {
    // data json yang sudah di stringify
    var AJAX_SETTING = {
        "url": "localhost:8000/pasien/" + url,
        "method": "GET",
        "timeout": 0,
        "headers": {
            "Authorization": "Bearer " + TOKEN,
        },
        "contentType": "application/json",
        "data": data
    }

    return AJAX_SETTING;
}

function logout() {
    localStorage.removeItem("token");
    window.location.replace("/pasien/login");
}

function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

TOKEN = localStorage.getItem("token");
objprofile = parseJwt(TOKEN)

function LoadProfile() {
    tokenobject = parseJwt(TOKEN);
    $("img#fotoprofile").before($("img#fotoprofile").attr("src", tokenobject['foto']));
    $("span#usernamebase").text(tokenobject["username"]);
    latestPoint = 0
}


function GetProvinsi() { 
    $.ajax({
        type: "GET",
        url: "http://localhost:8000/global/provinsi",
        dataType: "JSON",
        success: function (response) {
            console.log(response);
        }
    });
 }