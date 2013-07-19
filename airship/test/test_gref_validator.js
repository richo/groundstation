var fs = require("fs");
var assert = require("assert");
var groundstation = {
  "validators": {}
};

// Oh yes.
eval(fs.readFileSync("static/airship-gref-validation.js").toString());

function alert(string) {
  // Noop
}

describe('groundstation.validators.gref', function(){
  var gref_validator = groundstation.validators.gref("defaultname", "defaulttitle", "defaultbody");
  describe('name', function(){
    var validator = gref_validator.valid_name_p;
    it('should return false for non strings', function(){
      assert.equal(false, validator(123));
    });
    it('should return false if spaces in name', function(){
      assert.equal(false, validator("butts lol"));
    });
    it ('should return false for empty strings', function(){
      assert.equal(false, validator(""));
    });
    it('should return true for short valid names', function(){
      assert.equal(true, validator("buttslol"));
    });
    it('should return false for the default name', function(){
      assert.equal(false, validator("defaultname"));
    });
  });
  describe('title', function(){
    var validator = gref_validator.valid_title_p;
    it('should return false for non strings', function(){
      assert.equal(false, validator(123));
    });
    it ('should return false for empty strings', function(){
      assert.equal(false, validator(""));
    });
    it('should return false for the default title', function(){
      assert.equal(false, validator("defaulttitle"));
    });
  });
  describe('body', function(){
    var validator = gref_validator.valid_body_p;
    it('should return false for non strings', function(){
      assert.equal(false, validator(123));
    });
    it ('should return false for empty strings', function(){
      assert.equal(false, validator(""));
    });
    it('should return false for the default body', function(){
      assert.equal(false, validator("defaultbody"));
    });
  });
});
