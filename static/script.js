action=''
window.onload = function() {
    action = document.code_form.action
}
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
last_value = "+"
$(document).ready(function() {
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
        document.code_form.action = action + phone.innerHTML;
        last_value = phone.innerHTML;
    });
});