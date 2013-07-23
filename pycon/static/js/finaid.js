$(function () {
  /* which controls determine which other controls are visible */
  var controls = {
    'input#id_hotel_grant_requested': 'div#div_id_hotel_nights,div#div_id_sex',
    'input#id_travel_grant_requested': 'div#div_id_international,div#div_id_travel_amount_requested,div#div_id_travel_plans',
    'input#id_tutorial_grant_requested': 'div#div_id_tutorial_1,div#div_id_tutorial_2,div#div_id_tutorial_3,div#div_id_tutorial_4'
  };

  /* Function to update visibility when triggers change */
  var update_visibility = function () {
    var trigger;
    for (trigger in controls) {
      var $affected = $(controls[trigger]);
      var checked_ones = $(trigger + ':checked');
      if ($(trigger + ':checked').length) {
        $affected.show();
      } else {
        $affected.hide();
      }
    }
  };

  /* Run update function when any of the controls changes value */
  for (trigger in controls) {
    $(trigger).change(update_visibility);
  }

  /* initialize visibility */
  update_visibility();
});
