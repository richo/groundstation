var fs = require("fs");
var assert = require("assert");
var groundstation = {
  "validators": {}
};

// Oh yes.
eval(fs.readFileSync("static/airship-gref-validation.js").toString());

describe('groundstation.validators.gref', function(){
  describe('name', function(){
    var validator = groundstation.validators.gref.valid_name_p;
    it('should return false for non strings', function(){
      assert.equal(false, validator(123));
    });
    it('should return false if spaces in name', function(){
      assert.equal(false, validator("butts lol"));
    });
    it('should return true for short valid names', function(){
      assert.equal(true, validator("buttslol"));
    });
  });
  describe('title', function(){
    var validator = groundstation.validators.gref.valid_title_p;
    it('should return false for non strings', function(){
      assert.equal(false, validator(123));
    });
  });
  describe('body', function(){
    var validator = groundstation.validators.gref.valid_body_p;
    it('should return false for non strings', function(){
      assert.equal(false, validator(123));
    });
  });
});
