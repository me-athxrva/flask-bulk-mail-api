gsap.registerPlugin(ScrollTrigger);

oauth_login_btn = document.getElementById('oauth_login');

oauth_login_btn.addEventListener('click',()=>{
    window.location.href = '/auth/login'
    setTimeout(() => {
        preloaderAnim('page_out')
    }, 500);
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
        preloaderAnim();
        return console.error("No token found!");
    }

    try {
        const response = await fetch("/auth/status", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        let data;
        try {
            data = await response.json();  
        } catch (error) {
            console.error("Failed to parse JSON. Response might not be JSON:", error);
            return;
        }

        if (response.ok) {
            const app = document.getElementById("app");
            app.innerHTML = data.html; 
            // loadExternalScript('/static/scripts/preloader.js');
            loadExternalScript('/static/scripts/home.js');
            preloaderAnim();
        } else {
            console.log("Authentication failed:", data?.error || "Unknown error.");
            preloaderAnim();
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

document.addEventListener("DOMContentLoaded",()=>{
    checkAuthStatus();
    
});