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
    const username = this.dataset.username;
    fetch(`/follow/${username}`, {method: "POST"});

    // Animation
    if (this.innerHTML == "Follow") {
        this.animate({backgroundColor: "#3399FF"}, {duration:500, fill:"forwards"});
        this.innerHTML = "Unfollow";
        this.style.color = "#FFF";
    }
    else {
        this.animate({backgroundColor: "#FFF"}, {duration:500, fill:"forwards"});
        this.innerHTML = "Follow";
        this.style.color = "#000";
      }
    } 