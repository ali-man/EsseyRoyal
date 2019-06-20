$(document).ready(function () {

    setTimeout(function tick(i) {
        messagesFromChat();
        filesFromChat();
        // if (0 === i) return
        setTimeout(tick, 2000, i);
    }, 1000, 0)

});

function resultFilesFromChat(data) {
    $('ul.friend-list li').remove();
    for (let i = 0; i < data.length; i++) {
        $('ul.friend-list').prepend(
            `
            <li class="p-2">
                <a href="${data[i].link}" class="d-flex justify-content-between">
                    <img src="
                    ${data[i].avatar}
                    " alt="avatar" width="40" height="40"
                         class="avatar rounded-circle d-flex align-self-center mr-2 z-depth-1">
                    <div class="text-small">
                        <strong>${data[i].name}</strong>
                        <p class="last-message text-muted">
                            ${data[i].owner}
                        </p>
                    </div>
                    <div class="chat-footer">
                        <p class="text-smaller text-muted mb-0">${data[i].created_datetime}</p>
                        <!--<span class="badge badge-danger float-right">1</span>-->
                    </div>
                </a>
            </li>
            `
        );
    }
}

function resultMessagesFromChat(data) {
    $('ul.chat li').remove();
    for (let i = 0; i < data.length; i++) {
        $('ul.chat').prepend(
            `
            <li class="d-flex justify-content-between mb-4">
                <img src="${data[i].avatar}" class="avatar rounded-circle mr-2 ml-lg-3 ml-0 z-depth-1" style="width: 50px; height: 50px;">
                <div class="chat-body white p-3 ml-2 z-depth-1" style="width: 100%">
                    <div class="header">
                        <strong class="primary-font">${data[i].owner}</strong>
                        <small class="pull-right text-muted"><i class="far fa-clock"></i>
                            ${data[i].created_datetime}
                        </small>
                    </div>
                    <hr class="w-100">
                    <p class="mb-0">
                        ${data[i].message}
                    </p>
                </div>                
            </li>
            `
        );
    }
}

function messagesFromChat() {
    $.ajax({
        data: {messagesFromChat: 'all'},
        success: resultMessagesFromChat
    })
}

function filesFromChat() {
    $.ajax({
        data: {filesFromChat: 'all'},
        success: resultFilesFromChat
    })
}
