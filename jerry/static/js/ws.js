function WSSHClient() {
};


WSSHClient.prototype._generateEndpoint = function (options) {
    console.log(options);
    if (window.location.protocol == 'https:') {
        var protocol = 'wss://';
    } else {
        var protocol = 'ws://';
    }

    var endpoint = protocol + document.URL.match(RegExp('//(.*?)/'))[1] + '/ws/terminal' + document.URL.match(/(\?.*)/);
    return endpoint;
};


WSSHClient.prototype.connect = function (options) {
    var endpoint = this._generateEndpoint();

    if (window.WebSocket) {
        this._connection = new WebSocket(endpoint);
    }
    else if (window.MozWebSocket) {
        this._connection = MozWebSocket(endpoint);
    }
    else {
        options.onError('WebSocket Not Supported');
        return;
    }

    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = evt.data.toString()
        options.onData(data);
    };


    this._connection.onclose = function (evt) {
        options.onClose();
    };
};

WSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify(data));
};

WSSHClient.prototype.sendInitData = function (options) {
    var data = {
        hostname: options.host,
        port: options.port,
        username: options.username,
        ispwd: options.ispwd,
        secret: options.secret
    };
    this._connection.send(JSON.stringify({"tp": "init", "data": options}))
}

WSSHClient.prototype.sendClientData = function (data) {
    this._connection.send(JSON.stringify({"tp": "client", "data": data}))
}

var client = new WSSHClient();

$(document).ready(function () {
    var options = {
        host: $("#term").attr("sship"),
        port: 22,
        username: 'root',
    }
    openTerminal(options)
});
