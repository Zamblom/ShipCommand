var currentRoom;
var shownRoom;

function useAbility(ability) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {handleUpdate(request, "Use Ability")};
    request.open("GET", "/api/use_ability?ability=" + ability)
    request.send();
}

document.onkeypress = function (e) {
    e = e || window.event;
    if (e.keyCode >= 49 && e.keyCode <= 57) {
        const abilityElement = document.getElementsByClassName("room-ability")[e.keyCode - 49];
        if (abilityElement != undefined) {abilityElement.click();}
    }
};

window.onload = function() {
    currentRoom = document.getElementsByTagName("ship-room")[0];
    setPlayerStatistics();
    setState();
    setInterval(setState, 1000);
}
