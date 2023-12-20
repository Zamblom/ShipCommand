var currentRoom;
var shownRoom;

function useAbility(ability) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {handleUpdate(request, "Use Ability")};
    request.open("GET", "/api/use_ability?time=" + time + "&ability=" + ability)
    request.send();
}


document.onkeydown = function (event) {
    const codeToIndex = {
        "Digit1": 0, "Digit2": 1, "Digit3": 2, "Digit4": 3, "Digit5": 4,
        "Digit6": 5, "Digit7": 6, "Digit8": 7, "Digit9": 8, "Digit0": 9,
        "Numpad1": 0, "Numpad2": 1, "Numpad3": 2, "Numpad4": 3, "Numpad5": 4,
        "Numpad6": 5, "Numpad7": 6, "Numpad8": 7, "Numpad9": 8, "Numpad0": 9
    }

    if (event.code in codeToIndex) {
        const abilityElement = document.getElementsByClassName("room-ability")[codeToIndex[event.code]];
        if (abilityElement != null) {abilityElement.click()}
    }
};


window.onload = function() {
    setState();
    setPlayerStatistics();
    setInterval(setState, 2000);
}
