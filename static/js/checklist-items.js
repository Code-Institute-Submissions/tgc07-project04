// https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Function to make AJAX call to create checklist item
function createChecklistItem(team_id, task_id){
    fetch(`/tasks/api/${team_id}/${task_id}/create-checklist-item/`,
    {
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({item: document.querySelector('#add-checklist-item-input').value}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        }
    }).then(response => response.json())
}
