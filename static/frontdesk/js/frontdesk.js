TOKEN = localStorage.getItem("token");
BASE_URL = window.location.origin;

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


function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

objToken = parseJwt(TOKEN)
$("span#username").text(objToken["nama"])

