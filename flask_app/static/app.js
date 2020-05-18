let get_input_coefficients = function() {
    let hts = $("input#hts").val()
    let ats = $("input#ats").val()
    let hos = $("input#hos").val()
    let hwpg = $("input#hwpg").val()
    let awpg = $("input#awpg").val()

    return {'hts': parseFloat(hts),
            'ats': parseFloat(ats),
            'hos': parseFloat(hos),
            'hwpg': parseInt(hwpg),
            'awpg': parseInt(awpg)} 
};

let send_coefficient_json = function(coefficients) {
    $.ajax({
        url: '/solve',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            display_solutions(data);
        },
        data: JSON.stringify(coefficients)
    });
};

let display_solutions = function(solutions) {
    $("span#solution").html(solutions.prob)
};

$(document).ready(function() {

    $("button#solve").click(function() {
        let coefficients = get_input_coefficients();
        send_coefficient_json(coefficients);
    })

})