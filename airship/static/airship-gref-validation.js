groundstation.validators.gref = function(name, title, body) {
  if (name.indexOf(" ") >= 0)
    return false;
  return true;
};
