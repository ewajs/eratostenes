keyUpEventWhenFocus("email", validateEmailListener);
keyUpEventWhenFocus("password", validatePasswordListener);
keyUpEventWhenFocus("password_verify", validatePasswordVerifyListener);

function keyUpEventWhenFocus(elementId, keyUpEventListener) {
  let element = document.getElementById(elementId);
  element.addEventListener("focus", function () {
    element.addEventListener("keyup", function (event) {
      keyUpEventListener(event);
      updateSubmit();
    });
  });
}

function validateEmailListener(event) {
  if (validateEmail(event.target.value)) {
    event.target.classList.remove("is-invalid");
    event.target.classList.add("is-valid");
  } else {
    event.target.classList.remove("is-valid");
    event.target.classList.add("is-invalid");
  }
}

function validatePasswordListener(event) {
  if (event.target.value.length > 6) {
    event.target.classList.remove("is-invalid");
    event.target.classList.add("is-valid");
  } else {
    event.target.classList.remove("is-valid");
    event.target.classList.add("is-invalid");
  }
  let verify = document.getElementById("password_verify");
  if (event.target.value != verify.value) {
    verify.classList.remove("is-valid");
    verify.classList.add("is-invalid");
  } else {
    verify.classList.remove("is-invalid");
    verify.classList.add("is-valid");
  }
}

function validatePasswordVerifyListener(event) {
  console.log("triggered");
  if (event.target.value == document.getElementById("password").value) {
    event.target.classList.remove("is-invalid");
    event.target.classList.add("is-valid");
  } else {
    event.target.classList.remove("is-valid");
    event.target.classList.add("is-invalid");
  }
}

function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function updateSubmit() {
  let email = document.getElementById("email");
  let submit = document.getElementById("submit");
  submit.disabled = !(
    validateEmail(email.value) &&
    document.getElementById("password").value ==
      document.getElementById("password_verify").value
  );
}
