class ShipDeck extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {}

    select() {
        [...document.getElementsByTagName("ship-deck-selector")].filter((i) => {return i.deck == this;})[0].select();
    }
}
customElements.define("ship-deck", ShipDeck);

class ShipRoom extends HTMLElement {
    constructor() {
        super();
        this.players = new Set();
    }

    connectedCallback() {
        this.addEventListener("click", this.moveTo);
        this.addEventListener("mouseover", this.loadInfo);
        this.name = rooms[this.id].name;
        this.description = rooms[this.id].description;
        this.center = rooms[this.id].center;
        this.deck = this.parentElement;
        this.abilities = rooms[this.id].abilities;
    }

    addPlayer(player) {
        [...document.getElementsByTagName(this.tagName)].forEach((i) => {
            i.removePlayer(player);
        });
        this.players.add(player);
        this.renderPlayers();
    }

    removePlayer(player) {
        if (this.players.has(player)) {
            this.players.delete(player);
            this.renderPlayers();
        }
    }

    renderPlayers() {
        this.innerHTML = "";
        const points = [
            [],
            [[0, 0]],
            [[-1, 0], [1, 0]],
            [[-2, 0], [0, 0], [2, 0]],
            [[-1, -1.5], [1, -1.5], [-1, 1.5], [1, 1.5]],
            [[-2, -1.5], [0, -1.5], [2, -1.5], [-1, 1.5], [1, 1.5]],
            [[-2, -1.5], [0, -1.5], [2, -1.5], [-2, 1.5], [0, 1.5], [2, 1.5]]
        ][this.players.size];
        let i = 0;
        this.players.forEach((player) => {
            const point = {x: points[i][0], y: points[i][1]};
            const newPlayer = document.createElement("div");
            newPlayer.id = player;
            newPlayer.classList.add("counter");
            newPlayer.setAttribute("onClick", "javascript: setPlayerStatistics(this.id, event);");
            newPlayer.style.left = (point.x + this.center.x) + "%";
            newPlayer.style.top = (point.y + this.center.y) + "%";
            this.appendChild(newPlayer);
            i++;
        })
    }

    moveTo() {
        const request = new XMLHttpRequest();
        request.onreadystatechange = () => {handleUpdate(request, "Move To Room")};
        request.open("GET", "/api/move_to_room?room=" + this.id);
        request.send();
    }

    loadInfo() {
        document.getElementById("room-name").innerText = this.name + ((this != currentRoom) ? (": Preview") : "");
        document.getElementById("room-description").innerHTML = this.description;
    
        const roomAbilities = document.getElementById("room-abilities");
        roomAbilities.innerHTML = "";
        this.abilities.forEach((i) => {
            const roomAbility = abilities[i];
            const newRoomAbility = document.createElement("div");
            newRoomAbility.classList.add("room-ability");
            if (abilities[i].enabled) {
                newRoomAbility.classList.add("active");
                if (this == currentRoom) {
                    newRoomAbility.setAttribute("onClick", "javascript: " + roomAbility.action);
                }
            }
            newRoomAbility.innerText = roomAbility.name;
            roomAbilities.appendChild(newRoomAbility);
        });
    
        shownRoom = this;
    }
}
customElements.define("ship-room", ShipRoom);

class ShipDeckSelector extends HTMLElement {
    static observedAttributes = ["deck", "size"];

    constructor() {
        super();
    }

    connectedCallback() {
        this.addEventListener("click", this.select);
        this.setStyle();
        this.deselect();
    }

    setStyle() {
        this.style.width = "3vw";
        this.style.height = ((this.size == "small") ? (2) : (3)) + "vw";

        this.style.paddingRight = ((this.size == "small") ? (0.2) : (0.6)) + "vw";

        this.style.backgroundColor = "#DDD";

        this.style.borderWidth = "0.3vw 0.3vw 0.3vw 0vw";
        this.style.borderStyle = "solid";
        this.style.borderRadius = "0 0.5vw 0.5vw 0";

        this.style.fontSize = ((this.size == "small") ? (1) : (1.8)) + "vw";
        this.style.fontWeight = "bold";

        this.style.textAlign = "right";

        this.style.translate = "0, -50%";
    }

    select() {
        [...document.getElementsByTagName(this.tagName)].forEach((i) => {i.deselect();})
        this.style.left = "0%";
        this.style.borderColor = "#6A2";
        this.deck.hidden = false;
    }

    deselect() {
        this.style.left = "-1%";
        this.style.borderColor = "#F50";
        this.deck.hidden = true;
    }

    attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case "deck":
                this.deck = document.getElementById(newValue);
                break;
            case "size":
                this.size = newValue;
        }
    }
}
customElements.define("ship-deck-selector", ShipDeckSelector);