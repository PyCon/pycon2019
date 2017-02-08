var INITIAL_FORMS = 5;

/* Get the group registration URL off of the script tag. */
var GROUP_REGISTRATION_URL = (function() {
    var scripts = $('script');
    var current = $(scripts[scripts.length - 1]);
    return current.data('registrationUrl');
})();

/* Supply necessary CSRF credentials.
   https://docs.djangoproject.com/en/1.10/ref/csrf/#ajax */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});

/* Adds the specified number of registration forms to the page. */
var addRegistrationForms = function(count) {
  for (var i = 0; i < count; i ++) {
    var form = $('<form />').addClass('form-inline').append(
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
    $('#registrations').append(form);
  }
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
var addAlert = function(type, message) {
    button = $('<button>').addClass('close').html('&times;')
    button.attr({'type': 'button', 'data-dismiss': 'alert'});
    msg = $('<div>').addClass('alert fade in');
    msg.addClass('alert-' + type);
    msg.html(message);
    msg.prepend(button);
    $('#registration-messages').append(msg);
}

/* Add the given error message above the form. */
var addFormError = function(form, message) {
  var container = $('<div>').addClass("help-block text-error").html(message);
  form.prepend(container);
}

/* Remove all error messages and alerts from the page. */
var clearMessages = function() {
  $('#registrations form .help-block.text-error').remove();
  $('#registration-messages').html("");
}

/* Prevent the user from double-submitting by disabling the submit button. */
var disableSubmitButton = function() {
  var button = $('#submit-registrations');
  button.addClass('disabled').attr('disabled', '');
  button.html('Submitting...');
}

/* Re-enable ability for user to click the submit button. */
var enableSubmitButton = function() {
  var button = $('#submit-registrations');
  button.removeClass('disabled').removeAttr('disabled');
  button.html('Submit Registrations');
}

$(function() {
  $('#add-line').click(function(e) {
    addRegistrationForms(1);
  });
  $('#registrations').delegate('form', 'submit', function(e) {
    e.preventDefault();
  });
  $('#registrations').delegate('.remove-line', 'click', function(e) {
    $(this).closest('form').remove();
  });
  $('#submit-registrations').click(function(e) {
    clearMessages();

    var valid = true;
    var dataToSubmit = [];

    // Perform basic error checking on each form.
    var forms = $('#registrations form');
    forms.each(function(i, form) {
      var form = $(form);
      var data = getDataDictionary(form);
      if ((data.first_name || data.last_name) && !data.email) {
        addFormError(form, "Email address is required.");
        valid = false;  // Continue going through forms to find other errors.
      } else if (data.email) {
        dataToSubmit.push(data);
      } else {
        form.remove();  // Remove empty forms.
      }
    });

    // If _all_ forms are valid, submit them to the server for processing.
    if (valid) {
      if (!dataToSubmit.length) {
        addAlert("error", "There are no registrations to submit!");
        addRegistrationForms(INITIAL_FORMS);
      } else {
        disableSubmitButton();
        $.ajax({
          type: "POST",
          url: GROUP_REGISTRATION_URL,
          data: JSON.stringify(dataToSubmit),
          dataType: "json"
        }).done(function(data, status, xhr) {
          if (data.success) {
            var table = $('<table>');
            table.append($('<thead><th>Name</th><th>Email</th><th>pycon_id</th><th>Account status?</th></thead>'));
            table.append($('<tbody>'))
            $.each(data.users, function(i, user) {
              var tr = $('<tr>');
              var accountStatus = user.created ? "New account" : "Existing account";
              tr.append($('<td>').html(user.user.first_name + ' ' + user.user.last_name));
              tr.append($('<td>').html(user.user.email));
              tr.append($('<td>').html(user.user.pycon_id));
              tr.append($('<td>').html(accountStatus));
              table.find('tbody').append(tr);
            });
            $('#registrations-container').html(table);
            addAlert("success", "Thank you. PyCon accounts for individuals " +
                     "in this group have been created or retrieved. " +
                     "<a href='" + GROUP_REGISTRATION_URL +
                     "'>Register another group</a>")
          } else {
            $.each(data.users, function(i, user) {
              // Show errors for each form.
              if (!user.success) {
                var form = $($('#registrations form')[i]);
                $.each(user.errors, function(i, message) {
                  addFormError(form, message);
                });
              }
            });
            enableSubmitButton();
          }
        }).fail(function(xhr, status, error) {
          addAlert("error", "A problem occurred while submitting the registration. " +
                   "Please refresh the page and try again. " +
                   "If the problem persists, please contact a PyCon administrator.");
          enableSubmitButton();
        });
      }
    }
  });

  addRegistrationForms(INITIAL_FORMS);
});
