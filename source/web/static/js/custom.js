import "jquery-3.5.1.min.js";

$('.sortable-list').sortable({
  connectWith: '.sortable-list',
  update: function(event, ui) {
    var changedList = this.id;
    var order = $(this).sortable('toArray');
    var positions = order.join(';');

    console.log({
      id: changedList,
      positions: positions
    });
  }
});