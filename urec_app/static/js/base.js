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
    icon.classList.toggle('fa-times');
}


/*

Section for jquery data table implementation

*/
//view most recent count history
  $(document).ready( function () {
    $('#recent_counts').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

//view all count history
$(document).ready( function () {
    $('#all_counts').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

// view hourly count (May not be used)
$(document).ready( function () {
    $('#hourly_counts').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

// view accident tickets
$(document).ready( function () {
    $('#accident_ticket_info').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

// view accident tickets
$(document).ready( function () {
    $('#accident_ticket_injury').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

// view accident tickets
$(document).ready( function () {
    $('#accident_ticket_contact').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

// view incident tickets
$(document).ready( function () {
    $('#incident_ticket_info').DataTable({
        responsive: true,
        "scrollX": true,
    });
} );

