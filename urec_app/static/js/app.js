// classList - shows/gets all classes
// contains - checks classList for specific class
// add - add class
// remove - remove class
// toggle - toggles class

//for hamburger toggle when smaller screen
const navToggle = document.querySelector('.nav-toggle');
const navItemsToggle = document.querySelector('.nav-items-toggle');

navToggle.addEventListener('click', function() {
    navItemsToggle.classList.toggle('nav-items-toggle-show');
})

//changes bar icon to an X icon
let changeIcon = function(icon){
    console.log('hello');
    icon.classList.toggle('fa-times');
}