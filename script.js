
JSON_FILE = "output.json"

function createUserElem(userData, rank) {
	elem = document.createElement("div");
	elem.classList.add("user");
	elem.addEventListener("click", (event) => {
		window.open(`https://profile-v3.intra.42.fr/users/${userData.user.login}`)
	});
		
	img = document.createElement("img");
	img.src = userData.user.image.versions.medium;
	
	level = document.createElement("p");
	// level.innerText = userData.level;
	level.innerText = (Math.round(parseFloat(userData.level) * 100) / 100).toFixed(2);

	username = document.createElement("p");
	username.innerText = userData.user.login;

	rankElem = document.createElement("p");
	rankElem.innerText = `#${rank}`;
	rankElem.classList.add("rank");

	elem.appendChild(img);
	elem.appendChild(level);
	elem.appendChild(username);
	elem.appendChild(rankElem);
	return elem;
}

document.addEventListener("DOMContentLoaded", (event) => {
	fetch(JSON_FILE)
	.then(response => {
		if (!response.ok) {
			throw new Error(`Error loading ${JSON_FILE}`);
		}
		return response.json();
	})
	.then(data => {
		let counter = 1;
		data.forEach(user => {
			document.body.appendChild(createUserElem(user, counter));
			counter++;		
		});
	})
	.catch(error => console.error(error));
});