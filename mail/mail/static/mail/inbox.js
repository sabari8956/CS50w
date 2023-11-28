document.addEventListener('DOMContentLoaded', function() {

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
        console.log(response);
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

  const parentDiv = document.querySelector('#emails-view');
  fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .catch(error => {
      console.log(error);
    })
    .then(mails => {
      console.log(mails);
      mails.forEach(mail => {
        const mailDiv = document.createElement('div');
        mailDiv.classList.add('mail-divs');

        const senderAddress = document.createElement('h2');
        senderAddress.innerHTML = mail.sender;
        const subject = document.createElement('h4');
        subject.innerHTML = mail.subject;
        const body = document.createElement('p');
        body.innerHTML = mail.body;

        if (!mail.read)
        {
          mailDiv.style.backgroundColor = '#ccc';
        }
        mailDiv.addEventListener('click', () => mail_view(mail.id));
        mailDiv.append(senderAddress, subject, body);
        parentDiv.append(mailDiv);
      });
    })
}


function mail_view(mail_id) 
{
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';

  const parentDiv = document.querySelector('#mail-view');

  fetch(`emails/${mail_id}`)
  .then(response => response.json())
  .then(data => {
      const headersDiv = document.createElement('div');
      const subject_data = document.createElement('h1');
      subject_data.innerHTML = data.subject;
      const sender_data = document.createElement('h4');
      sender_data.innerHTML = data.sender;
      const body_data = document.createElement('p');
      body_data.innerHTML = data.body;
      headersDiv.append(subject_data, sender_data, body_data);
      parentDiv.append(headersDiv);
  })
}