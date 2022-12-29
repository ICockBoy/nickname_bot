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
$(document).ready(function() {
    last_value = document.getElementById("phone").innerHTML
    $('#phone').on('input', function() {
        phone = document.getElementById("phone");
        if (last_value.length > phone.innerHTML.length){
            if (phone.innerHTML[0] != "+"){
                phone.innerHTML = last_value;
                $('#phone').focusEnd();
            }
        }
        if (last_value.length < phone.innerHTML.length){
            if (isDigit(phone.innerHTML) == false || phone.innerHTML.length > 12){
                phone.innerHTML = last_value;
                $('#phone').focusEnd();
            }
        }
        $("#phone").attr('class', 'input-field-input');
        $("#phone_text_1").text('Phone Number');
        last_value = phone.innerHTML;
    });
    $('#form_butt').click(function() {
        username_b = document.getElementById("username").innerHTML;
        phone_b = Number(document.getElementById("phone").innerHTML).toString();
        $.get("/check_number/" + username_b+"&"+phone_b, function(data) {
            if (data=='0'){
                $("#phone").attr('class', 'input-field-input error');
                $("#phone_text_1").text('Invalid Phone Number');
            }
            else if (data=='1'){
                window.location.replace("/code?username="+username_b+"&"+"phone="+phone_b);
            }
        });

    });
});