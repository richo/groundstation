groundstation.validators.gref = (function() {
  func = function(name, title, body) {
    return func.valid_name_p(name) &&
           func.valid_title_p(title) &&
           func.valid_body_p(body);
  };
  return function(d_name, d_title, d_body) {
    func.valid_name_p = function(name) {
      if ((typeof name) !== 'string')
        return false;
      if (name.length === 0)
        return false;
      if (name === d_name)
        return false;
      if (name.indexOf(" ") >= 0)
        return false;
      return true;
    };
    func.valid_title_p = function(title) {
      if ((typeof title) !== 'string')
        return false;
      if (title.length === 0)
        return false;
      if (title === d_title)
        return false;
      // TODO
      return true;
    };
    func.valid_body_p = function(body) {
      if ((typeof body) !== 'string')
        return false;
      if (body.length === 0)
        return false;
      if (body === d_body)
        return false;
      // TODO
      return true;
    };
    return func;
  };
})();
