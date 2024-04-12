window.onload = function () {
    alert("let's go!");
}

function initKeycloak(func) {
    console.log("loading...");
    keycloak = new Keycloak('keycloak.json');
    console.log("init keycloak");
    keycloak.init({
        onLoad: 'login-required'
    }).then(func);
}

function logAuthState(authenticated) {
    console.log(authenticated ? 'authenticated' : 'not authenticated');
}

function prefill(authenticated) {
    logAuthState(authenticated);
    fill_introspect_info();
}

function get_roles(token_info) {
    var roles = token_info['realm_access']['roles'];

    return roles;
}

function secured_action(event) {
    event.preventDefault();

    fetch("../secured/test", {
        method: 'get',
        headers: new Headers({
            'Authorization': 'Bearer ' + keycloak.token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }),
    })
        .then(x => x.text())
        .then(y => document.getElementById("result").innerHTML = y);
}

function fill_introspect_info() {
    // document.getElementById("token").innerHTML = keycloak.token;
    // document.getElementById("token_input").innerHTML = keycloak.token;
    for (element of document.getElementsByClassName("token")) {
        element.innerHTML = keycloak.token;
    }

    var roles = get_roles(keycloak.tokenParsed);
    document.getElementById("roles_info").innerHTML = roles.join("<br>");

    document.getElementById("logout_button").removeAttribute("disabled");
}

function logout_token(event) {
    event.preventDefault();
    keycloak.logout();
}