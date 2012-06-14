function selectToken()
{
    // var txt = document.getElementByName("reg_area");
    var content = document.regularization.reg_area.value;
    var txt = document.regularization.reg_area;
    var startPos = txt.selectionStart;
    var endPos = txt.selectionEnd;
    //alert(startPos + " " + endPos);
    //alert(content.substring(startPost,endPos));
    var reg_word = "";
    var i = 0;
    for(i=startPos; i<endPos; i++)
    {
	reg_word = reg_word + content[i];
    }
    //alert(reg_word);
    document.regularization.reg_this.value = reg_word;
}
