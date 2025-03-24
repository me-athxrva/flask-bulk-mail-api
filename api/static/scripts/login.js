gsap.registerPlugin(ScrollTrigger);


oauth_login_btn = document.getElementById('oauth_login');

oauth_login_btn.addEventListener('click',()=>{
    window.location.href = '/auth/login'
})

gsap.fromTo(".fade_out",{
    opacity: 1,
    display: 'flex'
},{
    opacity: 0,
    duration: 0.2,
    ease: 'none',
    display: 'none',
    scrollTrigger: {
        trigger: '#container1',
        start: '20% top',
        endTrigger: '#container1',
        end: '20% top',
        toggleActions: 'play none none reverse',
    },
});

async function checkAuthStatus() {
    const token = localStorage.getItem("jwt");

    if (!token) {
        return console.error("No token found!")
    }

    try {
        const response = await fetch("/auth/status", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (response.ok) {
            const app = document.getElementById("app");  
            app.innerHTML = "";
            app.innerHTML = data.html;
            loadExternalScript('/static/scripts/home.js');
        } else {
            console.log("Authentication failed.");
        }
    } catch (error) {
        console.error("Error checking authentication status:", error);
    }
}


function loadExternalScript(src) {
    const existingScript = document.querySelector(`script[src="${src}"]`);
    if (existingScript) {
        existingScript.remove(); 
    }

    const script = document.createElement("script");
    script.src = src;
    script.type = "text/javascript";
    script.async = false;
    script.onload = () => console.log(`Loaded script: ${src}`);
    
    document.body.appendChild(script);
}

document.addEventListener("DOMContentLoaded", checkAuthStatus);