"use strict";



// function toggleEdits(e) {
//     $('#edit-fields').toggle();
//     $('#toggleEditButton').toggle();
// }


// function toggleEdits(e) {
//     $("#toggleEditButton").css({display: none});
// },{
//     $("#toggleEditButton").css({display: block});
// };

// $("#toggleEditButton").toggle(function() {
//   $('#edit-fields').show()
// }, function() {
//   $("edit-fields").hide()
// });

$('#edit-fields').hide();

function toggleEdits(e) {
   $('#edit-fields').show();
   $('#current-details').hide(); 
}
