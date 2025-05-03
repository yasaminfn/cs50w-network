document.addEventListener('DOMContentLoaded', function() {
    //newpost button
    document.querySelector('#new-post-btn').addEventListener('click', new_post); 
    //edit button
    document.querySelectorAll('#edit').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const post_id = this.dataset.postId;
            edit_post(post_id);
        });
    });

    //editpost form
    document.querySelector('#editpost-form').addEventListener('submit', function (event){
        event.preventDefault();
        let content = document.querySelector('#editpost-content').value;;

        //csrf token
        const csrftoken = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

        // sending data
        fetch(`/edit/${current_post_id}`, {
            method: 'PUT',
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
            document.querySelector('#editpost-view').style.display = 'none';
            document.querySelector('#editpost-content').value = '';
            //refresh the page
            location.reload();

        })
        .catch(error => {
            console.log('ERROR', error);
        });
    });

    //newpost form
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
            //refresh the page
            location.reload();
        })
        .catch(error => {
            console.log('ERROR', error);
        });
        
        }
        
    )
})

let current_post_id = null; //global 

function new_post(){
    console.log("adding new post..");
    document.querySelector('#newpost-view').style.display = 'block';
    document.querySelector('#newpost-content').value = '';
    };


function edit_post(post_id){

    console.log("editing post:", post_id);
    document.querySelector('#editpost-view').style.display = 'block';

    current_post_id = post_id;
    
    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data); //post's data
        document.querySelector('#editpost-content').value = `${data.content}`;
    });

    };

