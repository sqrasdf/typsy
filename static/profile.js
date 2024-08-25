const get_gamse_data_button = document.getElementById("get_games_data_button");
const games_data = document.getElementById("games_data");


async function getGamesData() {
    const formData = new FormData();
    formData.append("user_id", user_id);
    const response = await fetch("/get_games_data", {
        method: "POST",
        body: formData,
    });
    const text = await response.text();
    console.log(typeof(text));
    games_data.innerText = text;
}


get_gamse_data_button.addEventListener("click", getGamesData);