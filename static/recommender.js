//After the user clicks the submit button there will be a loading spinner to indicate that their results are being queried
function loading(){
    document.getElementById("form").style.display = "none";
    document.getElementById("loadSpinner").style.display = "block";
    document.getElementById("info").innerHTML = "Please wait while your recommendations are found!";
}

function getLocation() {
    var userLat = document.getElementById("userLat");
    var userLong = document.getElementById("userLong");

    if (!navigator.geolocation){
        document.getElementById("output").innerHTML = "<p>Geolocation is not supported by your browser</p>";
        return true;
    }

    function success(position) {
        var latitude  = position.coords.latitude;
        var longitude = position.coords.longitude;

        userLat.value = latitude;
        userLong.value = longitude;
    }

    function error() {
        showPostal();
    }

    navigator.geolocation.getCurrentPosition(success, error);
}

function showPostal(){
    document.getElementById("hiddenPost").style.display = "block";
    document.getElementById("submit").disabled = true;
}

function checkPostal() {
    var ca = new RegExp(/([ABCEGHJKLMNPRSTVXY]\d)([ABCEGHJKLMNPRSTVWXYZ]\d){2}/i);

    //Used to do a live check of the postal code
    var postalCode = document.getElementById("postcode").value;

    if (ca.test(postalCode.toString().replace(/\W+/g, ''))) {
        document.getElementById("submit").disabled = false;
        document.getElementById("output").innerHTML = "";
    }
    else{
       document.getElementById("output").innerHTML = "Your postal code must be 6 characters long ex. V3X8V9";
    }
}


function srmColorChanger(value){
   
    var srmValue = value;
    if(srmValue < 2){
        document.getElementById("srmColor").style = "background-color:#ffff45";
        document.getElementById("srmColor").innerHTML = "Pale Straw";
    }
    else if(srmValue == 3){
        document.getElementById("srmColor").style = "background-color:#ffe93e";
        document.getElementById("srmColor").innerHTML = "Straw";
    }
    else if(srmValue > 4 && srmValue <= 6){
        document.getElementById("srmColor").style = "background-color:#fed849";
        document.getElementById("srmColor").innerHTML = "Pale Gold";
    }
    else if(srmValue > 6 && srmValue <= 9){
        document.getElementById("srmColor").style = "background-color:#ffa846";
        document.getElementById("srmColor").innerHTML = "Deep Gold";
    }
    else if(srmValue > 9 && srmValue <= 12){
        document.getElementById("srmColor").style = "background-color:#f49f44";
        document.getElementById("srmColor").innerHTML = "Pale Amber";
    }
    else if(srmValue > 12 && srmValue <= 15){
        document.getElementById("srmColor").style = "background-color:#d77f59";
        document.getElementById("srmColor").innerHTML = "Medium Amber";
    }
    else if(srmValue > 15 && srmValue <= 18){
        document.getElementById("srmColor").style = "background-color:#94523a";
        document.getElementById("srmColor").innerHTML = "Deep Amber";
    }
    else if(srmValue > 18 && srmValue <= 20){
        document.getElementById("srmColor").style = "background-color:#804541";
        document.getElementById("srmColor").innerHTML = "Amber-Brown";
    }
    else if(srmValue > 20 && srmValue <= 24){
        document.getElementById("srmColor").style = "background-color:#5b342f";
        document.getElementById("srmColor").innerHTML = "Brown";
    }
    else if(srmValue > 24 && srmValue <= 30){
        document.getElementById("srmColor").style = "background-color:#4c3b2b";
        document.getElementById("srmColor").innerHTML = "Ruby Brown";
    }
    else if(srmValue > 30 && srmValue <= 40){
        document.getElementById("srmColor").style = "background-color:#38302e";
        document.getElementById("srmColor").innerHTML = "Deep Brown";
    }
    else if(srmValue > 40){
        document.getElementById("srmColor").style = "background-color:#31302c";
        document.getElementById("srmColor").innerHTML = "Black";
    }
}
