

    // 🔔 Open/Close Notification Popup
    function openNotificationPopup() {
        document.getElementById("notification-popup").style.display = "flex";
    }
    
    function closeNotificationPopup() {
        document.getElementById("notification-popup").style.display = "none";
    }
    
    // 🔔 Send Notification
    function sendNotification() {
        const internId = document.getElementById("notify-intern").value;
        const message = document.getElementById("notify-message").value;
        const statusElement = document.getElementById("notification-status");
    
        if (!internId || !message) {
            statusElement.innerText = "Please fill all fields!";
            statusElement.style.color = "red";
            return;
        }
    
        fetch("{% url 'send_notification' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: JSON.stringify({ intern_id: internId, message: message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusElement.innerText = data.success;
                statusElement.style.color = "green";
                document.getElementById("notify-message").value = "";
            } else {
                statusElement.innerText = data.error;
                statusElement.style.color = "red";
            }
        })
        .catch(error => {
            statusElement.innerText = "Error sending notification!";
            statusElement.style.color = "red";
        });
    }
    

    
    // 📢 Open/Close Announcement Form
    document.getElementById("open-announcement-form-btn").addEventListener("click", function() {
        document.getElementById("announcement-popup").style.display = "block";
    });
    
    document.getElementById("close-announcement-form-btn").addEventListener("click", function() {
        document.getElementById("announcement-popup").style.display = "none";
    });
    
    // 📢 Submit Announcement
    document.getElementById("announcement-form").addEventListener("submit", function(event) {
        event.preventDefault();
    
        const formData = new FormData(this);
    
        fetch("{% url 'add_announcement' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("announcement-response-message").innerText = data.success || data.error;
            if (data.success) {
                this.reset();
                setTimeout(() => {
                    document.getElementById("announcement-popup").style.display = "none";
                }, 1000);
            }
        })
        .catch(error => console.error("Error:", error));
    });
    

    
    // 📅 Add Meeting
    document.getElementById("meeting-form").addEventListener("submit", function(event) {
        event.preventDefault();
    
        const title = document.getElementById("meeting-title").value.trim();
        const description = document.getElementById("meeting-description").value.trim();
        const date = document.getElementById("meeting-date").value;
        const location = document.getElementById("meeting-location").value.trim();
    
        if (!title || !date) {
            alert("Meeting title and date/time are required!");
            return;
        }
    
        fetch("{% url 'add_meeting' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: JSON.stringify({
                title: title,
                description: description,
                date: date,
                location: location,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Meeting added successfully!");
                this.reset();
                location.reload();
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            alert("An error occurred while adding the meeting.");
        });
    });
    

    
    // 📝 Add/Edit Practice Session
    function submitSession() {
        const session_id = document.getElementById("session_id").value;
        const title = document.getElementById("session-title").value;
        const description = document.getElementById("session-description").value;
        const date = document.getElementById("session-date").value;
        const location = document.getElementById("session-location").value;
        const meeting_link = document.getElementById("session-link").value;
    
        const url = session_id 
            ? `/elementishead/edit-session/${session_id}/`
            : `/elementishead/add-practice-session/`;
    
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}&date=${encodeURIComponent(date)}&location=${encodeURIComponent(location)}&meeting_link=${encodeURIComponent(meeting_link)}`,
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("session-response-message").innerText = data.success || data.error;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
    