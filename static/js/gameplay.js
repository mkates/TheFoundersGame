
//************************************
//*****Slider Functionality***********
//************************************
	$(function() {
		$( "#slider-vertical" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 7,
			step: 1,
			value: 4,
			slide: function( event, ui ) {
				reDrawBars(ui.value);
			}
		});
	});

	var clearGradients = function() {
		$('.prog').removeClass('green-gradient');
		$('.prog').removeClass('yellow-gradient');
		$('.prog').removeClass('red-gradient');
	}
	
	var reDrawBars = function (uivalue) {
				$("#amount").html( uivalue );
				clearGradients();
				$( "#slider-vertical" ).slider({ value: uivalue});
				if (uivalue > 5) {
					$('.prog').addClass('green-gradient');
				} else if (uivalue > 2) {
					$('.prog').addClass('yellow-gradient');
				} else {
					$('.prog').addClass('red-gradient');
				}
				$('.prog').css('height',uivalue*46+20);
				
				$('.statusword').removeClass("selected");
				$("#status"+uivalue).addClass("selected");
				$('#questionblackedout').fadeOut();
				barValue = uivalue;
	}
	
	$(document).ready(function () {
		$('.statusword').click(function() {
			var status = $(this).attr('id');
			var value = status.charAt(6);
			reDrawBars(value);
		});
		
	});


//************************************
//**Load in template******************
//************************************
$(document).ready(function() {
	questionsAsked = [];
	meterValue = [];
	$.get(static_url+'txt/game1.txt', function(data) {
	    var txt = data.split("\n");
	    for (var a=0; a < txt.length; a++) {
	    	var array = txt[a].split(";");
	    	var nextq = null;
			if (array[5]) {
				nextq = array[5];
			}
	    	//If its a question
	    	if (array[0] === 'Q') {
	    		var ques = new question(array[1],array[2],array[3],array[4],nextq,true);
	    		questionarray.push(ques);
	    	} else if (array[0] === 'T') {
	    		title = array[1];
	    	} else if (array[0] === 'FQ') {
	    		var ques = new question(array[1],array[2],array[3],array[4],nextq,false);
	    		questionarray.push(ques);
	    	}  	
	    }
	    populate(questionarray,'black');
	}, 'text');
});



//************************************
//**Populate question well************
//************************************
var te = 0; var id = 0; var ma = 0; var fi = 0; var ex = 0;

var populate = function(questionarray,color) {
	for (var q=0; q < questionarray.length; q++) {
		var qa = questionarray[q];
		if (qa.visible) {
			var categoryid;
			var value;
			if (qa.category == "Te") { categoryid = 1; te+=1; value = te;};
			if (qa.category == "Id") { categoryid = 2; id+=1; value = id;};
			if (qa.category == "Ma") { categoryid = 3; ma+=1; value = ma;};
			if (qa.category == "Fi") { categoryid = 4; fi+=1; value = fi;};
			if (qa.category == "Ex") { categoryid = 5; ex+=1; value = ex;};
			if (color === 'blue') {
				var btncolor = 'btn-blue';
			} else {
				var btncolor = 'btn-orange';
			}
			$(".question"+categoryid+"_"+value).append("<button class='questionbutton btn "+btncolor+"'>"+qa.question+"</button>");
		};
	}
	buttonFunctionality();
};


//************************************
//********Global variables************
//************************************
var coins = 10;
var title;
var questionarray = [];
var followquestionarray = [];
var question = function (id,category,question,answer,nextquestionid,visible) {
	this.id = id;
	this.category = category;
	this.question = question;
	this.answer = answer;
	this.nextquestion = nextquestionid;
	this.visible = visible;
}
var barValue = 4;
//Storing User Selections
var questionsAsked = [];
var meterValue = [];

//************************************
//********Modal Windows***************
//************************************
var rulesdiv = $("<div class='rulesdiv'>");
$(document).on("click", ".reset", function(e) {
	bootbox.dialog("Are you sure you want to restart the game?", [{
		"label" : "Cancel",
		"class" : "btn",
		"callback": function() {
			//Do Nothing
		}
		}, {
		"label" : "Reset",
		"class" : "btn-danger",
		"callback": function() {
			location.reload();
			//Can custom reset too down the road
		}
		}]);
});
$(document).on("click", ".play", function(e) {
	bootbox.dialog(rulesdiv, [{
		"label" : "OK",
		"class" : "btn",
		"callback": function() {
			//Do Nothing
		}
	}]);
});

$(document).ready(function () {
	rulesdiv.append($('<h3>Game Play</h3>'));
	rulesdiv.append($('<p>You are Marty Dresdo, the leading venture capitalist in Boston. It is your job to evaluate a new idea that is being presented to you.<p>'));
	rulesdiv.append($('<p>To learn more about the idea, you can ask the entreprenuer questions from the question bank. Be careful though, because each question costs 1 coin, so you cannot ask every question.</p>'));
	rulesdiv.append($('<p>After each question, use the invest-o-meter on the right to change how likely you would be to fund this company.</p>'));
	rulesdiv.append($('<p>Once you use all your coins, click the Final Decision button to see how well you performed.</p>'));
	rulesdiv.append($('<h3>Scoring</h3>'));
	rulesdiv.append($('<p>Asking the right questions - It is important that you ask the right questions about an idea. Each question has an associated point value that adds to your score.</p>'));
	rulesdiv.append($('<p>Evaluating the idea - Some information presented by the entreprenuer will be promising, whileothers will signal red flags. If you slide the invest-o-meter the correct way and by the correct amount, you will acheive a higher score.</p>'));
});


//************************************
//********Tabs Functionality**********
//************************************
$(document).ready(function() {
	var currenttab = $("#questions1");
	currenttab.addClass("active");
	$('.option').click(function() {
		var id = $(this).attr('id');
		var handler = $("."+id);
		if (!(handler.is(":visible"))) {
			oldtab = currenttab.attr('id');
			currenttab.removeClass("active");
			newtab = $(this);
			$('.'+oldtab).fadeOut('fast',function() {
				currenttab = newtab;
				currenttab.addClass("active");
				$(handler).fadeIn();	;	
			});
		}
	});
});

var buttondisable = function(buttonhandle) {
	buttonhandle.addClass('disabled');
	buttonhandle.removeClass("btn-orange");
	buttonhandle.addClass("linethrough");
};

var buttonFunctionality = function() {
	$(".questionbutton").click(function() {
		if (!($(this).hasClass('disabled')) && coins > 0) {
			buttondisable($(this));
			decrementCoins();
			var question = $(this).html();
			var answer;
			var handler;
			//Find the answer in the array
			for (var q=0; q < questionarray.length; q++) {
				if (questionarray[q].question === question) {
					var handler = questionarray[q];
					var answer = questionarray[q].answer;
				}
			}
			
			//Record previous meter spot
			meterValue.push($( "#slider-vertical" ).slider('value'));
			//Add question to the Player Object
			questionsAsked.push(handler.id);
					
			//Draw the answers
			var response1 = $('<div class="response response-left">');
			var table = $('<table border="0" cellspacing="0" cellpadding="0">');
			var tr = $('<tr><td class="avatar"><img src="'+static_url+'img/busguy.png"/></td><td><div class="bubble bubbleleft"><p>'+question+'</p></div></td></tr>');
			table.append(tr);
			response1.append(table);
			$("#answers").append(response1);
			var elem = document.getElementById('answers');
			elem.scrollTop = elem.scrollHeight;
			
			var response2 = $('<div class="response response-right">');
			var table2 = $('<table border="0" cellspacing="0" cellpadding="0">');
			var tr2 = $('<tr><td><div class="bubble bubbleright"><p>'+answer+'</p></div></td><td class="avatar"><img src="'+imgurl+'"/></td></tr>');
			table2.append(tr2);
			response2.append(table2);
			setTimeout(function() {
				$("#answers").append(response2);
				var elem = document.getElementById('answers');
				elem.scrollTop = elem.scrollHeight;
			},500);
			
			
			//Black out the questions
			if (coins === 0) {
				$("#blackoutfinal").fadeIn()
			} else {
				$("#questionblackedout").fadeIn('400',function() {
					//Draw followup questions
					var nextq = handler.nextquestion;
					if (nextq !== null) {	
						for (var q=0; q < questionarray.length; q++) {
							if (questionarray[q].id === nextq) {
								questionarray[q].visible = true;
								populate([questionarray[q]],'blue');
							}
						}					
					};
				});
			};
		};
	});
};

//************************************
//********Coins JS********************
//************************************
var decrementCoins = function() {
	coins -= 1;
	if (coins == 0) {
		//Game Over
		console.log("Game Over");
	}
	$(".coinsleft").html(coins);
	//Coin momentarily glows after changing value
	$(".coin-container h4").addClass("coin-glow");
	setTimeout(function() {
		$(".coin-container h4").removeClass("coin-glow");
	},1000);
}

//************************************
//********Didn't affect me button ****
//************************************
$(document).ready(function() {
		$(".noeffect").click(function() {
			if (coins > 0) {
				$(".questionblackedout").fadeOut();
			};
		});
		$(".positiveeffect").click(function() {
			reDrawBars(Math.min(7,barValue+1));
			$(".questionblackedout").fadeOut();
		});
		$(".negativeeffect").click(function() {
			reDrawBars(Math.max(0,barValue-1));
			$(".questionblackedout").fadeOut();
		});
});

//************************************
//********Submit Results**************
//************************************

