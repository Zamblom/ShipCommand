var diceRollInterval;

function rollByLabel(label) {
    if (document.getElementById("revert-player").hidden) {
        rollDiceDisplay(parseInt(label.nextElementSibling.innerHTML));
    }
}

function rollByValue(value) {
    if (document.getElementById("revert-player").hidden) {
        rollDiceDisplay(parseInt(value.innerHTML));
    }
}

function hideDiceDisplay() {
    document.getElementById("dice-display").hidden = true;
    document.getElementById("click-blocker").hidden = true;
    clearInterval(diceRollInterval);
}

function showDiceDisplay() {
    document.getElementById("dice-display").hidden = false;
    document.getElementById("click-blocker").hidden = false;
}

function updateDiceDisplay(number) {
    var digit1 = Math.floor(number / 10 % 10);
    var digit2 = number % 10;
    if (digit1 === 0) {
        digit1 = "";
    } else if (digit2 < 0) {
        digit1 = "-";
        digit2 = -digit2;
    }
    updateDiceDigit(document.getElementById("digit-1"), digit1);
    updateDiceDigit(document.getElementById("digit-2"), digit2);
}

function updateDiceDigit(digit, value) {
    var segments = digit.children;
    var active = [false, false, false, false, false, false, false];
    switch (value) {
        case "-":
            active[3] = true;
            break;
        case 0:
            active[0] = true;
            active[1] = true;
            active[2] = true;
            active[4] = true;
            active[5] = true;
            active[6] = true;
            break;
        case 1:
            active[2] = true;
            active[5] = true;
            break;
        case 2:
            active[0] = true;
            active[2] = true;
            active[3] = true;
            active[4] = true;
            active[6] = true;
            break;
        case 3:
            active[0] = true;
            active[2] = true;
            active[3] = true;
            active[5] = true;
            active[6] = true;
            break;
        case 4:
            active[1] = true;
            active[2] = true;
            active[3] = true;
            active[5] = true;
            break;
        case 5:
            active[0] = true;
            active[1] = true;
            active[3] = true;
            active[5] = true;
            active[6] = true;
            break;
        case 6:
            active[0] = true;
            active[1] = true;
            active[3] = true;
            active[4] = true;
            active[5] = true;
            active[6] = true;
            break;
        case 7:
            active[0] = true;
            active[2] = true;
            active[5] = true;
            break;
        case 8:
            active[0] = true;
            active[1] = true;
            active[2] = true;
            active[3] = true;
            active[4] = true;
            active[5] = true;
            active[6] = true;
            break;
        case 9:
            active[0] = true;
            active[1] = true;
            active[2] = true;
            active[3] = true;
            active[5] = true;
            active[6] = true;
            break;
    }
    for (let i = 0; i < 7; i++) {
        if (active[i]) {
            segments[i].classList.add('active');
        } else {
            segments[i].classList.remove('active');
        }
    }
}

function rollDiceDisplay(modifier = 0) {
    document.getElementById("roll-result").innerHTML = "Rolling";
    document.getElementById("roll-calculation").innerHTML = "[1d20 " + ((modifier >= 0) ? ("+") : ("-")) + " " + Math.abs(modifier) + "]";
    showDiceDisplay();
    updateDiceDisplay(0);
    var iter = 110;
    var roll = 0;
    diceRollInterval = setInterval(function() {
        var newRoll = roll;
        while (roll === newRoll) {
            newRoll = Math.ceil(Math.random() * 20)
        }
        roll = newRoll;
        updateDiceDisplay(roll);
        switch (iter) {
            case 130:
                document.getElementById("roll-result").innerHTML = "Rolling.";
                break;
            case 140:
                document.getElementById("roll-result").innerHTML = "Rolling..";
                break;
            case 150:
                document.getElementById("roll-result").innerHTML = "Rolling...";
                break;
            case 160:
                document.getElementById("roll-result").innerHTML = "Total -> " + (roll + modifier);
                clearInterval(diceRollInterval);
                break;
        }
        iter += 5;
    }, iter);
}
