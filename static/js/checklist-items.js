const teamId = document.querySelector('#task-id').name;
const taskId = document.querySelector('#task-id').value;
const progressBar = document.querySelector('.progress-bar');
const progressBarSpan = document.querySelector('.progress-bar-text');

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

// Function to make AJAX call to get checklist items count and checked items count
function displayChecklistItemsProgress(teamId, taskId){
    fetch(`/tasks/api/${teamId}/${taskId}/count-checklist-items/`,
        {
            method: 'GET',
            mode: 'same-origin',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }
    ).then(response => response.json()
    ).then(data => {
        percentageComplete = Math.floor(data.checked_items_count/data.items_count*100);
        progressBar.style.width = `${percentageComplete}%`;
        progressBar.setAttribute('aria-valuenow', percentageComplete);
        progressBarSpan.innerText = `${data.checked_items_count}/${data.items_count}`;
    })
}

// Function to make AJAX call to create checklist item
function createChecklistItem(teamId, taskId){
    let checklistItemInput = document.querySelector('#add-checklist-item-input');
    fetch(`/tasks/api/${teamId}/${taskId}/create-checklist-item/`,
        {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({item: checklistItemInput.value.slice(0,50)}),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            }
        }
    ).then(response => response.json()
    ).then( () => {
        // Reset input field value at end
        checklistItemInput.value = "";
    }).then( () => {
        // Get checked items count and display progress
        displayChecklistItemsProgress(teamId, taskId);
    })
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
    ).then(response => response.json()
    ).then( () => {
        // Get checked items count and display progress
        displayChecklistItemsProgress(teamId, taskId);
    })
}

// Function to make AJAX call to update checklist item
function updateChecklistText(teamId, checklistId, newText){
    fetch(`/tasks/api/${teamId}/${checklistId}/update-checklist-item/`,
        {
            method: 'PATCH',
            mode: 'same-origin',
            body: JSON.stringify({item: newText.slice(0,50)}),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            }
        }
    ).then(response => response.json())
}

// Function to make AJAX call to delete checklist item
function deleteChecklistItem(teamId, checklistId){
    fetch(`/tasks/api/${teamId}/${checklistId}/delete-checklist-item/`,
        {
            method: 'DELETE',
            mode: 'same-origin',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            }
        }
    ).then(response => response.json()
    ).then( () => {
        // Get checked items count and display progress
        displayChecklistItemsProgress(teamId, taskId);
    })
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
            // Create a <tr> element container for each checklist item
            let newTr =  document.createElement('tr');
            newTr.id = 'checklist-item-' + item.id;

            // Create checkbox element, append to container
            let newTdCheckbox = document.createElement('td');
            let newCheckbox = document.createElement('input');
            newCheckbox.type = 'checkbox';
            newCheckbox.id = 'checkbox-' + item.id;
            newCheckbox.name = 'checkbox-' + item.id;
            newCheckbox.checked = item.completed;
            // Add event listener to update database when checkbox changes
            newCheckbox.addEventListener('change', function() {
                updateCheckbox(teamId, item.id, this.checked);
            });
            newTdCheckbox.appendChild(newCheckbox);
            newTr.appendChild(newTdCheckbox);

            // Create label for checkbox
            let newTdLabel = document.createElement('td');
            let newLabel = document.createElement('label');
            newLabel.htmlFor = 'checkbox-' + item.id;
            newLabel.innerText = item.item;
            newLabel.className = 'checklist-item';
            newTdLabel.appendChild(newLabel);
            // When label is clicked, change element to text input so user can update checklist item
            newLabel.addEventListener('click', function() {
                newTdLabel.innerText = "";
                let newTextInput = document.createElement('input');
                newTextInput.type = 'text';
                newTextInput.value = item.item;
                newTextInput.name = 'checklist-item-' + item.id;
                newTextInput.className = 'checklist-text-input mr-2 pl-2';
                newTdLabel.appendChild(newTextInput);
                let updateBtn = document.createElement('button');
                updateBtn.innerText = "Update";
                updateBtn.className = "btn btn-info btn-sm";
                updateBtn.addEventListener('click', async function() {
                    await updateChecklistText(teamId, item.id, newTextInput.value);
                    setTimeout( function() {
                        readChecklistItems(teamId, taskId);
                    }, 500);
                });
                newTdLabel.appendChild(updateBtn);
            });
            newTr.appendChild(newTdLabel);

            // Create delete button for checklist item
            let newTdDelete = document.createElement('td');
            let deleteBtn = document.createElement('button');
            deleteBtn.innerText = "Delete";
            deleteBtn.className = "btn btn-secondary btn-sm";
            deleteBtn.addEventListener('click', async () => {
                await deleteChecklistItem(teamId, item.id);
                setTimeout( function() {
                    readChecklistItems(teamId, taskId);
                }, 500);
            });
            newTdDelete.appendChild(deleteBtn);
            newTr.appendChild(newTdDelete);

            // Append div container to parent container
            parentElement.appendChild(newTr);
        }
    })
}

// Wait until page loads
window.addEventListener('load', () => {
    // Add event listener to create checklist item button to activate AJAX call
    document.querySelector('#add-checklist-item-btn').addEventListener('click', async () => {
        await createChecklistItem(teamId, taskId);
        setTimeout( function() {
            readChecklistItems(teamId, taskId);
        }, 500);
    });
    
    // Get all checklist items belogning to task
    readChecklistItems(teamId, taskId);
    // Get checked items count and display progress
    displayChecklistItemsProgress(teamId, taskId);

});