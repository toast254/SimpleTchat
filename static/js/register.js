
var submitButton = document.getElementById("submit_button");

function onError () {
    submitButton.classList.remove("is-loading");
    submitButton.removeAttribute("disabled");
}

function onSuccess () {
    if (this.status == 201) {
        window.location.replace("/room");
    }
    else {
        onError();
    }
}

function register(oFormElement) {
    submitButton.classList.add("is-loading");
    submitButton.setAttribute("disabled", "disabled");
    //
    var oReq = new XMLHttpRequest();
    oReq.onload = onSuccess;
    oReq.onerror = onError;
    //oReq.upload.addEventListener("load", onSuccess);
    //oReq.upload.addEventListener("error", onError);
    //
    oReq.open("post", oFormElement.action);
    oReq.send(new FormData(oFormElement));
}
