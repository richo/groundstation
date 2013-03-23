var fs = require("fs");
var assert = require("assert");
var groundstation = {
  "validators": {}
};

// Oh yes.
eval(fs.readFileSync("static/airship-gref-validation.js").toString());

describe('groundstation.validators.gref', function(){
  it('should return false if spaces in name', function(){
    assert.equal(false, groundstation.validators.gref.valid_name_p("butts lol"));
  });
  it('should return true for short valid names', function(){
    assert.equal(true, groundstation.validators.gref.valid_name_p("buttslol"));
  });
});
