$('#date_deadline').datetimepicker({
    format: 'd-m-Y',
    value: new Date(new Date().setDate(new Date().getDate() + 1)),
    timepicker: false
});
$('#time_deadline').datetimepicker({
    format: "H:i",
    value: "00:00",
    datepicker: false
});

$('.customer_remove_order').click(function () {
    let orderID = $(this).attr('data-order-id');
    $('#id_remove').val(orderID);
});


// CUSTOMER CALCULATE
function fnCalculate(data) {
    $('#per_page').text(`$${data.per_page}`);
    $('#total_cost').text(`$${data.total_cost}`);
}

function fnCount() {
    let typeOrder = $('#id_type_order').val(); // 4
    let pagesOrder = $('#id_number_page').val(); // 4
    let date = $('#date_deadline').val(); // 30-05-2019
    let time = $('#time_deadline').val(); // 17:30
    let dataObj = {
        typeOrder: typeOrder,
        pagesOrder: pagesOrder,
        date: date,
        time: time
    };
    ajaxQyery('calculate', dataObj, fnCalculate);
}

let listChangeCalculate = ['#id_type_order', '#id_number_page', '#date_deadline', '#time_deadline'];

for (let i = 0; i < listChangeCalculate.length; i++) {
    $(listChangeCalculate[i]).change(function () {
        fnCount();
    })
}