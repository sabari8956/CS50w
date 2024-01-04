import {getCookie, manage_post, manage_like, manage_comment } from "./index.js";


document.addEventListener("DOMContentLoaded", () => {

    // Handles Post
    const postBtn = document.querySelector("#post-btn");

    if (postBtn) {
        postBtn.addEventListener('click', () => {
            manage_post();
        });
    }

    // Handles Like
    document.querySelectorAll('#like-btn').forEach(btn => {
        btn.addEventListener('click', (event) => {
            manage_like(event);            
        });
    });

    // Handles Comment
    // ERROR HERE
    // document.querySelectorAll("#comment-submitBtn").forEach(submitBtn => {
    //     console.log(submitBtn); // This should log the entire dataset object
    //     submitBtn.addEventListener('click', (event) => {
    //         console.log(submitBtn); 
    //         manage_comment(event);
    //     });
    // });
    

    // expands / shrink the comment area
    document.querySelectorAll('#comment-btn').forEach(commentBtn => {
        commentBtn.addEventListener('click', (event) => {
            const commentSection = event.target.nextElementSibling;
            if (commentSection.style.display === 'none'){
                commentSection.style.display = 'block';
                commentBtn.innerHTML = "Discard";
            } else {
                commentSection.style.display = 'none';
                commentBtn.innerHTML= "Comment";
            }
        });
    });

    document.querySelectorAll(".post-container").forEach(post => {
        post.addEventListener('click', () => {            
            fetch(`post/${post.dataset.post_id}`, {
                method: "POST",
                headers: { "X-CSRFToken": getCookie('csrftoken') }
            })
            .then(response => response.json())
            .then(response => {
                let hoverDiv = document.querySelector("#text");
                let post_user = hoverDiv.querySelector(".post_username");
                let post_content = hoverDiv.querySelector(".post_content");

                response = response["postData"]
                post_user.textContent = response["user"];
                post_content.textContent = response["content"];
            });
            const postOverlay = document.querySelector("#post-overlay");
            postOverlay.style.display = 'block';
            postOverlay.classList.add('blurred-background');
        });
    });
    
    document.querySelector("#post-overlay").addEventListener('click', (event) => {
        const clickedElement = event.target;
        const isWithinContent = clickedElement.closest("#text");
    
        if (!isWithinContent) {
            const postOverlay = document.querySelector("#post-overlay");
            postOverlay.style.display = 'none';
            postOverlay.classList.remove('blurred-background');
        }
    });
    
    
})


