$(function () {
  /* which controls determine which other controls are visible */
  var controls = {
    'input#id_hotel_grant_requested': 'div#div_id_hotel_nights,div#div_id_sex',
    'input#id_travel_grant_requested': 'div#div_id_international,div#div_id_travel_amount_requested,div#div_id_travel_plans'
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

  /* If someone requests a PyLadies grant, and the hotel sex field has
  not been set yet, change it to Female.
   */
  $('input#id_pyladies_grant_requested').on('change', function() {
    if ($(this).val() === 'on') {
      var $sex = $('select#id_sex');
      var val = $sex.val();
      if ((val === '0') || (val === '')) {
        $sex.val('1');  // Female
      }
    }
  });
});
