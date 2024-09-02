document.addEventListener('DOMContentLoaded', function() {

    const followButton = document.querySelector('#follow-button');
    if (followButton.innerHTML === 'Follow') {
        followButton.style.backgroundColor = "white";
    }
    else {
        followButton.style.backgroundColor = "#3399FF";
        followButton.style.color = "#FFF";
    }
    followButton.addEventListener('click', follow);

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