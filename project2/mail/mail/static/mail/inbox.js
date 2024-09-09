document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_mail);
  document.querySelector('#reply').addEventListener('click', () => compose_email(true));
  document.querySelector('#archieve').addEventListener('click', archieve );
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(prefill=false) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-mail').style.display = 'none';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Clear out composition fields
  if (prefill == true) {
    sender = document.querySelector('#from').innerHTML;
    exSubject = document.querySelector('#subject').innerHTML;
    if (exSubject.slice(0,4) === "Re: ") {
      preSubject = "";
    }
    else {
      preSubject = "Re: ";
    }
    preBody = `On ${document.querySelector('#time').innerHTML} ${sender} wrote:`;
    document.querySelector('#compose-recipients').value = sender;
    document.querySelector('#compose-subject').value = preSubject.concat(document.querySelector('#subject').innerHTML);
    document.querySelector('#compose-body').value = preBody.concat(document.querySelector('.mail-body__p').innerHTML);
  }
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-mail').style.display = 'none';

  // Show the mailbox name
  const emailDiv = document.querySelector('#emails-view');
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(email => {
      for (let i = 0; i < email.length; i++) {
        let row = document.createElement('div');
        let sender = document.createElement('p');
        let topic = document.createElement('p');
        let time = document.createElement('p');

      if (mailbox === 'inbox') {
        sender.innerHTML = email[i].sender;
      }
      else if (mailbox === 'sent') {
        if (email[i].recipients.length > 1) {
          sender.innerHTML = email[i].recipients[0].concat(' + more')
        }
        else {
          sender.innerHTML = email[i].recipients[0]
        }
      }
      // sender.innerHTML = email[i].sender;
      topic.innerHTML = email[i].subject;
      time.innerHTML = email[i].timestamp;

      row.classList.add('emails-container');
      if ((email[i].read === true) && (mailbox === 'inbox')) {
        row.classList.add('read');
      }
      row.addEventListener('click', () => view_mail(email[i].id));  
      sender.classList = 'sender';
      topic.classList = 'topic';
      time.classList = 'time';

      emailDiv.appendChild(row);
      row.appendChild(sender);
      row.appendChild(topic);
      row.appendChild(time);
    }




    // ... do something else with email ...
  });
}

function send_mail(event) {
  event.preventDefault();
  
  const body = document.querySelector('#compose-body').value;
  const subject = document.querySelector('#compose-subject').value;
  const receivers = document.querySelector('#compose-recipients').value;

  if ( body === '' || subject === '' || receivers === ''){
    alert('Please fill all of the parts');
    }
  else {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: receivers,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent')

    });
  // load_mailbox('sent')
  }

  return false;
  }

function view_mail(mail_id) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view'  ).style.display = 'none';
  document.querySelector('#view-mail').style.display = 'block';
  document.querySelector('#archieve').style.display = 'inline';

  const title = document.querySelector('#emails-view').firstChild.innerHTML;
  const archieveBtn = document.querySelector('#archieve');
  archieveBtn.dataset.id = mail_id;

  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#from').innerHTML = email.sender;
    document.querySelector('#to').innerHTML = email.recipients.toString();
    document.querySelector('#subject').innerHTML = email.subject;
    document.querySelector('#time').innerHTML = email.timestamp;
    document.querySelector('.mail-body__p').innerHTML = email.body;

    if (title != "Sent") {
      if (email.archived === true) {
        archieveBtn.innerHTML = "Unarchieve";
      }
      else {
        archieveBtn.innerHTML = "Archieve";
      }}
    else {
      archieveBtn.style.display = "none";
    }

  });

  fetch(`/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
}

function archieve() {

  if (this.innerHTML === "Archieve") {
  fetch(`/emails/${this.dataset.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(() => load_mailbox('inbox'));}
  else {
    fetch(`/emails/${this.dataset.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(() => load_mailbox('inbox'));}
}