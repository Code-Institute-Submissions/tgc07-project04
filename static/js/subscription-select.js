const serviceElement1 = document.getElementById('service-1');
const serviceElement2 = document.getElementById('service-2');
const serviceContainer1 = document.getElementById('service-1-container');
const serviceContainer2 = document.getElementById('service-2-container');

serviceContainer1.addEventListener('click', () => {
    serviceElement1.checked = true;
    serviceContainer1.classList.add('service-selected');
    serviceContainer2.classList.remove('service-selected');
});

serviceContainer2.addEventListener('click', () => {
    serviceElement2.checked = true;
    serviceContainer2.classList.add('service-selected');
    serviceContainer1.classList.remove('service-selected');
});
