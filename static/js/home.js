$(document).ready(function () {

    $(".scroll").click(function (event) {
        event.preventDefault();
        let full_url = this.href;
        let parts = full_url.split("#");
        let trgt = parts[1];
        let target_offset = $("#" + trgt).offset();
        let target_top = target_offset.top;
        $('html, body').animate({scrollTop: target_top + -170}, 500);
    });

    function fnCalculate(data) {
        $('#per_page').text(`$${data.per_page}`);
        $('#total_cost').text(`$${data.total_cost}`);
    }

    function fnCount() {
        let typeOrder = $('#id_type_order').val(); // 4
        let pagesOrder = $('#id_pages_order').val(); // 4
        let date = $('#ddate-picker').val(); // 30-05-2019
        let time = $('#ttime-picker').val(); // 17:30
        let dataObj = {
            typeOrder: typeOrder,
            pagesOrder: pagesOrder,
            date: date,
            time: time
        };
        ajaxQyery('calculate', dataObj, fnCalculate);
    }

    let listChangeCalculate = ['#id_type_order', '#id_pages_order', '#ddate-picker', '#ttime-picker'];

    for (let i = 0; i < listChangeCalculate.length; i++) {
        $(listChangeCalculate[i]).change(function () {
            fnCount();
        })
    }

    objectFitImages();
    jarallax(document.querySelectorAll('.jarallax'));

    $('.mdb-select').select2({
        width: '100%'
    });


    let currentDate = new Date(new Date().getTime() + (24 * 16) * 60 * 60 * 1000);

    $('.datepicker').datetimepicker({
        format: 'd-m-Y',
        value: currentDate,
        timepicker: false
    });
    $('.timepicker').datetimepicker({
        format: "H:i",
        value: currentDate,
        datepicker: false
    });
});