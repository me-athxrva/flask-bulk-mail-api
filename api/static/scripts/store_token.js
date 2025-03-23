function getTokenFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("tk");
}

function storeToken() {
    const token = getTokenFromUrl();

    if (token) {
        localStorage.setItem("jwt", token);
        console.log("JWT stored successfully!");
        
        setTimeout(checkAuthStatus, 500);
    }
}

async function checkAuthStatus() {
    const token = localStorage.getItem("jwt");

    if (!token) {
        console.log("No token found. Redirecting to login...");
        return window.location.replace('/auth/login'); 
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
            console.log("User authenticated:", data);
            window.location.replace('/'); 
        } else {
            console.warn("Authentication failed:", data);
            localStorage.removeItem("jwt"); 
            window.location.replace('/auth/login'); 
        }
    } catch (error) {
        console.error("Error checking authentication status:", error);
        localStorage.removeItem("jwt"); 
        window.location.replace('/auth/login');
    }
}

// Run storeToken() when the page loads
document.addEventListener("DOMContentLoaded", storeToken);
