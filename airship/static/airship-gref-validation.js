groundstation.validators.gref = (function() {
  func = function(name, title, body) {
    return func.valid_name_p(name) &&
           func.valid_title_p(title) &&
           func.valid_body_p(body);
  };
  func.valid_name_p = function(name) {
    if (name.indexOf(" ") >= 0)
      return false;
    return true;
  };
  func.valid_title_p = function(title) {
    // TODO
    return true;
  };
  func.valid_body_p = function(body) {
    // TODO
    return true;
  };
  return func;
})();
