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
        document.getElementById(event.target.id).disabled = true;
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
    if (event.target.id == 'account_btn') {
        window.location.href = '/account'
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
        const response = await fetch("/sendMails", {
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
            setTimeout(() => {
                document.getElementById('send_mails').disabled = false;
            }, 500);
            document.getElementById('tasks').innerHTML = "";
            userTasks();
            return alert(`${data.message} & Your task id is ${data.task_id}`)
        } else {
            console.log("Authentication failed.");
        }
    } catch (error) {
        console.error("Error checking authentication status:", error);
    }
}

const checkElement = setInterval(() => {
    const access_key = document.getElementById("access_key");
    if (access_key) {
        clearInterval(checkElement);
        access_key.innerText = token;
    }
}, 10);
const checkTasks = setInterval(() => {
    const tasks = document.getElementById("tasks");
    if (tasks) {
        clearInterval(checkTasks);
        userTasks();
    }
}, 50);


async function userTasks() {
    try {
        const response = await fetch("/tasks", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        const data = await response.json();

        if (response.ok) {
            data.slice().reverse().forEach(task => {
                createTaskElement(task.task_id, task.status);
            });
        } else {
            console.log("Authentication failed.");
        }
    } catch (error) {
        console.error("Error getting task history:", error);
    }
}

function createTaskElement(taskId, taskStatus) {
    let dummyTask = document.createElement("div");
    dummyTask.id = "dummy_task";

    let taskIdContainer = document.createElement("div");
    taskIdContainer.id = "task_id";

    let idLabel = document.createElement("p");
    idLabel.className = "pTask";
    idLabel.textContent = "Id:";

    let idDiv = document.createElement("div");
    idDiv.id = "id";
    idDiv.textContent = taskId;

    taskIdContainer.appendChild(idLabel);
    taskIdContainer.appendChild(idDiv);

    let taskStatusContainer = document.createElement("div");
    taskStatusContainer.id = "task_status";

    let statusLabel = document.createElement("p");
    statusLabel.className = "pTask";
    statusLabel.textContent = "Status:";

    let statusDiv = document.createElement("div");
    statusDiv.id = "status";
    statusDiv.textContent = taskStatus;
    if(taskStatus=='completed'){
        statusDiv.style.background = 'greenyellow'
    }
    if(taskStatus=='pending'){
        statusDiv.style.background = 'orange'
        statusDiv.style.color = 'white'
    }
    if(taskStatus=='error' || taskStatus=='failed'){
        statusDiv.style.background = 'red'
        statusDiv.style.color = 'white'
    }

    taskStatusContainer.appendChild(statusLabel);
    taskStatusContainer.appendChild(statusDiv);

    dummyTask.appendChild(taskIdContainer);
    dummyTask.appendChild(taskStatusContainer);

    let tasksContainer = document.getElementById("tasks");
    if (tasksContainer) {
        tasksContainer.appendChild(dummyTask);
    } else {
        console.error("Parent container with id 'tasks' not found.");
    }
}