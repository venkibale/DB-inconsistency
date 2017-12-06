			
 function showTableData(obj) {
	    document.getElementById('database').innerHTML = "";
        document.getElementById('info1').innerHTML = "";
		 //document.getElementById('info').src = "";
		document.getElementById('info').innerHTML = "";

		 var tab;

        var myTab = document.getElementById(obj.getAttribute('data-info'));
        //info.innerHTML="<table border='1'><th>Table Names</th>";
        tab="<table border='1'><th>Table Names</th>"
		// LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
        for (i = 1; i < myTab.rows.length; i++) {
           tab += '<tr>';
            // GET THE CELLS COLLECTION OF THE CURRENT ROW.
            var objCells = myTab.rows.item(i).cells;

            // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
            for (var j = 0; j < objCells.length; j++) {
				
                tab +=  '<td>'+' '+ objCells.item(j).innerHTML+'</td>';	
				
            }
			
             			 // ADD A BREAK (TAG).
			 
        
		tab += ''+'</tr>';		
    }
	info.innerHTML +=tab+'</table>';
 }
	
function showData(obj) {
		document.getElementById('info').innerHTML = "";
        document.getElementById('info1').innerHTML = "";
        //info1.innerHTML="<table border='1'><th>Parent Table</th><th>Child Table</th><th>Deletion Order</th>";
        var myTab = document.getElementById(obj.getAttribute('data-info'));
        var tab;
		
		tab="<table border='1'><th>Parent Table</th><th>Child Table</th></th><th>Deletion Order</th>"
        // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
        for (i = 1; i < myTab.rows.length; i++) {
            //info1.innerHTML += '<tr>';
            // GET THE CELLS COLLECTION OF THE CURRENT ROW.
            var objCells = myTab.rows.item(i).cells;

            // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
			tab+='<tr>'	
            for (var j = 0; j < objCells.length; j++) {
                tab+= '<td>'+' '+ objCells.item(j).innerHTML+'</td>'
				
            }
			tab+='</tr>'
		}
			//document.write(tab)
			info1.innerHTML +=tab ;
			//document.write("<scr"+ "ipt src='jscript.js' type='text/javascript'>"+info1.innerHTML+"<\/scr"+"ipt>")
			//document.write("<head><link rel='import' href='Data(spyder).html'><head><scr" + "ipt src='jscript.js' type='text/javascript'><\/scr" + "ipt>"+info1.innerHTML);
                  // ADD A BREAK (TAG).
        info1.innerHTML +='</table>';
		}
		
		
function myFunction(obj) {
    //document.getElementById(obj.getAttribute('data-info')).style.display = "block";
	
	var text=document.getElementById(obj).id;
	localStorage.setItem("text1",text);
	//console.log(text)
	//window.open("new.html","_self")
	if (text!='NULL'){
	
	
	window.open("new.html","_self");	
	
	}
	
}


function myFunction_table(obj) {
    //document.getElementById(obj.getAttribute('data-info')).style.display = "block";
	
	var textb=document.getElementById(obj).id;
	localStorage.setItem("text2",textb);
	//console.log(text);
	if (textb!='NULL'){
	
	
	window.open("final.html");	
	
	}
	
}

function myFunction_parent(obj) {
    //document.getElementById(obj.getAttribute('data-info')).style.display = "block";
	//console.log(obj);
	var textc=document.getElementById(obj).id;
	
	console.log(textc);
	if (textc!='NULL'){
	
	
     document.getElementById(localStorage.getItem("text2")).style.display='none';	
	 document.getElementById(localStorage.getItem("text3")).style.display='none';	
	localStorage.setItem("text3",textc);
	}
	console.log(document.getElementById(localStorage.getItem("text3")));
	document.getElementById(localStorage.getItem("text3")).style.display='block';
	//localStorage.removeItem(localStorage.getItem("text3"));
	
}

	
function myfunc() {
	var textx=localStorage.getItem("text1");
	//console.log(textx);
	document.getElementById(textx).style.display='block';
	//console.log(textx);
    //alert(textx);
	localStorage.removeItem(textx);
}
function myfunc1() {
	//var texty=localStorage.getItem("text2");
	//console.log(localStorage.getItem("text2"));
	//console.log(texty);
	//console.log(document.getElementById(localStorage.getItem("text2")));
	document.getElementById(localStorage.getItem("text2")).style.display='block';
	//console.log(texty);
    //alert(localStorage.getItem("text2"));
	//localStorage.removeItem(localStorage.getItem("text2"));
}

	
    