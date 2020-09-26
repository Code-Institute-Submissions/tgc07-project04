let teamId = document.querySelector('#task-id').name;
let taskId = document.querySelector('#task-id').value;

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
function createChecklistItem(teamId, taskId){
    let checklistItemInput = document.querySelector('#add-checklist-item-input');
    fetch(`/tasks/api/${teamId}/${taskId}/create-checklist-item/`,
        {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({item: checklistItemInput.value}),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            }
        }
    ).then(response => response.json())
}

// Function to make AJAX call to get all checklist items belonging to taskId
function readChecklistItems(teamId, taskId){
    let parentElement = document.querySelector('#checklist-items-container')
    parentElement.innerText = "";
    fetch(`/tasks/api/${teamId}/${taskId}/read-checklist-items/`,
        {
            method: 'GET',
            mode: 'same-origin',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }
    ).then(response => response.json()
    ).then(data => {
        for (let item of data) {
            let newDiv =  document.createElement('div');
            newDiv.id = 'checklist-item-' + item.id;
            let newCheckbox = document.createElement('input');
            newCheckbox.type = 'checkbox';
            newCheckbox.id = 'checkbox-' + item.id;
            newCheckbox.name = item.id;
            newCheckbox.checked = item.completed;
            newCheckbox.addEventListener('change', function() {
                console.log(this)
            })
            newDiv.appendChild(newCheckbox);
            let newLabel = document.createElement('label');
            newLabel.htmlFor = 'checklist-item-' + item.id;
            newLabel.innerText = item.item;
            newDiv.appendChild(newLabel);
            parentElement.appendChild(newDiv);
        }
    })
}

document.querySelector('#add-checklist-item-btn').addEventListener('click', async () => {
    await createChecklistItem(teamId, taskId);
    await readChecklistItems(teamId, taskId);
});

readChecklistItems(teamId, taskId);
