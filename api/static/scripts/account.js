const token = localStorage.getItem('jwt');

document.addEventListener('click',(e)=>{
    if (e.target.id == 'logout') {
        window.location.href = '/logout'
    }
    if (e.target.id == 'delete_account_btn') {
        window.location.href = `/auth/delete/${token}`
    }
})

async function authStatus() {
    if (!token) {
        console.log('no token found')
        window.location.href = '/'
        return;
    }
    try {
        const response = await fetch("/auth/account_data", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` 
            }
        });

        if (response.ok) {
            console.log('logged in');
        }

        const data = await response.json();
        document.getElementById("mail").innerText = data.user;
        document.getElementById("account_img_src").src = data.profile_picture 
    } catch (error) {
        console.error("Error fetching protected data:", error);
    }
}

window.addEventListener('DOMContentLoaded',authStatus);