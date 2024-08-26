const menuButton = document.getElementById('menu-button');
const dropdown = document.getElementById('dropdown');
const text_to_type = document.getElementById("text-container");
const button = document.getElementById("restart-button");    
const wpmField = document.getElementById("wpm");
const accuracyField = document.getElementById("accuracy");

let words = "";
let current_index = 0;
let writing = false;
let words_count = 0;
let startTime;
let mistakes;

async function getData(){
    text_to_type.innerHTML = "";
    words_count = 1;
    current_index = 0;
    mistakes = 0;
    writing = false;
    fetch('/get_data')
    .then(response=>response.json())
    .then(data=>{ 
        words = data["words"];
        // console.log(words); 
        for (let i in words) {
            let current = words[i];
            if (current == " ") words_count++;
            let span = document.createElement("span");
            span.innerText = current;
            span.id = i;
            span.classList.add("clean");
            text_to_type.appendChild(span);
        }
    });
}

async function sendData(wpm, accuracy) {
    const formData = new FormData();
    formData.append("wpm", wpm);
    formData.append("accuracy", accuracy);
    // formData.append("date", new Date().toString())
    const response = await fetch("/send_data", {
        method: "POST",
        body: formData,
    });
}

function isLetter(c) {
    return /^[a-zA-Z]$/.test(c);
}

function checkLetter(event) {
    let current_span = document.getElementById(current_index);
    let current_letter = event.key;

    if (!writing) {
        startTime = Date.now();
        writing = true;
    }

    // console.log(event.key);
    if (event.key == "Backspace") {
        text_to_type.children[current_index - 1].className = "clean";
        current_index--;
        return;
    }

    // end of the words to type
    if (current_index == words.length){
        return;
    }

    if (isLetter(current_letter) || current_letter === " " || current_letter === "'"){
        if (current_letter == words[current_index]) {
            current_span.className = "correct";
            // end game
            if (current_index + 1 === words.length){
                console.log("end game");
                // display wpm
                let sec_diff = (Date.now() - startTime) / 1000;
                let wpm = words_count / (sec_diff / 60);
                wpmField.innerText = Math.round(wpm) + "wpm";

                // display accuracy
                let accuracy = 100 - mistakes / words.length * 100;
                accuracyField.innerText = Math.round(accuracy) + "%";

                // send wpm and accuracy to the server
                if (user_id) {
                    console.log("sending data to server");
                    sendData(wpm, accuracy);
                }

                getData();
                return;
            }
        }
        else {
            current_span.className = "incorrect";
            mistakes++;
        }
        current_index++;
    }
}

function removeFocus() {
    let tmp = document.createElement("input");
    document.body.appendChild(tmp);
    tmp.focus();
    document.body.removeChild(tmp);
}


button.addEventListener("click", getData);
button.addEventListener("click", removeFocus);
document.addEventListener("keydown", (event) => checkLetter(event));

getData();
