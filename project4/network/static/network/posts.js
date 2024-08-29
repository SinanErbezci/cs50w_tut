document.addEventListener('DOMContentLoaded', function() {

    // event listeners for sections
    document.querySelector('#post-nav').addEventListener('click', load_post);
    document.querySelector('#profile-nav').addEventListener('click', load_profile);
    document.querySelector('#follow-nav').addEventListener('click', load_follow);

    // loading posts default
    load_post();
  });
  
function load_post() {
    const postDiv = document.querySelector('.posts')
    postDiv.style.display = 'block';
    document.querySelector('.profile').style.display = 'none';
    document.querySelector('.follow').style.display = 'none';

    fetch('/posts')
    .then(response => response.json())
    .then(post => {
        console.log(post);
        for (let i = 0; i < post.length; i++) {
            let row = document.createElement('div');
            let username = document.createElement('p');
            let content = document.createElement('p');
            let time = document.createElement('p');

            row.classList = 'post';
            username.innerHTML = post[i].owner;
            content.innerHTML = post[i].content;
            time.innerHTML = post[i].time;
            
            row.appendChild(username);
            row.appendChild(content);
            row.appendChild(time);
            postDiv.appendChild(row);
        }
    })
}

function load_profile() {
    document.querySelector('.posts').style.display = 'none';
    document.querySelector('.profile').style.display = 'block';
    document.querySelector('.follow').style.display = 'none';
}

function load_follow() {
    document.querySelector('.posts').style.display = 'none';
    document.querySelector('.profile').style.display = 'none';
    document.querySelector('.follow').style.display = 'block';
}