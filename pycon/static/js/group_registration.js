var GROUP_REGISTRATION_URL = (function() {
    var scripts = $('script');
    var current = $(scripts[scripts.length - 1]);
    return current.data('registrationUrl');
})();

/* Adds another group registration form to the page. */
var addLine = function() {
  var form = $('<form />').addClass('group-registration form-inline').append(
    $('<input>').addClass('form-control').attr({
      type: 'text',
      name: 'first_name',
      placeholder: 'First name'
    }),
    $('<input>').addClass('form-control').attr({
      type: 'text',
      name: 'last_name',
      placeholder: 'Last name'
    }),
    $('<input>').addClass('form-control').attr({
      type: 'email',
      name: 'email',
      placeholder: 'Email'
    }),
    $('<span>').addClass('btn btn-mini btn-default remove-line').attr({
      title: 'Remove line'
    }).html('&times;')
  );
  $('#group-registrations').append(form);
}

/* Serialize data from a group registration form as a dictionary. */
var getDataDictionary = function(form) {
  return {
    first_name: form.find('[name=first_name]').val(),
    last_name: form.find('[name=last_name]').val(),
    email: form.find('[name=email]').val(),
  }
}

/* Add a form-nonspecific message to the page. */
var addAlert = function(message) {
    button = $('<button>').addClass('close').html('&times;')
    button.attr({'type': 'button', 'data-dismiss': 'alert'});
    msg = $('<div>').addClass('alert group-registration-message fade in alert-error');
    msg.html(message);
    msg.prepend(button);
    $('#user-messages').append(msg);
}

/* Add the given error message above the form. */
var addError = function(form, message) {
  var container = $('<div>').addClass("help-block text-error").html(message);
  form.prepend(container);
}

/* Remove all error messages from the page. */
var clearErrors = function() {
  $('.group-registration .help-block.text-error').remove();
  $('#user-messages .group-registration-message').remove();
}

$(function() {
  $('#add-line').click(function(e) {
    addLine();
  });
  $('#group-registrations').delegate('.group-registration', 'submit', function(e) {
    e.preventDefault();
  });
  $('#group-registrations').delegate('.remove-line', 'click', function(e) {
    $(this).closest('form').remove();
  });
  $('#submit-registrations').click(function(e) {
    clearErrors();
    var valid = true;
    var dataToSubmit = [];

    // Perform basic error checking on each form.
    var forms = $('.group-registration');
    forms.each(function(i, form) {
      var form = $(form);
      var data = getDataDictionary(form);
      if ((data.first_name || data.last_name) && !data.email) {
        addError(form, "Email address is required.");
        valid = false;  // Continue going through forms to find other errors.
      } else if (data.email) {
        dataToSubmit.push(data);
      } else {
        // Remove empty forms.
        form.remove();
      }
    });

    // If _all_ forms are valid, submit them to the server for processing.
    if (valid) {
      if (!dataToSubmit.length) {
        alert("There are no forms to submit!");
      } else {
        $.ajax({
          type: "POST",
          url: GROUP_REGISTRATION_URL,
          data: JSON.stringify(dataToSubmit),
          dataType: "json"
        }).done(function(data, status, xhr) {
          if (data.success) {
            var table = $('<table>');
            table.append($('<thead><th>Name</th><th>Email</th><th>pycon_id</th><th></th></thead>'));
            $.each(data.users, function(i, user) {
              var tr = $('<tr>');
              tr.append($('<td>').html(user.user.first_name + ' ' + user.user.last_name));
              tr.append($('<td>').html(user.user.email));
              tr.append($('<td>').html(user.user.pycon_id));
              tr.append($('<td>'));
              table.find('tbody').append(tr);
            });
            $('#group-registrations-container').html(table);
          } else {
            $.each(data.users, function(i, user) {
              // Show errors for each form.
              if (!user.success) {
                  var form = $($('#group-registrations form')[i]);
                  addError(form, user.error_message);
              }
            });
          }
        }).fail(function(xhr, status, error) {
          addAlert("A problem occurred while submitting the registration. " +
                   "Please refresh the page and try again. " +
                   "If the problem persists, please contact a PyCon administrator.");
        });
      }
    } else {
      addAlert("We spotted a problem - please fix errors and try again.");
    }
  });
});
