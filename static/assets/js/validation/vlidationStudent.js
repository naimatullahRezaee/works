$(document).ready(function () {

    $("#SId").keyup(function () {
      var enName = $("#SId").val();
      var Icon_enName = $(".SId_icon");
      validationEnInput(enName, Icon_enName);
    });
  
    $("#Susername").keyup(function () {
      var enName = $("#Susername").val();
      var Icon_enName = $(".Susername_icon");
      validationPerInput(enName, Icon_enName);
    });
  
    $("#Sl_name").keyup(function () {
      var enName = $("#Sl_name").val();
      var Icon_enName = $(".Slname_icon");
      validationPerInput(enName, Icon_enName);
    });
    $("#Sf_name").keyup(function () {
      var enName = $("#Sf_name").val();
      var Icon_enName = $(".Sfname_icon");
      validationPerInput(enName, Icon_enName);
    });
    $("#SnikName").keyup(function () {
        var enName = $("#SnikName").val();
        var Icon_enName = $(".SnikName_icon");
        validationPerInput(enName, Icon_enName);
      });
      $("#Sschool").keyup(function () {
        var enName = $("#Sschool").val();
        var Icon_enName = $(".Sschool_icon");
        validationPerInput(enName, Icon_enName);
      });
      $("#Sprovince_name").keyup(function () {
        var enName = $("#Sprovince_name").val();
        var Icon_enName = $(".Sprovince_name_icon");
        validationPerInput(enName, Icon_enName);
      });
  
  
    // English part
    $("#Sen_name").keyup(function () {
      var enName = $("#Sen_name").val();
      var Icon_enName = $(".SenName_icon");
      validationEnInput(enName, Icon_enName);
    });
    $("#Sen_lname").keyup(function () {
      var enName = $("#Sen_lname").val();
      var Icon_enName = $(".SenLName_icon");
      validationEnInput(enName, Icon_enName);
  
    });
    $("#Sen_fname").keyup(function () {
      var enName = $("#Sen_fname").val();
      var Icon_enName = $(".SenFName_icon");
      validationEnInput(enName, Icon_enName);
  
    });
    $("#SEn_username").keyup(function () {
        var enName = $("#SEn_username").val();
        var Icon_enName = $(".SenUName_icon");
        validationEnInput(enName, Icon_enName);
    
      });
 
    
  });
  function validationPerInput(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[A-Za-z]/)) ||
      (ID.length !== 0 && ID.match(/^[0-9]/)) ||
      (ID.length !== 0 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},',', ,",",:,;,/,?,.,>,<,]/
        ))
    ) {
      console.log("wrong");
      Icon_name.html('<i class="fa fa-exclamation-circle error_icon"></i>');
      return false;
    } else if (ID.length <= 2) {
      Icon_name.html("");
      console.log("empty");
      return false;
    }
    Icon_name.html('<i  class="fas fa-check-circle true_icon"></i>');
    console.log("correct");
    return true;
  }
  function validationEnInput(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[ا-ی]/)) ||
      (ID.length !== 0 && ID.match(/^[0-9]/)) ||
      (ID.length !== 0 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},', ,',",",:,;,/,?,.,>,<,]/
        ))
    ) {
      console.log("wrong");
      Icon_name.html('<i class="fa fa-exclamation-circle error_icon"></i>');
      return false;
    } else if (ID.length <= 2) {
      Icon_name.html("");
      console.log("empty");
      return false;
    }
    Icon_name.html('<i  class="fas fa-check-circle true_icon"></i>');
    console.log("correct");
    return true;
  }
  
  
  
  $("#Semail").keyup(function () {
  
    var email = $("#Semail").val();
    var Icon_email = $(".Semail_icon");
  
    if (email.length <= 2) {
      Icon_email.html("");
      console.log("empty");
      return false;
    } else if (!email.match(/^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/)) {
      console.log("wrong");
      Icon_email.html('<i class="fa fa-exclamation-circle error_icon "></i>');
      return false;
    }
    Icon_email.html('<i class="fas fa-check-circle  true_icon"></i>');
    console.log("correct");
    return true;
  });
  
  
  //part show passwords
  const hideIcon1 = document.getElementById("Sicon_pass_hide1");
  const passFiled1 = document.getElementById("Spassword1");
  const hideIcon2 = document.getElementById("Sicon_pass_hide2");
  const passFiled2 = document.getElementById("Spassword2");
  hideIcon1.addEventListener("click", () => {
    hideIcon1.classList.toggle("fa-eye-slash");
    hideIcon1.classList.toggle("fa-eye");
  
    if (hideIcon1.classList.contains("fa-eye")) {
      passFiled1.type = "text";
    } else {
      passFiled1.type = "password";
    }
  });
  
  hideIcon2.addEventListener("click", () => {
    hideIcon2.classList.toggle("fa-eye-slash");
    hideIcon2.classList.toggle("fa-eye");
  
    if (hideIcon2.classList.contains("fa-eye")) {
      passFiled2.type = "text";
    } else {
      passFiled2.type = "password";
    }
  });
  
  $('#Spassword2').keyup(function () {
    const pass1 = $("#Spassword1").val();
    const pass2 = $("#Spassword2").val();
    if(pass1.length=="" && pass2.length==""){
      $('#Spassword1').css('border', '1px solid lightgray');
      $('#Spassword2').css('border', '1px solid lightgray');
      return false;
    }
   else if (pass1.length==""){
      $('#Spassword1').css('border', '2px solid red');
      console.log("wrong!");
      return false;
    }
    else if(pass1 !=pass2){
      $('#Spassword2').css('border', '2px solid red');
      $('#Spassword1').css('border', '1px solid lightgray');
      return false;
  
    }
    else if (pass2==pass1){
      $('#Spassword1').css('border', '2px solid rgb(11, 75, 11)');
      $('#Spassword2').css('border', '2px solid rgb(11, 75, 11)');
      return true
    }
  });
  
  // datePick.....
  $(document).ready(function() {
    $("#Semp_date").pDatepicker({
      maxDate:new Date(),
      format: 'YYYY-MM-DD',
      initialValue : false,
      calendar:{
          persian: {
              locale: 'en'
          }
      }
    });
  })