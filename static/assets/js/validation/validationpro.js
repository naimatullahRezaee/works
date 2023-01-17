$(document).ready(function () {


  
    $("#education").keyup(function () {
      var enName = $("#education").val();
      var Icon_enName = $(".education_icon");
      validationPerInput(enName, Icon_enName);
    });
  
    $("#university").keyup(function () {
      var enName = $("#university").val();
      var Icon_enName = $(".university_icon");
      validationPerInput(enName, Icon_enName);
    });
    $("#discription").keyup(function () {
      var enName = $("#discription").val();
      var Icon_enName = $(".discription_icon");
      validationPerInputText(enName, Icon_enName);
    });

    //part of exprience 
    $("#select_education").keyup(function () {
        var enName = $("#select_education").val();
        var Icon_enName = $(".select_education_icon");
        validationPerInputExp(enName, Icon_enName);
      });
      $("#job_expreince").keyup(function () {
        var enName = $("#job_expreince").val();
        var Icon_enName = $(".job_expreince_icon");
        validationPerInputExp(enName, Icon_enName);
      });
      $("#discription_exp").keyup(function () {
        var enName = $("#discription_exp").val();
        var Icon_enName = $(".discription_exp_icon");
        validationPerInputText(enName, Icon_enName);
      });
      
//..............Details of experienc........................
      $("#profile_username").keyup(function () {
        var enName = $("#profile_username").val();
        var Icon_enName = $(".profile_username_icon");
        validationEnInput(enName, Icon_enName);
      });
      $("#job_biographi").keyup(function () {
        var enName = $("#job_biographi").val();
        var Icon_enName = $(".job_biographi_icon");
        validationPerInputText(enName, Icon_enName);
      });
      $("#profile_address").keyup(function () {
        var enName = $("#profile_address").val();
        var Icon_enName = $(".profile_address_icon");
        validationPerInput(enName, Icon_enName);
      });
      $("#profile_tazkira").keyup(function () {
        var enName = $("#profile_tazkira").val();
        var Icon_enName = $(".profile_tazkira_icon");
        validationPerInput(enName, Icon_enName);
      });
    
  });

  $("#profile_email").keyup(function () {
  
    var email = $("#profile_email").val();
    var Icon_email = $(".profile_email_icon");
  
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
  
  function validationPerInput(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[A-Za-z]/)) ||
      (ID.length !== 0 && ID.match(/^[0-9]/)) ||
      (ID.length !== 0 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},', ,',", ,",:,;,/,?,.,>,<,]/
        ))
    ) {
      console.log("wrong");
      Icon_name.html('<i class="fa fa-exclamation-circle error_icon"></i>');
      return false;
    } else if (ID.length <= 5) {
      Icon_name.html("");
      console.log("empty");
      return false;
    }
    Icon_name.html('<i  class="fas fa-check-circle true_icon"></i>');
    console.log("correct");
    return true;
  }
  function validationPerInputText(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[A-Za-z]/)) ||
      (ID.length !== 0 && ID.match(/^[0-9]/)) ||
      (ID.length !== 0 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},',',", ,",:,;,/,?,.,>,<,]/
        ))
    ) {
      console.log("wrong");
      Icon_name.html('<i class="fa fa-exclamation-circle error_icon"></i>');
      return false;
    } else if (ID.length <= 5) {
      Icon_name.html("");
      console.log("empty");
      return false;
    }
    Icon_name.html(''); 
    console.log("correct");
    return true;
  }


  // expreince of validation
  function validationPerInputExp(ID, Icon_name) {
    if (
      (ID.length !== 0 && ID.match(/^[0-9]/)) ||
      (ID.length !== 0 && ID.match(/^[۰-۹]/)) ||
      (ID.length !== 0 &&
        ID.match(
          /^[~,`,!,@,#,$,%,^,&,*,(,),_,-,=,+,|,{,},',', ,", ,",:,;,/,?,.,>,<,]/
        ))
    ) {
      console.log("wrong");
      Icon_name.html('<i class="fa fa-exclamation-circle error_icon"></i>');
      return false;
    } else if (ID.length <= 3) {
      Icon_name.html("");
      console.log("empty");
      return false;
    }
    Icon_name.html('<i  class="fas fa-check-circle true_icon"></i>');
    console.log("correct");
    return true;
  }
  // datePick.....
//   start date  experience//
  $(document).ready(function() {
    $("#start_date").pDatepicker({
      format: 'YYYY-MM-DD',
      initialValue : false,
      calendar:{
          persian: {
              locale: 'fa'
          }
      }
    });
  })

  //end Date
  $(document).ready(function() {
    $("#end_date").pDatepicker({
      format: 'YYYY-MM-DD',
      initialValue : false,
      calendar:{
          persian: {
              locale: 'en'
          }
      }
    });
  })
//..................end of experience...........................



//.....................start .........................................
$(document).ready(function() {
    $("#date_start_exp").pDatepicker({
      format: 'YYYY-MM-DD',
      initialValue : false,
      calendar:{
          persian: {
              locale: 'en'
          }
      }
    });
  })
  $(document).ready(function() {
    $("#date_End_exp").pDatepicker({
      format: 'YYYY-MM-DD',
      initialValue : false,
      calendar:{
          persian: {
              locale: 'en'
          }
      }
    });
  })