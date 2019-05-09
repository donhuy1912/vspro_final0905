
function validateForm(){  
    var isValid = true;
    var requiredFields = $("input[class*='required']");
    for(var i=0; i<requiredFields.length;++i){
        var item = $(requiredFields[i]);
        isValid &= showErrorForRequired(item);
    }
    return isValid;
}

function showErrorForRequired(item){
    if($(item).val() != ""){
        $(item).closest("div").removeClass("has-error");
        $(item).siblings("span[class*='error']").hide();
        $("#btnSubmit").prop("disabled",false);
        return true;
    }
    else{
        $(item).closest("div").addClass("has-error");
        $(item).siblings("span[class*='error']").show();
        $("#btnSubmit").prop("disabled",true);
        return false;
    }
}

function checkOnlyNumeric(evt) {
    var theEvent = evt || window.event;
    var key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode( key );
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }

$(document).ready(function () {
    $("input.form-control.required").on('keyup',function(){
        showErrorForRequired(this);
    }); 
    $("input.form-control.required").on('blur',function(){
        showErrorForRequired(this);
    });    


    var url = new URL(window.location);
    var mod = url.searchParams.get("mod");
    if(mod == '112'){
        window.location = "index.php";
    }
  });
