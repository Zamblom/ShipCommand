var time = "0001.01.01-00:00:00.000000"

function handleUpdate(request, caller) {
    switch (request.readyState) {
        case XMLHttpRequest.DONE:
            switch (request.status) {
                case 200:
                    const response = JSON.parse(request.responseText);

                    if ("playerData" in response) {
                        handlePlayerData(response.playerData);
                        return;
                    }

                    time = response.time;
                    const data = response.data;

                    if ("abilities" in data) {handleAbilities(data.abilities)}
                    if ("conditions" in data) {handleConditions(data.conditions)}
                    if ("decks" in data) {handleDecks(data.decks)}
                    if ("resources" in data) {handleResources(data.resources)}

                    break;
                default:
                    console.log("FAILED: " + caller + " - " + request.status);
                    break;
            }
            break;
    }
}

function handleAbilities(newAbilities) {
    for (ability in newAbilities) {
        if (!(ability in abilities)) {abilities[ability] = {}}
        let valueChanged = false;
        for (stat in newAbilities[ability]) {
            valueChanged ||= (abilities[ability][stat] !== newAbilities[ability][stat]);
            abilities[ability][stat] = newAbilities[ability][stat];
        }
        if (shownRoom !== undefined && shownRoom.abilities.includes(ability) && valueChanged) {shownRoom.loadInfo();}
    }
}

function handleConditions(conditionsData) {
    for (condition in conditionsData) {
        const conditionData = conditionsData[condition];
        if (!(condition in conditions)) {conditions[condition] = {}}
        for (conditionAttribute in conditionData) {
            const conditionAttributeData = conditionData[conditionAttribute];
            conditions[condition][conditionAttribute] = conditionAttributeData;
        }
    }
    setConditions();
}

function handleDecks(decksData) {
    for (deck in decksData) {
        const deckData = decksData[deck];
        let deckElement = document.getElementById(deck);
        if (deckElement === null) {
            deckElement = document.getElementById("map").appendChild(document.createElement("ship-deck"));
            deckElement.id = deck;
            deckElement.hidden = true;
        }
        let newCurrentRoom = false;
        for (deckAttribute in deckData) {
            const deckAttributeData = deckData[deckAttribute];
            switch (deckAttribute) {
                case "rooms":
                    for (room in deckAttributeData) {
                        const roomData = deckAttributeData[room];
                        let roomElement = document.getElementById(room);
                        if (roomElement === null) {
                            roomElement = deckElement.appendChild(document.createElement("ship-room"));
                            roomElement.id = room;
                        }
                        for (roomAttribute in roomData) {
                            const roomAttributeData = roomData[roomAttribute];
                            switch (roomAttribute) {
                                case "players":
                                    if (roomAttributeData.includes(currentPlayer())) {
                                        currentRoom = roomElement;
                                        newCurrentRoom = true;
                                    }
                                    roomElement.addPlayers(roomAttributeData);
                                    break;
                                case "isLink":
                                    (roomAttributeData) ? (roomElement.classList.add("link")) : (roomElement.classList.remove("link"))
                                    break;
                                case "clip-path":
                                    roomElement.style.clipPath = roomAttributeData;
                                    break;
                                default:
                                    roomElement[roomAttribute] = roomAttributeData;
                                    break;
                            }
                        }
                    }
                    break;
                default:
                    deckElement.setAttribute(deckAttribute, deckAttributeData);
                    break;
            }
        }
        if (newCurrentRoom) {
            [...document.getElementsByClassName("currentRoom")].forEach((i) => {i.classList.remove("currentRoom")});
            currentRoom.classList.add("currentRoom");
            currentRoom.deck.select();
            currentRoom.loadInfo();
        }
        [...document.getElementsByClassName("available")].forEach((i) => {i.classList.remove("available")});
        currentRoom.connections.forEach((connection) => {document.getElementById(connection[1]).classList.add("available")});
    }
}

function handleResources(resourcesData) {
    for (resource in resourcesData) {
        const resourceData = resourcesData[resource];
        if (!(resource in resources)) {resources[resource] = {}}
        for (resourceAttribute in resourceData) {
            const resourceAttributeData = resourceData[resourceAttribute];
            resources[resource][resourceAttribute] = resourceAttributeData;
        }
    }
    setResources();
}

function handlePlayerData(newPlayerData) {
    document.getElementById("player-name").innerText = newPlayerData.name;
    document.getElementById("revert-player").hidden = newPlayerData.id === currentPlayer();
    for (i in newPlayerData.stats) {
        statFromName(i).innerText = newPlayerData.stats[i];
    }
}
