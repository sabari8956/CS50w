document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // onSubmit form
  document.querySelector("#compose-form").addEventListener('submit', (e) => {

    // preventing it from reloading
    e.preventDefault();

    // getting Values from form
    const recipients_data = document.querySelector('#compose-recipients').value;
    const subject_data = document.querySelector('#compose-subject').value;
    const body_data = document.querySelector('#compose-body').value;

    // using api to post data
    fetch('emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients_data,
        subject: subject_data,
        body: body_data
      })
    })
      .then(response => response.json())
      .catch(error => {
        console.log(error);
      })
      .then(response => {
        // Redirects to Sent Page
        load_mailbox('sent');
      })
  })
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Loads mails
  const parentDiv = document.querySelector('#emails-view');
  fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .catch(error => {
      console.log(error);
    })
    .then(mails => {
      // Creates a div , with mail details and adds to div
      mails.forEach(mail => {

        // Mail Container
        const mailDiv = document.createElement('div');
        mailDiv.classList.add('mail-divs');

        // mail Data
        const senderAddress = document.createElement('h2');
        senderAddress.innerHTML = mail.sender;
        const subject = document.createElement('h4');
        subject.innerHTML = mail.subject;
        const body = document.createElement('p');
        body.innerHTML = mail.body;

        // if mail is read
        if (mail.read) {
          mailDiv.style.backgroundColor = 'aliceblue';
        }
        // on Clicking a Mail 
        mailDiv.addEventListener('click', () => mail_view(mail.id));
        mailDiv.append(senderAddress, subject, body);
        parentDiv.append(mailDiv);
      });
    })
}


function mail_view(mail_id) {

  // Showing only the mail and hiding the rest
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';

  // Setting the html to none so the previous mail won't show 
  const parentDiv = document.querySelector('#mail-view');
  parentDiv.innerHTML = "";

  // Getting the mal data 
  fetch(`emails/${mail_id}`)
    .then(response => response.json())
    .then(data => {
      fetch(`emails/${mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })

      // Creating Containers to Show the mail data
      const headersDiv = document.createElement('div');
      const subject_data = document.createElement('h1');
      const sender_data = document.createElement('h4');
      const body_data = document.createElement('p');
      const otherData = document.createElement('p');
      const reply_btn = document.createElement('button');
      const archive = document.createElement('button');

      // Assigning values to elements 
      otherData.innerHTML = data.timestamp;
      subject_data.innerHTML = data.subject;
      sender_data.innerHTML = data.sender;
      body_data.innerHTML = data.body;
      reply_btn.innerHTML = 'Reply';

      // Adds event lisner to reply btn
      reply_btn.addEventListener('click', () => reply_mail(data))
    
      // Toggle archive true <-> false
      const archive_data = data.archived;
      if (!archive_data) {
        archive.innerHTML = "Archive";
        archive.addEventListener('click', () => {
          fetch(`/emails/${mail_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
            .then(response => {
              load_mailbox('archive');
            })
        })
      }

      else {
        archive.innerHTML = "UN Archive";
        archive.addEventListener('click', () => {
          fetch(`/emails/${mail_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
            .then(response => {
              load_mailbox('inbox');
            })
        })
      }

      // Appends everythinh into to child div and appends child div to parent div
      headersDiv.append(subject_data, sender_data, body_data, otherData, archive, reply_btn);
      parentDiv.append(headersDiv);
    })
}


function reply_mail(data) {
  // Goes to Compose section 
  compose_email();

  // Pre-Filling the mail data
  document.querySelector('#compose-recipients').value = data.sender;
  console.log(data.subject);
  var reply_msg = data.subject;
  if (!reply_msg.startsWith("Re:")) {
    reply_msg = "Re :" + reply_msg;
  }
  document.querySelector('#compose-subject').value = reply_msg;
  document.querySelector('#compose-body').value = `On ${data.timestamp} ${data.sender} wrote: ${data.body}\n`;
}