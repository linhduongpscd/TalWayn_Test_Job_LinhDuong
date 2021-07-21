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
    var intervalAutoRefresh = null;
    function refresh() {
        $.ajax({
            type: 'GET',
            url: '/',
            data: {
                auto_refresh: true
            },
            processData: true,
            contentType: false,
            success: function (data) {
                if (data['status'] == 'success') {
                    $(".card-body").html(data['html']);
                }
            },
            error: function () { }
        });
    }

    $(document).on('change', '.auto-refresh', function (e) {
        let checked = e.target.checked;
        if (checked) {
            intervalAutoRefresh = setInterval(refresh, 5000);
        }
        else {
            clearInterval(intervalAutoRefresh);
        }
    });

    // ============= Refresh status ================
    var intervalRefreshStatus = null;
    function refreshStatus() {
        $.ajax({
            type: 'GET',
            url: '/',
            data: {
                refresh_status: true
            },
            processData: true,
            contentType: false,
            success: function (data) { },
            error: function () { }
        });
    }

    $(document).on('change', '.refresh-status', function (e) {
        let checked = e.target.checked;
        if (checked) {
            intervalRefreshStatus = setInterval(refreshStatus, 60000);
        }
        else {
            clearInterval(intervalRefreshStatus);
        }
    });
})
