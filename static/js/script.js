const draggableElements = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.task-bucket')

draggableElements.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        console.log("Start dragging")
        draggable.classList.add('dragging')
    })

    draggable.addEventListener('dragend', () => {
        console.log("End dragging")
        draggable.classList.remove('dragging')
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')
        if (afterElement == null) {
            container.appendChild(draggable)
        } else {
            container.insertBefore(draggable, afterElement)
        }
    })
})

function getDragAfterElement(container, y) {
    const targetElements = [...container.querySelectorAll('.draggable:not(.dragging)')]

    return targetElements.reduce((closest, target) => {
        const box = target.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: target }
        } else {
            return closest
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element
}