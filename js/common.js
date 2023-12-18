var abilities = {}

var conditions = {
    brigLocked: {
        name: "Brig Locked",
        active: false
    },
    evasive: {
        name: "Evasive",
        active: false
    },
    heatSeeking: {
        name: "Heat Seeking",
        active: false
    },
    targetLocked: {
        name: "Target-Locked",
        active: false
    }
}

var resources = {
    fuel: {
        name: "Fuel",
        color: "#FB1",
        amount: 0,
        maxAmount: 0
    },
    flares: {
        name: "Flares",
        color: "#F00",
        amount: 0,
        maxAmount: 0
    }
}

function setConditions() {
    const shipConditionsElement = document.getElementById("ship-conditions");
    let newShipConditionsElementInnerHTML = "";

    for (i in conditions) {
        const condition = conditions[i];
        newShipConditionsElementInnerHTML += (condition.active) ? (condition.name + "<br>") : ("");
    }
    shipConditionsElement.innerHTML = newShipConditionsElementInnerHTML;   
}

function setResources() {
    const shipResourcesElement = document.getElementById("ship-resources");
    let newShipResourcesElementInnerHTML = "";

    let resourceNameWidth = 20;

    for (i in resources) {
        const resource = resources[i];
        const resourceBlockWidth = (100 - resourceNameWidth) / resource.maxAmount;
        newShipResourcesElementInnerHTML += "<table width='100vw'><colgroup><col width='" + resourceNameWidth + "vw'>"
        for (let j = 0; j < resource.maxAmount; j++) {
            newShipResourcesElementInnerHTML += "<col width='" + resourceBlockWidth + "vw'>";
        }
        newShipResourcesElementInnerHTML += "</colgroup><tbody><tr><td>" + resource.name + "</td>";
        for (let j = 0; j < resource.amount; j++) {
            newShipResourcesElementInnerHTML += "<td style='background-color: " + resource.color + "'></td>";
        }
        for (let j = 0; j < resource.maxAmount - resource.amount; j++) {
            newShipResourcesElementInnerHTML += "<td></td>";
        }
        newShipResourcesElementInnerHTML += "</tbody></table>";
    }
    shipResourcesElement.innerHTML = newShipResourcesElementInnerHTML;
}

function setPlayerStatistics(player, event) {
    if (event !== undefined) {event.stopPropagation();}
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {handleUpdate(request, "Set Player Statistics");};
    request.open("GET", "/api/player_statistics" + ((player !== undefined) ? ("?player=" + player) : ("")));
    request.send();
}

function setState() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {handleUpdate(request, "Set State")};
    request.open("GET", "/api/state?time=" + time);
    request.send();
}
