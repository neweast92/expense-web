const usernameField=document.querySelector('#usernameField');
const feedBackField=document.querySelector('.invalid-feedback')

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
                usernameField.classList.add("is-invalid");
                feedBackField.style.display="block";
                feedBackField.innerHTML='<p>'+data.username_error+'</p>';
            } else {
                usernameField.classList.remove("is-invalid");
                feedBackField.style.display="none";
            }
        }); 
    }
})