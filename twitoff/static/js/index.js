$(document).ready(() => {

    /* 
        Function called on form submission when comparing users and who
        is more likely to make a tweet.
    */
    $("#compare_form-button").click(() => {

        const user1 = $("#compare_form select[name='user1']").val();
        const user2 = $("#compare_form select[name='user2']").val()
        let error_msg = '';
        // form message container
        const compare_result = $(".compare-result");

        if (user1 === null || user2 === null) {
            error_msg +=
                `
                <div class="alert alert-warning text-center" role="alert">
                    <p>You need to select User1 and User2, default values selected!</p>
                </div>
                `;
            compare_result.html(error_msg)
            setTimeout(() => compare_result.html(''), 2.5 * 1000);

        }
        else if (user1 === user2) {
            error_msg +=
                `
            <div class="alert alert-warning text-center" role="alert">
                <p>Both users are same, please try again!</p>
            </div>
            `;
            compare_result.html(error_msg)
            setTimeout(() => compare_result.html(''), 2.5 * 1000);
        }
        else {

            const post_url = "/compare"
            const request_method = "POST"; //get form GET/POST method
            const tweet_text = $("#compare_form textarea[name=tweet_text]").val();
            const post_data = JSON.stringify({
                "user1": user1,
                "user2": user2,
                "tweet_text": tweet_text
            })

            $.ajax({
                url: post_url,
                type: request_method,
                data: post_data,
                success: function (results) {
                    const msg = `
                    <div class="alert alert-info text-center" role="alert">
                    <p>${results.message}</p>
                </div>
                    `
                    compare_result.html(msg);
                    setTimeout(() => compare_result.html(''), 10 * 1000);
                },
                error: function () {
                    return
                }
            });
        }
    })

    /*
        Add a new twitter user to the app
    */
    $("#add-user-form-btn").click((event) => {

        let username = $("#add-user-form input").val();

        if (username[0] === "@") {
            username = username.slice(1);
        }
        let post_data = JSON.stringify({
            "username": username
        })
        let user_results = $(".my-2");
        $(".loading-icon").toggleClass("d-none");
        $(".btn-sav-usr").attr("disabled", true);
        $.ajax({
            url: "/user",
            type: "post",
            data: post_data,
            success: function (results) {
                if (results.success !== true) {
                    $(".btn-sav-usr").removeAttr("disabled");
                    $(".loading-icon").toggleClass("d-none");
                    let msg = `
                    <div class="alert alert-warning text-center" role="alert">
                    <p>${results.message}</p>
                </div>
                    `
                    user_results.html(msg);
                    setTimeout(() => {
                        user_results.html('');
                        $('input[name=username]').val('');
                    }, 2.5 * 1000
                    );
                    return
                }
                $(".loading-icon").toggleClass("d-none");
                let msg = `
                <div class="alert alert-success text-center" role="alert">
                <p>${results.message}</p>
            </div>
                `
                user_results.html(msg);
                setTimeout(() => {
                    user_results.html('');
                    window.location.reload(true);

                }, 2.5 * 1000
                );



            },
            error: function () {
                return
            }


        });
    })

    /*
        Visually remove a user from the DOM along with delteing
        the twitter user from the DB
    */
    $('.user-card').click((e) => {
        let user_card_txt = e.target.textContent.replace(/\s+/, "").toLowerCase();
        console.log(user_card_txt);
        debugger;
        if (user_card_txt === "delete") {
            $.ajax({
                url: `/delete/${e.currentTarget.id}`,
                type: "delete",
                success: function (results) {
                    if (results.success === true) {
                        $(`#${e.currentTarget.id}`).remove();
                        window.location.reload(true);
                    }
                },
                error: function (results) {
                    return
                }
            });
        }
    });

});


