var rooms = {
    gunTurretB: {
        name: "Gun Turret B",
        description: "The second of the primary gun turrets.",
        center: {x: 50, y: 50},
        deck: "deckGunTurretB",
        abilities: []
    },
    hatchFromGunTurretB: {
        name: "Hatch to Deck B",
        description: "A hatch leading downward to Deck B.",
        center: {x: 0, y: 0},
        deck: "deckGunTurretB",
        abilities: []
    },
    gunTurretC: {
        name: "Gun Turret C",
        description: "The third of the primary gun turrets.",
        center: {x: 50, y: 50},
        deck: "deckGunTurretC",
        abilities: []
    },
    hatchFromGunTurretC: {
        name: "Hatch to Deck B",
        description: "A hatch leading downward to Deck B.",
        center: {x: 0, y: 0},
        deck: "deckGunTurretC",
        abilities: []
    },
    corridor: {
        name: "Corridor",
        description: "A corridor allowing passage between the main hallway and upper gun bays.",
        center: {x: 36, y: 50},
        deck: "deckB",
        abilities: []
    },
    gunBayB: {
        name: "Gun Bay B",
        description: "A gun bay containing Gun Turret B.",
        center: {x: 0, y: 0},
        deck: "deckB",
        abilities: []
    },
    gunBayC: {
        name: "Gun Bay C",
        description: "A gun bay containing Gun Turret C.",
        center: {x: 0, y: 0},
        deck: "deckB",
        abilities: []
    },
    gunBayD: {
        name: "Gun Bay D",
        description: "A empty gun bay fit for a WMD.",
        center: {x: 59.8, y: 50},
        deck: "deckB",
        abilities: []
    },
    ladderToDeckA: {
        name: "Ladder To Deck A",
        description: "A ladder leading downwards to Deck A.",
        center: {x: 0, y: 0},
        deck: "deckB",
        abilities: []
    },
    sledBay: {
        name: "Sled Bay",
        description: "A room equipped with two sleds, each capable of boarding an enemy ship, provided that they survive the perilous journey to its hull.",
        center: {x: 12, y: 41},
        deck: "deckA",
        abilities: []
    },
    engineersQuarter: {
        name: "Engineer's Quarter",
        description: "Piles of tools lie strewn across several large workbenches.<br><br>Several large sheets of metal stand by the door, ready to be used to patch hull and bulkhead alike.",
        center: {x: 25, y: 21},
        deck: "deckA",
        abilities: []
    },
    cargoHold: {
        name: "Cargo Hold",
        description: "Various crates fill the front left quarter of the ship.<br><br>Inside them: all of the supplies needed for the arduous task that is space travel.",
        center: {x: 48, y: 21},
        deck: "deckA",
        abilities: []
    },
    medBay: {
        name: "Med-Bay",
        description: "Should any crew member sustain a serious injury, the med-bay offers a single room to house all of the various medicines and equipments used to restore them to health.",
        center: {x: 64, y: 37},
        deck: "deckA",
        abilities: []
    },
    cockpit: {
        name: "Cockpit",
        description: "The main command center of the ship.<br><br>All of the tools needed to pilot a modern space-faring vessel can be found here, plugged into consoles and jammed into wall spaces.",
        center: {x: 84, y: 50},
        deck: "deckA",
        abilities: ["evasiveManoeuvres", "enterWarp", "deployFlares"]
    },
    brig: {
        name: "Brig",
        description: "An isolated prison cell.<br><br>Bars built into the walls of the ship acts as hard-points for a wide variety of restraints.",
        center: {x: 69, y: 66},
        deck: "deckA",
        abilities: []
    },
    monitoring: {
        name: "Monitoring",
        description: "A room filled with consoles and tools fit to monitor even the most unusual of criminal scum.",
        center: {x: 56, y: 61},
        deck: "deckA",
        abilities: ["lockBrigCell", "unlockBrigCell"]
    },
    livingArea: {
        name: "Living Area",
        description: "The friendliest room of the ship.<br><br>Harsh metal walls give way to lighter custom paintwork and a couple of tables sit covered in equipment and the odd boardgame.",
        center: {x: 37, y: 68},
        deck: "deckA",
        abilities: []
    },
    messHall: {
        name: "Mess Hall",
        description: "Wall mounted shelves host the assorted collection of crew rations and a lone counter tops acts as the sole place clean enough to prepare food.",
        center: {x: 47, y: 86},
        deck: "deckA",
        abilities: []
    },
    crewQuarters: {
        name: "Crew Quarters",
        description: "Several beds stand near each other, each fitted like tetris pieces into one of the smallest rooms in the ship.<br><br>Only just suitable for sleep, the crew are unlikely to spend any unnecessary time within these walls.",
        center: {x: 25, y: 86},
        deck: "deckA",
        abilities: []
    },
    workshop: {
        name: "Workshop",
        description: "A variety of machine and hand tools clutter shelves and tables.<br><br>For any craft that can't be achieved by hand, this room is the first place to look.",
        center: {x: 12, y: 59},
        deck: "deckA",
        abilities: []
    },
    hallway: {
        name: "Hallway",
        description: "A single hallway linking together almost all of the ships major rooms.",
        center: {x: 53, y: 50},
        deck: "deckA",
        abilities: []
    },
    security: {
        name: "Security",
        description: "A hardened security room sits firmly in between the cockpit and the rest of the ship.<br><br>In the event of intrusion, two large doors form an impassible barrier to protect the pilot and crew.",
        center: {x: 69, y: 50},
        deck: "deckA",
        abilities: []
    },
    ladderToDeckB: {
        name: "Ladder To Deck B",
        description: "A ladder leading upwards to Deck B.",
        center: {x: 0, y: 0},
        deck: "deckA",
        abilities: []
    },
    hatchToGunTurretA: {
        name: "Hatch To Gun Turret A",
        description: "A hatch leading downwards to Gun Turret A and the main airlock.",
        center: {x: 0, y: 0},
        deck: "deckA",
        abilities: []
    },
    hatchToSledA: {
        name: "Hatch To Sled A",
        description: "A hatch leading outwards to Sled A.",
        center: {x: 0, y: 0},
        deck: "deckA",
        abilities: []
    },
    hatchToSledB: {
        name: "Hatch To Sled B",
        description: "A hatch leading outwards to Sled B.",
        center: {x: 0, y: 0},
        deck: "deckA",
        abilities: []
    }
}

var abilities = {
    evasiveManoeuvres: {
        name: "Evasive Manoeuvres [R]",
        action: "useAbility('evasiveManoeuvres');",
        enabled: false
    },
    deployFlares: {
        name: "Deploy Flares [R]",
        action: "useAbility('deployFlares');",
        enabled: false
    },
    enterWarp: {
        name: "Enter Warp [A]",
        action: "useAbility('enterWarp');",
        enabled: false
    },
    lockBrigCell: {
        name: "Lock Brig Cell [A]",
        action: "useAbility('lockBrigCell');",
        enabled: false
    },
    unlockBrigCell: {
        name: "Unlock Brig Cell [A]",
        action: "useAbility('unlockBrigCell');",
        enabled: false
    }
}

var conditions = {
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
    if (event != undefined) {event.stopPropagation();}
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {handleUpdate(request, "Set Player Statistics");};
    request.open("GET", "/api/player_statistics" + ((player != undefined) ? ("?player=" + player) : ("")));
    request.send();
}

function setState() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {handleUpdate(request, "Set State")};
    request.open("GET", "/api/state");
    request.send();    
}
