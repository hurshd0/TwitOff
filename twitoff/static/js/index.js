$(document).ready(() => {

    /* 
        Function called on form submission when comparing users and who
        is more likely to make a tweet.
    */
    $("#compare_form").submit(compareUsers(event))

    /*
        Add a new twitter user to the app
    */
    $("#add-user-form").submit(addUser(event))

    /*
        Visually remove a user from the DOM along with delteing
        the twitter user from the DB
    */
    $('.user-card').click(deleteUser(event));

});


function compareUsers(e){
    e.preventDefault(); //prevent default action
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
    let msg = '';

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
        $.ajax({
            url: post_url,
            type: request_method,
            data: post_data,
            success: function (results) {
                msg += `
                <div class="alert alert-info text-center" role="alert">
                <p>${results.message}</p>
            </div>
                `
                compare_result.html(msg);
                setTimeout(() => compare_result.html(''), 5.5 * 1000);
            },
            error: function () {
                return
            }
        });
    }
}

function addUser(e){
    e.preventDefault(); //prevent default action
    let username = $(this.username).val();
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

}

function deleteUser(e){
    let user_card = e.target.textContent;
    if (user_card.toLowerCase() === "delete me") {
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
}