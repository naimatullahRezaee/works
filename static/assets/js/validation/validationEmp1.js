$(document).ready(function () {

    $("#Id").keyup(function () {
      var enName = $("#Id").val();
      var Icon_enName = $(".Id_icon");
      validationEnInput(enName, Icon_enName);
    });
  
    $("#username").keyup(function () {
      var enName = $("#username").val();
      var Icon_enName = $(".username_icon");
      validationPerInput(enName, Icon_enName);
    });
  
    $("#l_name").keyup(function () {
      var enName = $("#l_name").val();
      var Icon_enName = $(".lname_icon");
      validationPerInput(enName, Icon_enName);
    });
    $("#f_name").keyup(function () {
      var enName = $("#f_name").val();
      var Icon_enName = $(".fname_icon");
      validationPerInput(enName, Icon_enName);
    });
    $("#address").keyup(function () {
      var enName = $("#address").val();
      var Icon_enName = $(".address_icon");
      validationPerInput(enName, Icon_enName);
    });
    $("#phone_number").keyup(function () {
      var enName = $("#phone_number").val();
      var Icon_enName = $(".phone_number_icon");
      validationPhoneNumber(enName, Icon_enName);
    });
  
  
    // English part
    $("#en_name").keyup(function () {
      var enName = $("#en_name").val();
      var Icon_enName = $(".enName_icon");
      validationEnInput(enName, Icon_enName);
    });
    $("#en_lname").keyup(function () {
      var enName = $("#en_lname").val();
      var Icon_enName = $(".enLName_icon");
      validationEnInput(enName, Icon_enName);
  
    });
    $("#en_fname").keyup(function () {
      var enName = $("#en_fname").val();
      var Icon_enName = $(".enFName_icon");
      validationEnInput(enName, Icon_enName);
  
    });
    $("#En_username").keyup(function () {
      var enName = $("#En_username").val();
      var Icon_enName = $(".enUName_icon");
      validationEnInput(enName, Icon_enName);
  
    });
    $("#en_name").keyup(function () {
      var enName = $("#en_name").val();
      var Icon_enName = $(".enName_icon");
      validationEnInput(enName, Icon_enName);
  
    });
  
  });
  function validationPhoneNumber(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[A-Za-z]/)) ||
      (ID.length !== 0 && ID.match(/^[ا-ی]/)) ||

      (ID.length <= 9 && ID.match(/^[0-9]/)) ||
      (ID.length <=9 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},',',",",:,;,/,?,.,>,<,]/
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
  function validationPerInput(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[A-Za-z]/)) ||
      (ID.length !== 0 && ID.match(/^[0-9]/)) ||
      (ID.length !== 0 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},',',",",:,;,/,?,.,>,<,]/
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
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},',',",",:,;,/,?,.,>,<,]/
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
  
  
  
  $("#email").keyup(function () {
  
    var email = $("#email").val();
    var Icon_email = $(".email_icon");
  
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
  const hideIcon1 = document.getElementById("icon_pass_hide1");
  const passFiled1 = document.getElementById("password1");
  const hideIcon2 = document.getElementById("icon_pass_hide2");
  const passFiled2 = document.getElementById("password2");
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
  
  $('#password2').keyup(function () {
    const pass1 = $("#password1").val();
    const pass2 = $("#password2").val();
    if(pass1.length=="" && pass2.length==""){
      $('#password1').css('border', '1px solid lightgray');
      $('#password2').css('border', '1px solid lightgray');
      return false;
    }
   else if (pass1.length==""){
      $('#password1').css('border', '2px solid red');
      console.log("wrong!");
      return false;
    }
    else if(pass1 !=pass2){
      $('#password2').css('border', '2px solid red');
      $('#password1').css('border', '1px solid lightgray');
      return false;
  
    }
    else if (pass2==pass1){
      $('#password1').css('border', '2px solid rgb(11, 75, 11)');
      $('#password2').css('border', '2px solid rgb(11, 75, 11)');
      return true
    }
  });
  
  // datePick.....
  $(document).ready(function() {
    $("#emp_date").pDatepicker({
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