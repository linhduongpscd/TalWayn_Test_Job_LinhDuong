$(document).ready(function () {
    // ============== Filter ============
    $("#filterStatus").change(function () {
        let val = $(this).find(":selected").val();
        let current_url = window.location.origin;
        if (val != 'all') {
            current_url = current_url + '/?status=' + val;
        }
        window.location.href = current_url;
    });
    // ============= Confirm delete ============ 
    $('a.delete-job').confirm('Are you sure you want to delete this user?', 'Warning!');
    $('a.delete-job').confirm({
        buttons: {
            hey: function () {
                location.href = this.$target.attr('href');
            }
        }
    });
    // =============== Auto refresh ==============
    var interval = null;
    function refresh() {
        $.ajax({
            type: 'GET',
            url: '/',
            // data: data,
            contentType: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function (data) {
                if (data['status'] == 'success') {
                    console.log()
                    $(".card-body").html(data['html']);
                }
            },
            error: function () {
                console.log("Error");
                console.log(data);
            }
        });
        console.log("Call update");
    }

    $(document).on('change', '.custom-control', function (e) {
        let test = e.target.checked;
        if (test) {
            interval = setInterval(refresh, 5000);
        }
        else {
            clearInterval(interval);
        }
    });
})
