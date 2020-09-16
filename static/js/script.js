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

// Function to make AJAX call to update a task's stage_id
function updateTaskStage(team_id, task_id, new_stage_id){
    fetch(`/tasks/api/${team_id}/${task_id}/update-task-stage/`,
    {
        method: 'PATCH',
        mode: 'same-origin',
        body: JSON.stringify({stage: `${new_stage_id}`}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        }
    }).then(response => response.json())
    .then(json => console.log(json))
}

const draggableElements = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.task-container')

draggableElements.forEach(draggable => {
    // Start dragging element
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging');
        // Remove old stage-id from draggable's class list
        draggable.classList.remove(draggable.parentElement.id);
    })
    // End dragging element
    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging');
        // Add new stage-id to draggable's class list
        containerId = draggable.parentElement.id;
        draggable.classList.add(containerId);
        // Get team-id from URL
        teamId = window.location.pathname.split('/')[2]
        // Update database with new stage-id
        updateTaskStage(teamId, draggable.id.replace(/^task-+/i, ''), containerId.replace(/^stage-+/i, ''))
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault();
        const afterElement = getDragAfterElement(container, e.clientY);
        const draggable = document.querySelector('.dragging');
        if (afterElement == null) {
            container.appendChild(draggable);
        } else {
            container.insertBefore(draggable, afterElement);
        }
    })
})

function getDragAfterElement(container, y) {
    const targetElements = [...container.querySelectorAll('.draggable:not(.dragging)')]

    return targetElements.reduce((closest, target) => {
        const box = target.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: target }
        } else {
            return closest
        }
    }, {
        offset: Number.NEGATIVE_INFINITY }).element
}


// async function getAPI() {
//     let response = await axios.get("/tasks/vanilla/api/get/");
//     console.log(response.data);
// }

// async function postAPI() {
//     let response = await axios.post("/tasks/vanilla/api/post/");
//     console.log(response.data);
// }

