$(document).ready(function () {
    // Back to Top
    $(window).scroll(function () {
        if ($(this).scrollTop() != 0) {
            $('#toTop').fadeIn();
        } else {
            $('#toTop').fadeOut();
        }
    });
    $('#toTop').click(function () {
        $('body,html').animate({scrollTop: 0}, 800);
    });

    // Tree view
    $("#tree").explr();

    // Notification messages
    let $message = $('.messages');
    if ($message[0] !== undefined) {
        setTimeout(function () {
            $message.stop().animate({
                opacity: 0,
            }, 800, function () {
                $(this).remove();
            })
        }, 8000);

        $message.children('li').click(function () {
            $(this).stop().animate({
                opacity: 0,
            }, 800, function () {
                $(this).remove();
            })
        })
    }
});