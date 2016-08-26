function validateForm() {
    var x = document.getElementById("myForm")["E-mail"].value;
    var z = document.getElementById("myForm")["seq"].value;
    var a = document.getElementById("myForm")["upFile"].value;
    var p = document.forms["myForm"].getAttribute("data-file-type");
    var q = document.forms["myForm"].getAttribute("data-enctype");
    var s = document.forms["myForm"].getAttribute("data-seq-type");
    getIP();
    if ((z == null || z == "") && (a == null || a == "")) {
        alert("Either Enter Sequence in Text Box or Upload File " + a);
        return false;
    }
    else if ((z == null || z == "") && (a != null || a != "")) {
        if (x == null || x == "") {
        alert("It is required to fill in E-mail for File Upload" + x);
        return false;
        }
        else{
        document.forms["myForm"].setAttribute("action", p);
        document.forms["myForm"].setAttribute("enctype", q);
        return true;}
    } 
     else if ((a == null || a == "") && (z != null || z != "")) {
        if(checkLength(z)){
        document.forms["myForm"].setAttribute("action", s);
        return true;
        }
        else{ 
        alert("Please Enter Proper Input");
        return false;
        }
    }
    else if ((z != null || z != "") && (a != null || a != "")) {
       
        alert("Please Enter either Sequence in Text Box or Upload File not both.");
        return false;
    } 
   
 
}

function checkemail(str){
var filter=(/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i)
if (filter.test(str))
return true;
else{
alert("Please input a valid email address!  " + str)
return false;
}
}

function getIP() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("myForm")["IP"].value = xhttp.responseText;
    }
  };
  xhttp.open("GET", "http://ip-api.com/json", true);
  xhttp.send();
}

function checkLength(str){
    var box = document.getElementById('format');
    var format = box.options[box.selectedIndex].text;
    var sample = "";
    var flag = 0;
    var p = "";
    if (format == 'FASTA Sequence'){
        for (i = 0; i < str.length; i++) {
        p = str.charAt(i); 
        if (p == '>'){ 
          flag +=1;
        }
    }    
    } else if (format == 'GenBank Identifier'){
        for (i = 0; i < str.length; i++) {
        p = str.charAt(i); 
        if (p == ','){ 
          flag +=1;
        }
     }   
    }else if (format == 'Uniprot Identifier'){
    for (i = 0; i < str.length; i++) {
        p = str.charAt(i); 
        if (p == ','){ 
          flag +=1;
        }
     } 
        
    }
    if (flag < 0 || flag > 10){
    return false;
    }
    else{
    return true;
    }
}
