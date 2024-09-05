document.addEventListener('DOMContentLoaded', function() {

    let followBtn = document.querySelector('#follow-button');
    if (typeof maybeObject != "undefined") {
        document.querySelector('#follow-button').addEventListener('click', follow);
    }

    let likeBtns = document.querySelectorAll('.like-btn');
    if (typeof likeBtns != "undefined") {
    likeBtns.forEach((button) => {
        button.onclick = like;
    });}

  });

function follow() {		
    // API Call
    const id = this.dataset.id;

    // Animation
    if (this.innerHTML == "Follow") {
        fetch(`/follow/${id}`, {
            method: "POST",
            body: JSON.stringify({
                text: 'follow'
              })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });
        this.animate({backgroundColor: "#3399FF"}, {duration:500, fill:"forwards"});
        this.innerHTML = "Unfollow";
        this.style.color = "#FFF";
    }
    else {
        fetch(`/follow/${id}`, {
            method: "POST",
            body: JSON.stringify({
                text: 'unfollow'
              })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });
        this.animate({backgroundColor: "#FFF"}, {duration:500, fill:"forwards"});
        this.innerHTML = "Follow";
        this.style.color = "#000";
      }
    } 

function like() {
    const id = this.dataset.id;
    fetch(`/like/${id}`, {
        method: "POST"})
    .then(response => response.json())
    .then(out => {
        if (out.out == "liked") {
            let parent = this.parentElement;
            parent.lastChild.innerHTML = parseInt(parent.lastChild.innerHTML) + 1;
        }
        else {
            let parent = this.parentElement;
            parent.lastChild.innerHTML = parseInt(parent.lastChild.innerHTML) + -1;
        }
    })
}