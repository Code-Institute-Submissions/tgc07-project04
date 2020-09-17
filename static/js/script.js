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
}

// https://github.com/WebDevSimplified/Drag-And-Drop
const dragElements = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.task-container')

// https://github.com/WebDevSimplified/Drag-And-Drop
dragElements.forEach(d => {
    // State variable to track dragged task's current stage container
    let stageState = "";
    // Start dragging element
    d.addEventListener('dragstart', () => {
        d.classList.add('dragging');
        stageState = d.parentElement.id;
        // Remove old stage-id from draggable's class list
        d.classList.remove(d.parentElement.id);
    })
    // End dragging element
    d.addEventListener('dragend', () => {
        d.classList.remove('dragging');
        // Add new stage-id to draggable's class list
        containerId = d.parentElement.id;
        d.classList.add(containerId);
        // Check if user is_authenticated
        if (document.querySelector('#is_authenticated').value) {
            // Get team-id from URL
            teamId = document.querySelector('#is_authenticated').name;
            // If task changes container, update database with new stage-id and reset state variable
            if (d.parentElement.id!==stageState) {
                stageState = "";
                updateTaskStage(teamId, d.id.replace(/^task-+/i, ''), containerId.replace(/^stage-+/i, ''));
            } else {
                stageState = "";
            };
        };
    })
})

// https://github.com/WebDevSimplified/Drag-And-Drop
function getElementAfter(container, yPosition) {
    const targetElements = [...container.querySelectorAll('.draggable:not(.dragging)')]
    return targetElements.reduce((closest, target) => {
        const boundary = target.getBoundingClientRect();
        const offset = yPosition - boundary.top - boundary.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: target }
        } else {
            return closest
        }
    }, {
        offset: Number.NEGATIVE_INFINITY }).element
}

// https://github.com/WebDevSimplified/Drag-And-Drop
containers.forEach(container => {
    container.addEventListener('dragover', event => {
        event.preventDefault();
        const afterElement = getElementAfter(container, event.clientY);
        const d = document.querySelector('.dragging');
        if (afterElement == null) {
            container.appendChild(d);
        } else {
            container.insertBefore(d, afterElement);
        }
    })
})

