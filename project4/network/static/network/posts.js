document.addEventListener('DOMContentLoaded', function() {

    let followBtn = document.querySelector('#follow-button');
    if (typeof maybeObject != "undefined") {
        document.querySelector('#follow-button').addEventListener('click', follow);
    }

    let likeBtns = document.querySelectorAll('#like-btn');
    if (typeof likeBtns != "undefined") {
    likeBtns.forEach((button) => {
        button.onclick = like;
    });}

    let editBtns = document.querySelectorAll('#edit-btn');
    if (typeof editBtns != "undefined") {
        editBtns.forEach((button) => {
            button.onclick = edit;
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

function edit() {
    const postDiv = this.parentElement;
    let content = postDiv.children[2];
    
    const newText = document.createElement("textarea");
    newText.innerHTML = content.innerHTML;
    newText.classList = "form-control";
    newText.required = true;

    const submitBtn = document.createElement("button");
    const cancelBtn = document.createElement("button");
    submitBtn.classList = "btn btn-primary submit-btn";
    submitBtn.innerHTML = "Submit";
    cancelBtn.classList = "btn btn-dark cancel-btn";
    cancelBtn.innerHTML = "Cancel";
    
    postDiv.appendChild(newText);
    postDiv.appendChild(submitBtn);
    postDiv.appendChild(cancelBtn);
    this.style.display = "none";
    content.style.display = "none";    
    newText.focus();

    submitBtn.addEventListener("click", editPost);
    cancelBtn.addEventListener("click", editPost);

}

function editPost() {
    if (this.innerHTML === "Cancel") {
        let divChild = this.parentElement.children;
        let content = divChild[2];
        let editBtn = divChild[1];
        content.style.display = "block";
        editBtn.style.display = "block";

        for(let i=0; i < 3; i++){
            divChild[5].remove();
        }
    }
    else {
        const content = this.parentElement.children[5].value;
        const id = this.parentElement.dataset.id;
        
        if (content.length > 0) {
        fetch(`/edit/${id}`, {
            method: "PATCH",
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(out => {
            if (out["success"] === "yes" ) {
                let divChild = this.parentElement.children;
                divChild[2].innerHTML = content;
                divChild[2].style.display = "block";
                divChild[1].style.display = "block";

                for(let i=0; i < 3; i++){
                    divChild[5].remove();
                }
            }
        });}
        else {
            this.parentElement.children[5].placeholder = "Please Fill this area or Cancel";
        }
    }

}