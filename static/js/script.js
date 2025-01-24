const addUrlButton = document.getElementById("add-url-btn");
const removeUrlButton = document.getElementById("remove-url-btn");
const startProcessingButton = document.getElementById("start-processing-btn");
const viewUrlsButton = document.getElementById("view-urls-btn");
const responseMessage = document.getElementById("response-message");
const urlsList = document.getElementById("urls");

const API_BASE_URL = "/"; // Flask backend URL (relative path)

function showMessage(message, success=true) {
    responseMessage.className = 'message ' + (success ? 'success' : 'error');
    responseMessage.textContent = message;
}

// Fetch current URLs from Redis
async function fetchUrls() {
    const response = await fetch(`${API_BASE_URL}get-urls`);
    const data = await response.json();
    urlsList.innerHTML = '';  // Clear the current list
    if (Object.keys(data).length === 0) {
        urlsList.innerHTML = '<li class="list-group-item">No URLs in the queue.</li>';
    } else {
        for (const streamName in data) {
            const url = data[streamName];
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            listItem.textContent = `${streamName}: ${url}`;
            urlsList.appendChild(listItem);
        }
    }
}

addUrlButton.addEventListener("click", async () => {
    const url = document.getElementById("url").value;
    const stream_name = document.getElementById("stream_name").value;
    if (!url || !stream_name) {
        showMessage("URL and Stream name are required!", false);
        return;
    }

    const response = await fetch(`${API_BASE_URL}add-url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, stream_name })
    });

    const result = await response.json();
    showMessage(result.message, response.ok);
    fetchUrls();  // Update the URL list after adding a new one
});

removeUrlButton.addEventListener("click", async () => {
    const stream_name = document.getElementById("stream_name").value;
    if (!stream_name) {
        showMessage("Stream name is required!", false);
        return;
    }

    const response = await fetch(`${API_BASE_URL}remove-url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stream_name })
    });

    const result = await response.json();
    showMessage(result.message, response.ok);
    fetchUrls();  // Update the URL list after removing one
});

startProcessingButton.addEventListener("click", async () => {
    const response = await fetch(`${API_BASE_URL}start-processing`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });

    const result = await response.json();
    showMessage(result.message, response.ok);
});

viewUrlsButton.addEventListener("click", fetchUrls);  // Button to fetch and display current URLs

// Initial fetch to display the current URLs when the page loads
window.onload = fetchUrls;
