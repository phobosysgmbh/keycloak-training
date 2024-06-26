window.onload = function () {
    alert("let's go!");
}

function initKeycloak(func) {
    keycloak = new Keycloak('keycloak.json');
    console.log("init keycloak");
    keycloak.init({ onLoad: 'check-sso' }).then(func);
}

function logAuthState(authenticated) {
    console.log(authenticated ? 'authenticated' : 'not authenticated');
}

function init_page(authenticated) {
    logAuthState(authenticated);
    fill_introspect_info(authenticated);
    if (authenticated) {
        set_button_states();
    }
}

function get_roles(token_info) {
    var roles = token_info['realm_access']['roles'];

    return roles;
}

function get_headers() {
    return new Headers({
        'Authorization': 'Bearer ' + keycloak.token,
        'Content-Type': 'application/x-www-form-urlencoded'
    });
}

function secured_action_1(event) {
    event.preventDefault();

    fetch("../secured/test", {
        method: 'get',
        headers: get_headers(),
    })
        .then(x => x.text())
        .then(y => document.getElementById("result").innerHTML = y);
}

function secured_action_2(event) {
    event.preventDefault();

    fetch("../secured/test2", {
        method: 'get',
        headers: get_headers(),
    })
        .then(x => x.text())
        .then(y => document.getElementById("result-2").innerHTML = y);
}

function fill_introspect_info(authenticated) {
    if (!authenticated) {
        document.getElementById("token").innerHTML = "not logged in";
        return
    }

    document.getElementById("token").innerHTML = keycloak.token;

    var roles = get_roles(keycloak.tokenParsed);
    document.getElementById("roles_info").innerHTML = roles.join("<br>");
}

function set_button_states() {
    document.getElementById("logout_button").removeAttribute("disabled");
    document.getElementById("manage_account_button").removeAttribute("disabled");
    document.getElementById("login_button").setAttribute("disabled", "");
}

function login_keycloak(event) {
    event.preventDefault();
    keycloak.login();
}

function logout_keycloak(event) {
    event.preventDefault();
    keycloak.logout();
}