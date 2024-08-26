const get_gamse_data_button = document.getElementById("get_games_data_button");
const games_data = document.getElementById("games_data");


async function getGamesData() {
    const formData = new FormData();
    formData.append("user_id", user_id);
    const response = await fetch("/get_games_data", {
        method: "POST",
        body: formData,
    });
    const json = await response.json();
    let res = json["response"];
    let table = '<br><br><table style="margin: 0 auto; border:none;text-align:center"><tr><th>Date</th><th class="px-5">WPM</th><th>Accuracy</th></tr>';
    let l = res.length;
    for (let i = 0; i < l; i++) {
        let date = res[i][0].toString().substring(0, 16);
        let wpm = Math.round(res[i][1]);
        let accuracy = Math.round(res[i][2]);
        table += `<tr><td>${date}</td><td class="px-5 text-center">${wpm}</td><td class="text-center">${accuracy}%</td></tr>`;
    }
    table += "</table><br><br>";

    games_data.innerHTML = table;
}


get_gamse_data_button.addEventListener("click", getGamesData);