function ajaxQyery(urlLink, dataObj, fnSuccess) {
    $.ajax({
        url: `/ajax/${urlLink}/`,
        method: 'GET',
        data: dataObj,
        dataType: 'json',
        success: fnSuccess
    });
}