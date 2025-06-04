function openEditMeetingModal(id, title, description, date, location) {
    document.getElementById("editMeetingId").value = id;
    document.getElementById("editMeetingTitle").value = title;
    document.getElementById("editMeetingDescription").value = description;
    document.getElementById("editMeetingDate").value = date;
    document.getElementById("editMeetingLocation").value = location;
    document.getElementById("editMeetingModal").style.display = "flex";
}

function closeEditMeetingModal() {
    document.getElementById("editMeetingModal").style.display = "none";
}

document.getElementById("editMeetingForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const id = document.getElementById("editMeetingId").value;
    const title = document.getElementById("editMeetingTitle").value;
    const description = document.getElementById("editMeetingDescription").value;
    const date = document.getElementById("editMeetingDate").value;
    const location = document.getElementById("editMeetingLocation").value;

    fetch(`/elementishead/edit-meeting/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}&date=${encodeURIComponent(date)}&location=${encodeURIComponent(location)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Meeting updated!");
            window.location.reload();

        } else {
            alert("Error updating meeting!");
        }
    })
    .catch(error => console.error('Error:', error));
});

function deleteMeeting(id) {
    if (confirm("Are you sure you want to delete this meeting?")) {
        fetch(`/elementishead/delete-meeting/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Meeting deleted successfully!");
                window.location.reload();

            } else {
                alert("Error deleting meeting!");
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function deleteAnnouncement(id) {
    if (confirm("Are you sure you want to delete this announcement?")) {
        fetch(`/elementishead/delete-announcement/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Announcement deleted successfully!");
                window.location.reload();

            } else {
                alert("Error deleting announcement!");
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function deletePracticeSession(id) {
    if (confirm("🗑️ Are you sure you want to delete this practice session?")) {
        fetch(`/elementishead/delete-practice-session/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("✅ Practice Session deleted successfully!");
                window.location.reload();
            } else {
                alert("❌ Error deleting practice session!");
            }
        })
        .catch(error => console.error('Error:', error));

    }
}