$(document).ready(() => {
    $("#compare_form").submit(function (event) {

        let post_url = $(this).attr("action"); //get form action url
        let request_method = $(this).attr("method"); //get form GET/POST method
        let tweet_text = $(this.tweet_text).val();
        let user1 = $(this.user1).val();
        let user2 = $(this.user2).val();
        let post_data = JSON.stringify({
            "user1": user1,
            "user2": user2,
            "tweet_text": tweet_text
        })

        let error_msg = '';
        let compare_result = $(".compare-result");

        console.log(error_msg);

        if (user1 === null || user2 === null) {
            error_msg +=
                `
                <div class="alert alert-warning" role="alert">
                    You need to select User1 and User2, default values selected!
                </div>
                `;
            compare_result.html(error_msg)
            setTimeout(() => compare_result.html(''), 2.5 * 1000);

        }
        else if (user1 === user2) {
            error_msg +=
                `
            <div class="alert alert-warning" role="alert">
                Both users are same, please try again!
            </div>
            `;
            compare_result.html(error_msg)
            setTimeout(() => compare_result.html(''), 2.5 * 1000);
        }

        else {
            $.ajax({
                url: post_url,
                type: request_method,
                data: post_data,
                success: function (results) {
                    console.log(results);
                },
                error: function () {
                    console.log()
                }
            });
        }

        event.preventDefault(); //prevent default action

    });



});

