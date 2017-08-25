function getAllQuestion(){
    var aq = $('.question');
    return aq;
}

var AQ = getAllQuestion();


function setName(name){
    $('.question-answer.format1').eq(0).find('input').eq(0).attr('value',name);
}

function setDanwei(danwei){
    var danweiQuestion = AQ.find(':contains("单位")').parent('.question');
    var allDanweiDiv = danweiQuestion.find(':contains('+danwei+')').parent('.answer-radio');
    var specificDanweiDiv = NaN;
    for (var each in allDanweiDiv) {
        if (allDanweiDiv[each].innerText === danwei) {
            specificDanweiDiv=allDanweiDiv[each];
            break;
        }
    }

    $(specificDanweiDiv).find('label').click();
}

function setBanji(banji){
    var banjiQuestion = AQ.find(':contains("班级")').parent('.question');
    var specificBanjiDiv = banjiQuestion.find(':contains('+banji+')').parent('.answer-radio');
    // specificBanjiDiv.addClass('checked');
    specificBanjiDiv.find('label').click();
}

function setAllToTen(){
    // $('input[data-col="1"]').parent().addClass('checked');
     $('input[data-col="1"]').click();
}

function scrollToEnd(){//滚动到底部
    var h = $(document).height()-$(window).height();
    $(document).scrollTop(h); 
}

function submit_wenjuan() {
    $('#page-next').click();

}

function gogogo(name,danwei,banji){
    setAllToTen();
    setName(name);
    setDanwei(danwei);
    setBanji(banji);
    scrollToEnd();
    // submit_wenjuan();
}

// $(document).ready(function(){
//     gogogo();
// });
