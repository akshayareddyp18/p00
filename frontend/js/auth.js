document.getElementById("signup-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;
    const email = document.getElementById("signup-email").value;  // Get email
    await authRequest("signup", { username, password, email });
});



document.getElementById("login-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    await authRequest("login", { username, password });
});



document.getElementById("logout-btn")?.addEventListener("click", async (event) => {
    event.preventDefault();
    logout();
});

document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Get form values
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;
    const email = document.getElementById("signup-email").value;

    // Simulate saving user data (you would typically send this to a backend)
    const userData = { username, password, email };
    localStorage.setItem("user", JSON.stringify(userData)); // Store in localStorage for testing

    // Redirect to login page
    window.location.href = "login.html";
});


async function login() {

    localStorage.removeItem("token");
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });


    const data = await response.json();


    console.log("🔑 Received Data:", data); // Log full response


    if (response.ok && data.access_token) {

        localStorage.setItem("token", data.access_token);
        console.log("✅ Token Saved:", localStorage.getItem("token"));  // Confirm saving
        window.location.href = "index.html";
    } else {
        alert("Login failed: " + (data.error || "Unknown error"));
    }
}


async function authRequest(endpoint, body) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        const data = await response.json();

        if (endpoint === "login" && response.ok) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "index.html";  // Redirect on successful login
        }

        alert(data.message || data.error);
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred.");
    }
}
async function logout() {
    localStorage.removeItem("token");  // Remove JWT token
    alert("Logged out successfully.");
    window.location.href = "index.html";  // Redirect to homepage
}



/*

async function fetchProtected() {
    try {
        const response = await fetch("http://127.0.0.1:8000/protected", {
            method: "GET",
            credentials: "include"
        });

        const data = await response.json();
        alert(data.message || data.error);
    } catch (error) {
        console.error("Error fetching protected route:", error);
        alert("An error occurred.");
    }
}






async function fetchUserProfile() {
    try {
        const response = await fetch("http://127.0.0.1:8000/user-profile", {
            method: "GET",
            credentials: "include"
        });

        const data = await response.json();
        alert(data.username ? `Username: ${data.username}` : data.error);
    } catch (error) {
        console.error("Error fetching user profile:", error);
        alert("An error occurred.");
    }
}
*/

async function fetchUserProfile() {



    const token = localStorage.getItem("token");

    console.log("🚀 Sending token:", token); // Log before sending request


    if (!token) {


        console.error("🚨 No token found. Redirecting to login.");
        alert("You need to log in first!");
        window.location.href = "login.html";
        return;

    }



    console.log("🚀 Sending token:", token); // Debugging output


    const response = await fetch("http://127.0.0.1:8000/user-profile", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        }
    });

        const data = await response.json();
        console.log("🔍 Server Response:", data); // Log response
        


        if (response.ok) {
            alert(`Username: ${data.username}`);
            document.getElementById("user-info").innerText = `Hello, ${data.username}`;
       } else {


            console.error("❌ Error fetching profile:", data);
            alert("Failed to fetch Profile. Please log in again.");
            localStorage.removeItem("token");
            window.location.href = "login.html";
        }
}

//fetchUserProfile()

async function fetchProtected() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("You need to log in first!");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/protected", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // Attach JWT
            },
        });

        const data = await response.json();
        alert(data.message || data.error);
    } catch (error) {
        console.error("Error fetching protected route:", error);
        alert("An error occurred.");
    }
}


async function logout() {
    localStorage.removeItem("token"); // Remove JWT
    alert("Logged out successfully.");
    window.location.href = "index.html"; // Redirect after logout
}



/*
async function logout() {
    try {
        const response = await fetch("http://127.0.0.1:8000/logout", {
            method: "POST",
            credentials: "include" // Ensures cookies/sessions are handled
        });

        const data = await response.json();
        alert(data.message || data.error);

        if (response.ok) {
            window.location.href = "login.html"; // Redirect after logout
        }
    } catch (error) {
        console.error("Error during logout:", error);
        alert("An error occurred during logout.");
    }
}
*/
