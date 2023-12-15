function handleUpdate(request, caller) {
    switch (request.readyState) {
        case XMLHttpRequest.DONE:
            switch (request.status) {
                case 200:
                    const response = JSON.parse(request.responseText);                
                    if ("roomsWithPlayers" in response) {handleNewPlayerLocations(response.roomsWithPlayers);}
                    if ("currentRoom" in response) {handleNewRoom(response.currentRoom);}
                    if ("connections" in response) {handleNewConnections(response.connections);}
                    if ("abilities" in response) {handleNewAbilities(response.abilities);}
                    if ("conditions" in response) {handleNewConditions(response.conditions);}
                    if ("resources" in response) {handleNewResources(response.resources);}
                    if ("playerData" in response) {handleNewPlayerData(response.playerData);}
                    break;
                default:
                    console.log("FAILED: " + caller + " - " + request.status);
            }
            break;
    }
}

function handleNewPlayerLocations(newPlayerLocations) {
    for (i in newPlayerLocations) {
        for (j in newPlayerLocations[i]) {
            document.getElementById(toKebabCase(i)).addPlayer(newPlayerLocations[i][j]);
        }
    }
}

function handleNewRoom(newCurrentRoomId) {
    const oldCurrentRoom = currentRoom;
    const newCurrentRoom = document.getElementById(newCurrentRoomId);
    if (currentRoom != newCurrentRoom) {
        currentRoom.classList.remove("current");
        newCurrentRoom.classList.add("current");
        newCurrentRoom.addPlayer(currentPlayer());
        newCurrentRoom.deck.select()
        currentRoom = newCurrentRoom;
    }
    if (oldCurrentRoom != currentRoom) {currentRoom.loadInfo();}
}

function handleNewConnections(newConnections) {
    for (i in rooms) {
        if (newConnections.includes(i)) {
            document.getElementById(i).classList.add("available");
        } else {
            document.getElementById(i).classList.remove("available");
        }
    }
}

function handleNewAbilities(newAbilities) {
    for (i in newAbilities) {
        const valueChanged = abilities[i].enabled != newAbilities[i].enabled;
        abilities[i].enabled = newAbilities[i].enabled;
        if (shownRoom.abilities.includes(i) && valueChanged) {shownRoom.loadInfo();}
    }
}

function handleNewConditions(newConditions) {
    for (i in newConditions) {
        conditions[i].active = newConditions[i].active;
    } 
    setConditions();
}

function handleNewResources(newResources) {
    for (i in newResources) {
        resources[i].amount = newResources[i].amount;
        resources[i].maxAmount = newResources[i].maxAmount;
    }
    setResources();
}

function handleNewPlayerData(newPlayerData) {
    document.getElementById("player-name").innerText = newPlayerData.name;
    document.getElementById("revert-player").hidden = newPlayerData.id == currentPlayer();
    for (i in newPlayerData.stats) {
        statFromName(i).innerText = newPlayerData.stats[i];
    }
}
