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

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}