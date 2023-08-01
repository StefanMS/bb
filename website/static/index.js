function deleteNote(noteId) {
    fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/";
    });
}

$(function() {
        setTimeout(function() { $("#flashingMessage").fadeOut(1000); }, 1000)
        
        })
