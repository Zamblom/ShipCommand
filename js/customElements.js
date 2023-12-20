class ShipDeck extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {}

    select() {
        [...document.getElementsByTagName("ship-deck-selector")].filter((i) => {return i.deck === this.id})[0].select();
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
        this.deck = this.parentElement;
    }

    addPlayers(players) {
        players.forEach((player) => {
            if (this.players.has(player)) {return}
            [...document.getElementsByTagName(this.tagName)].forEach((i) => {i.removePlayer(player)});
            this.players.add(player);
        });
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
            newPlayer.classList.add("player");
            if (player == currentPlayer()) {newPlayer.classList.add("currentPlayer");}
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
        request.open("GET", "/api/move_to_room?time=" + time + "&deck=" + this.deck.id + "&room=" + this.id);
        request.send();
    }

    loadInfo(event) {
        if (event !== undefined) {event.stopPropagation()}
        document.getElementById("room-name").innerText = this.name + ((this !== currentRoom) ? (": Preview") : "");
        document.getElementById("room-description").innerHTML = this.description;
    
        const roomAbilities = document.getElementById("room-abilities");
        roomAbilities.innerHTML = "";
        this.abilities.forEach((i) => {
            const roomAbility = abilities[i];
            const newRoomAbility = document.createElement("div");
            newRoomAbility.classList.add("room-ability");
            if (abilities[i].enabled) {
                newRoomAbility.classList.add("active");
                if (this === currentRoom) {
                    newRoomAbility.setAttribute("onClick", "javascript: useAbility(\"" + i + "\")");
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
    }

    attributeChangedCallback(name, oldValue, newValue) {this[name] = newValue}

    setStyle() {
        this.style.width = "3vw";
        this.style.height = ((this.size === "small") ? (2) : (3)) + "vw";

        this.style.paddingRight = ((this.size === "small") ? (0.2) : (0.6)) + "vw";

        this.style.backgroundColor = "#DDD";

        this.style.borderColor = "#F50";
        this.style.borderRadius = "0 0.5vw 0.5vw 0";
        this.style.borderStyle = "solid";
        this.style.borderWidth = "0.3vw 0.3vw 0.3vw 0vw";

        this.style.fontSize = ((this.size === "small") ? (1) : (1.8)) + "vw";
        this.style.fontWeight = "bold";

        this.style.left = "-1%";

        this.style.textAlign = "right";

        this.style.translate = "0, -50%";

        this.style.zIndex = 10;
    }

    select() {
        [...document.getElementsByTagName(this.tagName)].forEach((i) => {i.deselect()})
        this.style.left = "0%";
        this.style.borderColor = "#6A2";
        document.getElementById(this.deck).hidden = false;
    }

    deselect() {
        this.style.left = "-1%";
        this.style.borderColor = "#F50";
        if (document.getElementById(this.deck) !== null) {
            document.getElementById(this.deck).hidden = true;
        }
    }
}
customElements.define("ship-deck-selector", ShipDeckSelector);