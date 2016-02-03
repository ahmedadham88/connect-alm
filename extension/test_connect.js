$(document).ready( function() {

var host= "localhost";

document.getElementById('connectBtn').addEventListener('click',login);
document.getElementById('addArtifactBttn').addEventListener('click',addArtifact );
document.getElementById('logout').addEventListener('click',switchToUserLoginView );

var signum = readCookie("signum");

if(signum != "") {
	connectSignum(signum);
	switchToFeedView();
}


function login() {
	var loggedInUser = $('#signum').val();
	writeCookie('signum', loggedInUser, -1);
	connectSignum(loggedInUser);
	switchToFeedView();
}

function writeCookie(name, value, days) {
	var date, expires;

	if(days > 0) {
		date = new Date();
		date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
		expires = "; expires=" + date.toGMTString();
	} else {
		expires = "";
	}

	document.cookie = name + "=" + value + expires + "; path=/"
}

function readCookie(name) {
	var i, c, ca, nameEQ = name + "=";
    ca = document.cookie.split(';');
    for(i=0;i < ca.length;i++) {
        c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return '';
}

function connectSignum(signum) {
	var reqType = "GET";
	var dataType = "json";
	var url = "http://" + host + "/connect/" + signum.toUpperCase() + "/";
	var content_type = "application/json;charset=utf-8";

	$.ajax({ 
         type: reqType,
         dataType: dataType,
        
         url: url,         
       
         success: function(data){        
            poll(signum); //Start polling for this signum
         },
         error: function(x, t, m) {
    		//alert("im here");
    		$('#error').append( "Could not complete process");
    		$('#error').show();
        	
         }
         //timeout: 500            
     });
}

function addArtifact() {
	var artifactId = $('#artifactId').val();
	var signum = readCookie("signum");

	//get any artifacts currently being followed
	var artifacts = readCookie("artifacts");

	//add new artifact
	artifacts[artifacts.length] = artifactId;

	//debug - print list
	alert(artifacts);

	//make rest call
	var reqType = "GET";
	var dataType = "json";
	var url = "http://"+host+"/follow/" + signum.toUpperCase() + "QQQQQ" + artifactId + "/";

	$.ajax({ 
             type: reqType,
             dataType: dataType,
             url: url,
             success: function(data){        
                //alert(data);
                writeCookie("artifacts", artifacts);
             },
             error: function() {
             		$('#error').append("Could not complete process");
             	           
             }

    });
}

function switchToFeedView(){
	$('#status').hide();
	$('#feedContent').show();
}

function poll(signum) {
    setInterval(function () {
    	//alert("timeout");
        $.ajax({
            type: 'GET',
            dataType: 'json',
            url: "http://"+host+"/poll/"+signum + "/",
            success: function (data) {
            	var updateJson = data; //updates = JSON && JSON.parse(updateJson) || $.parseJSON(updateJson);
            	var updates = data;

				$.each(updates, function(key, value){
					$('#feedContent').append('<p><b>Artifact: </b>'+key+'</p>');
					
					$('#feedContent').append('<p><b>Update: </b>'+value+'</p>');
					
					$('#feedContent').append('<hr/>'); // horizontal line
				});
            }
            
        });
    }, 15000);
}

function switchToUserLoginView(){
	$('#status').show();
	$('#feedContent').hide();
	}
});