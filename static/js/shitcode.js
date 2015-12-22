//AJAX отправка ответа на сервер
$('#post-form').on('submit', function(event){
    event.preventDefault();
    create_answer(event.target);
});

function create_answer(target) {
    $.ajax({
        url : "/create_answer/",
        type : "POST", 
        data : { text : target.text.value,
                 csrfmiddlewaretoken : target.csrfmiddlewaretoken.value,
                 question_id : target.question_id.value
                 }, 
        success : function(json) {
            $('#post-form').html("<p class='response_for_answer'>Ваш ответ принят <br> <a href = '#' class='refresh_link' onclick='javascript:window.location.reload();' >Перезагрузить </a> </p>"); 
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            $('#post-form').html("<p class='response_for_answer error'>Что-то пошло не так ...</p>"); 
        }
    });
};

//AJAX лайк или дизлай ответу
function change_rating_answer(inj_answer_id, inj_mark) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : "/change_rating_answer/",
        type : "POST", 
        data : {answer_id : inj_answer_id,
                mark : inj_mark,
                csrfmiddlewaretoken : csrftoken
                }, 
        success : function(json) {
            console.log(json)
            $("span.answer_like." + inj_answer_id).html("")
            $("span.answer_dislike." + inj_answer_id).html("")
            $("div." + inj_answer_id).html(json.rating);
        },
        error : function(xhr,errmsg,err) { 
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$("span.answer_like").click(function(){
    change_rating_answer($(this).attr('id'), 1);
});

$("span.answer_dislike").click(function(){
    change_rating_answer($(this).attr('id'), -1);
});

//AJAX лайк или дизлай вопросу
function change_rating_question(inj_question_id, inj_mark) { 
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : "/change_rating_question/",
        type : "POST", 
        data : {question_id : inj_question_id,
                mark : inj_mark,
                csrfmiddlewaretoken : csrftoken
                }, 
        success : function(json) {
            console.log(json)
            $("span.question_like." + inj_question_id).html("")
            $("span.question_dislike." + inj_question_id).html("")
            $("div." + inj_question_id).html(json.rating);
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$("span.question_like").click(function(){
    change_rating_question($(this).attr('id'), 1);
});

$("span.question_dislike").click(function(){
    change_rating_question($(this).attr('id'), -1);
});

//AJAX checkbox ответ верен
$('.ckeck_ans').click(function() {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
    url : "/check_answer/",
    type : "POST", 
    data : {answer_id : $(this).attr('id'),
            mark : $(this).is(':checked'),
            csrfmiddlewaretoken : csrftoken
        }, 
    success : function(json) {
        console.log(json)
    },
    error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});

//Функция для получение кук по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
