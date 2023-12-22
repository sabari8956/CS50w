import { getCookie  } from "./index.js";

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#search-users").addEventListener('click', () => {
        let query = document.querySelector("#query-user").value;
        let csrftoken = getCookie('csrftoken');
        fetch("/finduser", {  // Use 'searchuser' without a trailing slash
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                query: query
            })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the data, e.g., update the search results in the UI
            const parent_div = document.querySelector("#search-result");
            parent_div.innerHTML = '';
            data.users.forEach(user => {
                const childDiv = document.createElement('div');
                const name = document.createElement('h2');
                const follower = document.createElement('p');
                const following = document.createElement('p');
                name.innerHTML = user.username;
                follower.innerHTML = 'followers: ' + user.followers;
                following.innerHTML = 'following: ' + user.following;
                childDiv.append(name, follower, following);

                childDiv.addEventListener('click', () => {
                    window.location.href= `/profile/${user.username}`;
                })
                parent_div.append(childDiv);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
