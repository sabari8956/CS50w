import { manage_post, manage_like, manage_comment } from "./index.js";


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
    document.querySelectorAll("#comment-submitBtn").forEach(submitBtn => {
        submitBtn.addEventListener('click',(event) => {
            manage_comment(event);
        } )
    });

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
        post.addEventListener('click', (event) => {
            console.log(post.dataset.post_id);
            
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


