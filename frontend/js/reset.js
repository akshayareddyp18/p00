document.getElementById("reset-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = document.getElementById("reset-email").value;
    await authRequest("reset-password", { email });
});
