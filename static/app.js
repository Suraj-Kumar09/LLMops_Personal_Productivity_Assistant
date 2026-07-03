async function askAssistant() {
    let queryInput = document.getElementById("query");
    let responseDiv = document.getElementById("response");
    let query = queryInput.value;

    // 1. Validation: Agar query khali hai
    if (!query || !query.trim()) {
        responseDiv.innerHTML = "<p style='color:orange;'>Please enter a question.</p>";
        return;
    }

    // 2. UI State: "Thinking..." dikhayein
    responseDiv.innerHTML = "<p>Thinking...</p>";

    try {
        // 3. API Call: Backend se connect karein
        let response = await fetch("/query", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json" 
            },
            body: JSON.stringify({ query: query })
        });

        let result = await response.json();

        // 4. Response Handling
        if (response.ok) {
            // Success: Response show karein
            responseDiv.innerHTML = `<p>${result.response}</p>`;
        } else {
            // Backend Error: Jo error backend se aa raha hai use display karein
            responseDiv.innerHTML = `<p style='color:red;'><strong>Error:</strong> ${result.error || "Something went wrong"}</p>`;
        }
    } catch (error) {
        // Network Error: Agar server hi down hai
        responseDiv.innerHTML = `<p style='color:red;'>Failed to connect to the server. Please ensure the backend is running.</p>`;
        console.error("Fetch Error:", error);
    }
}