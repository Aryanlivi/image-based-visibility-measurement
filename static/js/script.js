// const addUrlButton = document.getElementById("add-url-btn");
const removeUrlButton = document.getElementById("remove-url-btn");
const startButton = document.getElementById("start-btn");
// const viewUrlsButton = document.getElementById("view-urls-btn");
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

// addUrlButton.addEventListener("click", async () => {
//     console.log("addsa")
//     const url = document.getElementById("url").value;
//     const stream_name = document.getElementById("stream_name").value;
//     if (!url || !stream_name) {
//         showMessage("URL and Stream name are required!", false);
//         return;
//     }

//     const response = await fetch(`${API_BASE_URL}add-url`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ url, stream_name})
//     });

//     const result = await response.json();
//     showMessage(result.message, response.ok);
//     fetchUrls()
//       // Update the URL list after adding a new one
// });

removeUrlButton.addEventListener("click", async () => {
    const stream_name = document.getElementById("stream_name_remove").value;
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
startButton.addEventListener("click", async () => {
    const url = document.getElementById("url").value;
    const stream_name = document.getElementById("stream_name").value;
    const device_id = document.getElementById("device_id").value;
    const devicecode = document.getElementById("devicecode").value;
    const album_code = document.getElementById("album_code").value;
    const latitude = document.getElementById("latitude").value;
    const longitude = document.getElementById("longitude").value;
    const altitude = document.getElementById("altitude").value;
    const imageowner = document.getElementById("imageowner").value;
    const firstAngle = document.getElementById("firstAngle").value;
    const lastAngle = document.getElementById("lastAngle").value;

    // Validate if all fields are provided
    const missingFields = [];
    if (!url) missingFields.push("url");
    if (!stream_name) missingFields.push("stream_name");
    if (!device_id) missingFields.push("device_id");
    if (!devicecode) missingFields.push("devicecode");
    if (!album_code) missingFields.push("album_code");
    if (!latitude) missingFields.push("latitude");
    if (!longitude) missingFields.push("longitude");
    if (!altitude) missingFields.push("altitude");
    if (!imageowner) missingFields.push("imageowner");
    if (!firstAngle) missingFields.push("firstAngle");
    if (!lastAngle) missingFields.push("lastAngle");

    // If there are missing fields, show an error message
    if (missingFields.length > 0) {
        showMessage(`Missing fields: ${missingFields.join(", ")}`, false);
        return; // Stop further execution
    }

    // If all fields are present, proceed with the fetch request
    const response = await fetch(`${API_BASE_URL}start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            url, stream_name, device_id, devicecode, album_code,
            latitude, longitude, altitude, imageowner, firstAngle, lastAngle
        })
    });

    const result = await response.json();
    showMessage(result.message, response.ok);
    fetchUrls();
});

// viewUrlsButton.addEventListener("click", fetchUrls);  // Button to fetch and display current URLs

// Initial fetch to display the current URLs when the page loads
window.onload = fetchUrls;
