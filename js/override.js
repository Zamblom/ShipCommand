var current_room = "cockpit";

function set_room_information(room) {
    let is_preview = true;

    switch (room) {
        case undefined:
            room = current_room;
        case current_room:
            is_preview = false;
            break;
    }

    document.getElementById("room_name").innerHTML = rooms[room].name;
    if (is_preview) {document.getElementById("room_name").innerHTML += ": Preview";}

    document.getElementById("room_description").innerHTML = rooms[room].description;

    let room_abilities = ""
    for (var i = 0; i < rooms[room].abilities.length; i++) {
        let room_ability = abilities[rooms[room].abilities[i]];
        room_abilities += "<div class='room_ability";

        // If the ability is active, set a class to reflect that
        if (room_ability.enabled) {room_abilities += " active";}

        room_abilities += "'";

        // If the ability is active and this isn't a preview, set the relevant onclick event
        if (room_ability.enabled && !is_preview) {room_abilities += " onclick=\"" + room_ability.action + "\"";}

        room_abilities += ">" + room_ability.name + "</div>";
    }
    document.getElementById("room_abilities").innerHTML = room_abilities;

    shown_room = room;
}

function move_to_room(room) {
    const request = new XMLHttpRequest();
    request.open("GET", "/api/move_to_room?room=" + room);
    request.send();
    request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status == 200) {
            set_state();
        }
    }
}

function use_ability(ability) {
    const request = new XMLHttpRequest();
    request.open("GET", "/api/use_ability?ability=" + ability)
    request.send();
    request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status == 200) {
            set_state();
        }
    }
}

function get_current_player() {
    let cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("player=")) {
            return cookies[i].split("player=")[1];
        }
    }
}

function set_player_statistics(player, event) {
    if (event !== undefined) {
        event.stopPropagation();
    }

    const stat_request = new XMLHttpRequest();
    if (player === undefined) {
        stat_request.open("GET", "/api/player_statistics");
    } else {
        stat_request.open("GET", "/api/player_statistics?player=" + player)
    }
    stat_request.send();
    stat_request.onreadystatechange = () => {
        if (stat_request.readyState == 4 && stat_request.status == 200) {
            let response = stat_request.responseText.split(";");
            response.forEach((stat) => {
                document.getElementById(stat.split(":")[0]).innerHTML = stat.split(":")[1];
            });
        }
    }

    const name_request = new XMLHttpRequest();
    if (player === undefined) {
        name_request.open("GET", "/api/player_name");
    } else {
        name_request.open("GET", "/api/player_name?player=" + player)
    }
    name_request.send();
    name_request.onreadystatechange = () => {
        if (name_request.readyState == 4 && name_request.status == 200) {
            document.getElementById("player_name").innerHTML = name_request.responseText;
            if (player != undefined && player != get_current_player()) {
                document.getElementById("player_name").innerHTML += ": Preview";
            }
        }
    }

    let abilities = document.getElementsByClassName("abilities")[0].children;
    let saves = document.getElementsByClassName("saves")[0].children;
    let skills = document.getElementsByClassName("skills")[0].children;

    if (player === undefined || player == get_current_player()) {
        document.getElementById("revert_player").hidden = true;
    } else {
        document.getElementById("revert_player").hidden = false;
    }
}

function set_conditions() {
    let ship_conditions_element = document.getElementById("ship_conditions");
    let new_ship_conditions_element_innerHTML = "";

    for (condition_name in conditions) {
        let condition = conditions[condition_name];

        if (condition.active) {
            new_ship_conditions_element_innerHTML += condition.name + "<br>";
        }
    }
    ship_conditions_element.innerHTML = new_ship_conditions_element_innerHTML;
}

function set_resources() {
    let ship_resources_element = document.getElementById("ship_resources");
    let new_ship_resources_element_innerHTML = "";

    let resource_name_width = 20;

    for (resource_name in resources) {
        let resource = resources[resource_name];
        let resource_block_width = (100 - resource_name_width) / resource.max_amount;
        new_ship_resources_element_innerHTML += "<table width='100vw'><colgroup><col width='" + resource_name_width + "vw'>"
        for (let i = 0; i < resource.max_amount; i++) {
            new_ship_resources_element_innerHTML += "<col width='" + resource_block_width + "vw'>";
        }
        new_ship_resources_element_innerHTML += "</colgroup><tbody><tr><td>" + resource.name + "</td>";
        for (let i = 0; i < resource.amount; i++) {
            new_ship_resources_element_innerHTML += "<td style='background-color: " + resource.color + "'></td>";
        }
        for (let i = 0; i < resource.max_amount - resource.amount; i++) {
            new_ship_resources_element_innerHTML += "<td></td>";
        }
        new_ship_resources_element_innerHTML += "</tbody></table>";
    }
    ship_resources_element.innerHTML = new_ship_resources_element_innerHTML;
}



function set_state() {
    const request = new XMLHttpRequest();
    request.open("GET", "/api/state");
    request.send();
    request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status == 200) {
            const response = request.responseText.split("\n");

            let update_shown_deck = false;
            let update_shown_room = false;
            let update_conditions = false;
            let update_resources = false;

            handleNewPlayerLocations(response[0].split(";"));

            handleNewAbilityStates(response[1].split(";"));

            let new_conditions = response[2].split(";");
            new_conditions.forEach((condition) => {
                let condition_name = condition.split(":")[0];
                let condition_active = (condition.split(":")[1] === "true");

                update_conditions ||= (conditions[condition_name].active !== condition_active);

                conditions[condition_name].active = condition_active;
            });

            let new_resources = response[3].split(";");
            new_resources.forEach((resource) => {
                let resource_name = resource.split(":")[0];
                let resource_amount = parseInt(resource.split(":")[1].split("/")[0]);
                let resource_max_amount = parseInt(resource.split(":")[1].split("/")[1]);

                let resource_amount_has_changed = resources[resource_name].amount !== resource_amount;
                let resource_max_amount_has_changed = resources[resource_name].max_amount !== resource_max_amount;
                update_resources ||= resource_amount_has_changed || resource_max_amount_has_changed;

                resources[resource_name].amount = resource_amount;
                resources[resource_name].max_amount = resource_max_amount;
            });

            if (update_shown_deck) {show_deck(rooms[current_room].deck);}
            if (update_shown_room) {set_room_information(current_room);}
            if (update_conditions) {set_conditions();}
            if (update_resources) {set_resources();}
        }
    }
}

document.onkeypress = function (e) {
    e = e || window.event;
    if (e.keyCode >= 49 && e.keyCode <= 57) {
        ability_element = document.getElementsByClassName("room_ability")[e.keyCode - 49];
        if (ability_element != undefined) {ability_element.click();}
    }
};

window.onload = function() {
    set_state();
    set_room_information("cockpit");
    setInterval(set_state, 1000);
}
