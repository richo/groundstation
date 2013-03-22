var fs = require("fs");
var assert = require("assert");
var groundstation = {
  "validators": {}
};

// Oh yes.
eval(fs.readFileSync("static/airship-gref-validation.js", {encoding: 'utf8'}));

describe('groundstation.validators.gref', function(){
  it('should return false if spaces in name', function(){
    assert.equal(false, groundstation.validators.gref("butts lol", "oktitle", "okbody"));
  });
});
