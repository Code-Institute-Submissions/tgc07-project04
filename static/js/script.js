// https://github.com/WebDevSimplified/Drag-And-Drop
const dragElements = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.task-container')

dragElements.forEach(d => {
    // Start dragging element
    d.addEventListener('dragstart', () => {
        d.classList.add('dragging');
        // Remove old stage-id from draggable's class list
        d.classList.remove(d.parentElement.id);
    })
    // End dragging element
    d.addEventListener('dragend', () => {
        d.classList.remove('dragging');
        // Add new stage-id to draggable's class list
        containerId = d.parentElement.id;
        d.classList.add(containerId);
    })
})

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

