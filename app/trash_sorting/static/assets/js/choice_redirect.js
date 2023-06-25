function redirect_from_choice(element){
    var args = element.getAttribute("args");
    post_search_with_args(args);
}


function post_search_with_args(args){
    console.log(JSON.stringify("{"+ args +"}"))
    redirect_by_post("http://127.0.0.1:8000/search/", JSON.parse("{"+ args +"}"), false)
}


function redirect_by_post(purl, pparameters, in_new_tab) {
    pparameters = (typeof pparameters == 'undefined') ? {}: pparameters;
    in_new_tab = (typeof in_new_tab == 'undefined') ? true: in_new_tab;

    var form = document.createElement("form");
    $(form).attr("id", "reg-form").attr("name", "reg-form").attr("action", purl).attr("method", "post").attr("enctype", "multipart/form-data");
    if (in_new_tab) {
        $(form).attr("target", "_blank");
    }
    console.log("zf")
    for (const [key, value] of Object.entries(pparameters)) {
         console.log(key, value);
         $(form).append('<input type="text" name="' + key + '" value="' + value + '" />');
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

    return false;
}