import $ from 'jquery'
import 'reconnectingwebsocket'
import 'select2'

$(document).ready(function() {

    // select2 plugin
    $('#id_tags').addClass('js-tags-multiple')
    $('.js-tags-multiple').select2({
        tags: true,
        tokenSeparators: [',', ' ']
    });

    // Determine host for web sockets
    var wsLink = $('link[rel="ws"]')
    if (wsLink.length) {
        var host = wsLink.attr('src')
    }
    else {
        var host = window.location.host
    }

    function readCookie(name) {
    	var nameEQ = name + "=";
    	var ca = document.cookie.split(';');
    	for(var i=0;i < ca.length;i++) {
    		var c = ca[i];
    		while (c.charAt(0)==' ') c = c.substring(1,c.length);
    		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    	}
    	return null;
    }

    var sessionKey = readCookie('sessionid')

    const proto = window.location.protocol == 'https:' ? 'wss' : 'ws';
    const socket = new ReconnectingWebSocket(proto + '://' + host + '/socket/?session_key=' + sessionKey)
    console.log(socket)

    socket.onmessage = function(e) {
        console.log(e.data)
        let rcvd = e.data.split('/_/')

        if (rcvd[0] == 'comment_success:') {
            // Clear input field
            $('.comment-form__input').val('')

            // Slice up comment fields
            let rcvd_author = rcvd[1]
            let rcvd_description = rcvd[2]
            let rcvd_id = rcvd[4]
            let rcvd_idea_slug = rcvd[5]

            // Create new comment html
            var html = `<div class="idea-detail__comment">
                            <div class="meta-info">
                                <span class="comment-meta__user">${rcvd_author}</span>
                                <div class="seperator">
                                </div>
                                a second ago
                            </div>
                            <p>${rcvd_description}</p>
                            <div class="text-small-neutral">
                                <a href="/idea/rcvd_idea_slug/commentedit/${rcvd_id}/" class="text-link--alt text-link--no-decoration">Edit</a>
                                <div class="seperator"></div>
                                    <a href="/idea/rcvd_idea_slug/commentdelete/${rcvd_id}/" class="text-link--primary text-link--no-decoration">Delete</a>
                            </div>
                        </div>`

            // Add new comment html to DOM
            $('.idea-detail__comments').prepend(html)
        }

        else {
            console.log(e.data)
        }
    }

    $('.idea-vote').click(function(e) {
        e.stopPropagation()
        let $this = $(this)
        let ideaId = $this.attr('data-idea-id')
        let $voteTotalObject = $('#vote__total-for-' + ideaId)
        let voteTotalValue = parseInt($voteTotalObject.text())
        let msg = undefined

        if ($this.hasClass('idea-vote__cast')) {
            voteTotalValue--
            msg = ('remove_vote:' + '/_/' + ideaId)
        } else {
            voteTotalValue++
            msg = ('add_vote:' + '/_/' + ideaId)
        };

        // Add new vote to DOM, change class
        $voteTotalObject.text(voteTotalValue)
        $this.toggleClass('idea-vote__cast')

        // Send msg to consumer
        socket.send(msg);
    });

    $('.comment-button').click(function(e) {
        e.stopPropagation();
        let $this = $('.idea-vote');
        let ideaId = $this.attr('data-idea-id');
        let $commentDescription =  $('.comment-form__input').val()
        let $commentTotalObject = $('#comment__total-for-' + ideaId)
        let commentTotalValue = parseInt($commentTotalObject.text())

        if ($commentDescription.length > 0 && $commentDescription.length < 1500) {

            // Add new comment count to DOM
            commentTotalValue++;
            $commentTotalObject.text(commentTotalValue)

            // Assemble and send msg to consumer
            let listifyMsg = ['add_comment:', ideaId, $commentDescription]
            let stringifyMsg = listifyMsg.join('/_/')
            console.log(stringifyMsg)
            let msg = (stringifyMsg)
            socket.send(msg)
        }

        else {
            console.log('comment contains too many or few characters')
        }

    });
})
