document.addEventListener("click", function (event) {
    console.log("Event detected on:", event.target); 

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
        window.location.href = "/logout";
    }
});

window.addEventListener("click", (event) => {
    let dropdown = document.getElementById("profile_dropdown");

    if (!event.target.closest("#account") && dropdown.style.opacity === "1") {
        dropdown.style.opacity = "0";
        dropdown.style.visibility = "hidden";
    }
});
