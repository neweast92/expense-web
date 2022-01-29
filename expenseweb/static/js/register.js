const usernameField=document.querySelector('#usernameField');
const usernameFeedBackField=document.querySelector('.username-feedback')
const emailField=document.querySelector('#emailField')
const emailFeedBackField=document.querySelector(".email-feedBack")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")
const passwordField = document.querySelector("#passwordField")
const showPasswordToggle=document.querySelector('.showPasswordToggle')
const submitBtn = document.querySelector('.submit-btn')

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === 'SHOW'){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text")
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password")
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput);

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    
    if (emailVal.length > 0){
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVal}),
            method:"POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.email_error){
                submitBtn.disabled = true;

                emailField.classList.add("is-invalid");
                emailFeedBackField.style.display="block";
                emailFeedBackField.innerHTML=`<p>${data.email_error}</p>`;
            } else {
                submitBtn.removeAttribute('disabled')

                emailField.classList.remove("is-invalid");
                emailFeedBackField.style.display="none";
            }
        }); 
    }
})

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    
    if (usernameVal.length > 0){
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}),
            method:"POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.username_error){
                submitBtn.disabled = true;

                usernameField.classList.add("is-invalid");
                usernameFeedBackField.style.display="block";
                usernameFeedBackField.innerHTML=`<p>${data.username_error}</p>`;
            } else {
                submitBtn.removeAttribute('disabled');

                usernameField.classList.remove("is-invalid");
                usernameFeedBackField.style.display="none";
            }
        }); 
    }
})