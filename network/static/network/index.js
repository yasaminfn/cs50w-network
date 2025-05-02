document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new-post-btn').addEventListener('click', new_post);
    document.querySelector('#newpost-form').addEventListener('submit', function (event) {

        event.preventDefault();

        // storing data
        let content = document.querySelector('#newpost-content').value;

        // sending data
        //csrf token
        const csrftoken = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
        fetch('/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                content: content,
            
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
            document.querySelector('#newpost-view').style.display = 'none';
            document.querySelector('#newpost-content').value = '';
        })
        .catch(error => {
            console.log('ERROR', error);
        });
        
        }
        
    )
})

function new_post(){
    console.log("hi");
    document.querySelector('#newpost-view').style.display = 'block';
    document.querySelector('#newpost-content').value = '';
    };


