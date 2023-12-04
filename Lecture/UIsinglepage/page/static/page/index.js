document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach (btn => {
        btn.onclick = function() {
            const section = this.dataset.sec;

            // Add the current state to the history
            history.pushState({section: section}, "", `?section${section}`);
            showSection(section);
        }
    })
})
window.onpopstate = function(event) {
    showSection(event.state.section);
}


function showSection(page) {
    fetch(`section/${page}`)
    .then(response => response.text())
    .then(text => {
        document.querySelector('#content').innerHTML = text;
    })
}