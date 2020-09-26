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

// Function to make AJAX call to update checkbox
function updateCheckbox(teamId, checklistId, checkboxChecked){
    fetch(`/tasks/api/${teamId}/${checklistId}/update-checklist-item/`,
        {
            method: 'PATCH',
            mode: 'same-origin',
            body: JSON.stringify({completed: checkboxChecked}),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            }
        }
    ).then(response => response.json())
}

// Function to make AJAX call to update checkbox
function updateChecklistText(teamId, checklistId, newText){
    fetch(`/tasks/api/${teamId}/${checklistId}/update-checklist-item/`,
        {
            method: 'PATCH',
            mode: 'same-origin',
            body: JSON.stringify({item: newText}),
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
        // Loop through checklist items
        for (let item of data) {
            // Create a div container for each checklist item
            let newDiv =  document.createElement('div');
            newDiv.id = 'checklist-item-' + item.id;
            // Create checkbox element, add data, append to div container
            let newCheckbox = document.createElement('input');
            newCheckbox.type = 'checkbox';
            newCheckbox.id = 'checkbox-' + item.id;
            newCheckbox.name = 'checkbox-' + item.id;
            newCheckbox.checked = item.completed;
            // Add event listener to update database when checkbox changes
            newCheckbox.addEventListener('change', function() {
                updateCheckbox(teamId, item.id, this.checked);
            });
            newDiv.appendChild(newCheckbox);
            let newSpan = document.createElement('span');
            // Create label for checkbox
            let newLabel = document.createElement('label');
            newLabel.htmlFor = 'checkbox-' + item.id;
            newLabel.innerText = item.item;
            newLabel.className = 'checklist-item';
            newSpan.appendChild(newLabel);
            newLabel.addEventListener('click', function() {
                newSpan.innerText = "";
                let newTextInput = document.createElement('input');
                newTextInput.type = 'text';
                newTextInput.value = item.item;
                newTextInput.name = 'checklist-item-' + item.id;
                newSpan.appendChild(newTextInput);
                let newBtn = document.createElement('button');
                newBtn.innerText = "Update";
                newBtn.className = "btn btn-info btn-sm";
                newSpan.appendChild(newBtn);
                newBtn.addEventListener('click', async function() {
                    await updateChecklistText(teamId, item.id, newTextInput.value);
                    await readChecklistItems(teamId, taskId);
                })
            })
            newDiv.appendChild(newSpan);
            // Append div container to parent container
            parentElement.appendChild(newDiv);
        }
    })
}

document.querySelector('#add-checklist-item-btn').addEventListener('click', async () => {
    await createChecklistItem(teamId, taskId);
    await readChecklistItems(teamId, taskId);
});

readChecklistItems(teamId, taskId);
