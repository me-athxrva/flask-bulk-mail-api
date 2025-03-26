const token = localStorage.getItem("jwt");
let task_id;
document.addEventListener("click", function (event) {

    let dropdown = document.getElementById("profile_dropdown");

    if (event.target.id === "profile_pic") {
        let currentOpacity = window.getComputedStyle(dropdown).opacity;

        if (currentOpacity === "1") {
            dropdown.style.opacity = "0";
            dropdown.style.visibility = "hidden";
        } else {
            dropdown.style.opacity = "1";
            dropdown.style.visibility = "visible";
        }
    }

    if (event.target.id === "logout_btn") {
        console.log("Logout button clicked!");
        localStorage.removeItem('jwt');
        window.location.href = "/logout";
    }
    if (event.target.id === "send_mails") {
        sendMails();
    }
    if (event.target.id === "copy_token") {
        document.getElementById(event.target.id).innerText = 'Copied!';
        navigator.clipboard.writeText(token);
        gsap.set('#copy_token',{
            background: 'greenyellow',
            onComplete: ()=>{
                setTimeout(() => {
                    document.getElementById(event.target.id).innerText = 'Copy';
                    gsap.to('#copy_token',{
                        background: 'white',
                        duration: 0.5,
                        ease: 'none'
                    }) 
                }, 3000);
            }
        })
        
    }
});

window.addEventListener("click", (event) => {
    let dropdown = document.getElementById("profile_dropdown");

    if (!event.target.closest("#account") && dropdown.style.opacity === "1") {
        dropdown.style.opacity = "0";
        dropdown.style.visibility = "hidden";
    }
});

async function sendMails() {
    const recipients = document.getElementById('recipients_inp').value.split(",").map(email => email.trim());
    const subject = document.getElementById('subject_inp');
    const message = document.getElementById('body_inp');

    if (!token) {
        return alert('please login again!')
    }

    if (recipients.length >= 100) {
        alert('Google Restriction. Only first 100 will be processed.');
        recipients.length = 100;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/sendMails", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                recipients: recipients,
                subject: subject.value,
                body: message.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            task_id = data.task_id
            return alert(`${data.message} & Your task id is ${data.task_id}`)
        } else {
            console.log("Authentication failed.");
        }
    } catch (error) {
        console.error("Error checking authentication status:", error);
    }
}

function setAccInfo(){
    document.getElementById('access_key').innerHTML = token;
}



window.addEventListener('DOMContentLoaded',setAccInfo())