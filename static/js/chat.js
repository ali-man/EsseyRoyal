$(document).ready(function () {

    function answerAfterSendMessageInChat(data) {
        if (data.ok) {
            $('#message_for_chat').val("");
        }
    }

    $('#send_message_in_chat').click(function () {
        let message = $('#message_for_chat').val();
        ajaxQyery('chat-send', {message: message}, answerAfterSendMessageInChat)
    });

    function messagesFromChat() {

        function answerServer(data) {
            $('ul.chat li').remove();
            for (let i = 0; i < data.length; i++) {
                $('ul.chat').append(
                    `
                    <li class="d-flex justify-content-between mb-4">
                        <div class="chat-body white p-3 z-depth-1" style="width: 100%">
                            <div class="header">
                                <strong class="primary-font" data-user-id="${data[i].fields.owner}"></strong>
                                <small class="pull-right text-muted"><i class="far fa-clock"></i>
                                    ${data[i].fields.created_datetime}
                                </small>
                            </div>
                            <hr class="w-100">
                            <p class="mb-0">
                                ${data[i].fields.message}
                            </p>
                        </div>
                        <img src="/static/img/noimage.png" alt="avatar" class="avatar rounded-circle mr-0 ml-3 z-depth-1">
                    </li>
                    `
                );

                let userID = data[i].fields.owner;

                ajaxQyery('chat-person', {userID: userID}, function fnPerson(p){
                    let strong = $(`strong[data-user-id="${data[i].fields.owner}"]`);
                    if (p.fields.first_name) {
                        $.each(strong, function (index, value) {
                            $(strong[index]).text(`${p.fields.first_name} ${p.fields.last_name}`);
                        });
                    } else {
                        $.each(strong, function (index, value) {
                            $(strong[index]).text(`${p.fields.email}`);
                        });
                    }
                });
            }
        }

        ajaxQyery('chat-ajax', {}, answerServer);
    }

    setTimeout(function tick(i) {
        messagesFromChat();
        // if (0 === i) return
        setTimeout(tick, 3000, i);
    }, 1000, 0)

});