export function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }


export function manage_like(event) {
    let csrftoken = getCookie('csrftoken');
    fetch('auth',{
        method: "POST"
    })
    .then(response => response.json())
    .then(response => {
        let user = response["user_id"];
        let liked = event.target.dataset.like === 'true';
        let post = event.target.dataset.post_id;
        fetch('/addlike', {
            method: "PUT",
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                user_id: user,
                like: !liked,
                post: post,
            })
        })
        .then(response => response.json())
        .then(response => {
            if (!liked) {
                event.target.innerHTML = '👎';
                event.target.dataset.like = !liked;
            } else {
                event.target.textContent = '👍';
                event.target.dataset.like = !liked;
            }
        });
    })
}


export function manage_comment(event) {
    
    let csrftoken = getCookie('csrftoken');
    let user;
    fetch('auth',{
        method: "POST"
    })
    .then(response => response.json())
    .then(response => {
        user = response["user_id"];
        let post_id = event.currentTarget.dataset.post_id;
        console.log(post_id);
        let comment_data = event.currentTarget.previousElementSibling;
        fetch('addcomment', {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                user_id: user,
                post_id: post_id,
                comment_data: comment_data.value
            })
        })
        comment_data.value = '';
        let commentBtn = event.target.closest('.post-container').querySelector('#comment-btn');
        commentBtn.click();
    
    })
}


export function manage_post() {
    let text = document.querySelector("#post-content-input").value;
    let csrftoken = getCookie('csrftoken');
    fetch('post', {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        body: JSON.stringify({
            content: text
        })
    })
    .then(response => response.json())
    .then(response => {
        document.querySelector("#post-content-input").value = "";
        console.log(response);
    });
}