var $stars;

jQuery(document).ready(function ($) {

    // Custom whitelist to allow for using HTML tags in popover content
    let myDefaultWhiteList = $.fn.tooltip.Constructor.Default.whiteList;
    // myDefaultWhiteList.textarea = [];
    // myDefaultWhiteList.button = [];

    $stars = $('.rate-popover');

    $stars.on('mouseover', function () {
        let index = $(this).attr('data-index');
        markStarsAsActive(index);
    });

    function markStarsAsActive(index) {
        unmarkActive();
        for (let i = 0; i <= index; i++) {
            $($stars.get(i)).addClass('amber-text');
        }
    }

    function unmarkActive() {
        $stars.removeClass('amber-text');
    }

    let starsIndex = null;

    $stars.on('click', function () {

        starsIndex = $(this).attr('data-index');

        $stars.popover('hide');
    });

    function fnFeedbackSuccess(data) {
        if (data.ok) {
            window.location.href = '/dashboard/';
        }
    }

    // Submit, you can add some extra custom code here
    // ex. to send the information to the server
    $('#rateMe').on('click', '#voteSubmitButton', function () {

        let txt = $('#textarea_val').val();
        let orderID = $('#rateMe').attr('data-order-id');
        ajaxQyery('order-feedback', {txt:txt, stars:starsIndex, orderID: orderID}, fnFeedbackSuccess);

        $stars.popover('hide');
    });

    // Cancel, just close the popover
    $('#rateMe').on('click', '#closePopoverButton', function () {
        $stars.popover('hide');
    });

});

$(function () {
    $('.rate-popover').popover({
        // Append popover to #rateMe to allow handling form inside the popover
        container: '#rateMe',
        // Custom content for popover
        content: `<div class="my-0 py-0"> <textarea type="text" id="textarea_val" style="font-size: 0.78rem" class="md-textarea form-control py-0" placeholder="Write us what can we improve" rows="3"></textarea> <button id="voteSubmitButton" type="submit" class="btn btn-sm btn-primary">Submit!</button> <button id="closePopoverButton" class="btn btn-flat btn-sm">Close</button>  </div>`
    });
    $('.rate-popover').tooltip();
});
