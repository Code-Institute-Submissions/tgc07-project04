const draggableElements = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.task-container')

draggableElements.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging');
        console.log("Start dragging");
        draggable.classList.remove(draggable.parentElement.id);
    })

    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging');
        console.log("End dragging");
        draggable.classList.add(draggable.parentElement.id);
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


async function getAPI() {
    let response = await axios.get("/tasks/vanilla/api/get/");
    console.log(response.data);
}

async function postAPI() {
    let response = await axios.post("/tasks/vanilla/api/post/");
    console.log(response.data);
}
