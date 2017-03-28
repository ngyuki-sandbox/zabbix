(function(){
    var rpcid = 0;

    function render()
    {
        $.ajax({
            url: '/zabbix/api_jsonrpc.php',
            method: 'POST',
            contentType: 'application/json-rpc',
            dataType: 'json',
            processData: false,
            data: JSON.stringify({
                jsonrpc: '2.0',
                method: 'history.get',
                id: rpcid++,
                auth: Cookies.get('zbx_sessionid'),
                params: {
                    history: 2, // log
                    itemids: [23906], // アイテムIDをべた書き
                    sortfield: 'clock',
                    sortorder: 'DESC',
                    search: {
                        value: $('#value').val(), // 検索条件
                    },
                },
            }),
        })
        .success(function (data) {
            $('#list').empty();
            for ( let res of data.result) {
                if (res.value.length > 0) {
                    $('#list').append($('<li>').text(res.value))
                }
            }
        })
    }

    $(function(){
        render();
    });

    $('#value').on('keyup', function(){
        render();
    })

}())
