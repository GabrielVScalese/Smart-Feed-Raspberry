import 'dart:async';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:udp/udp.dart';

class UdpClient {
  String url;

  UdpClient();

  Stream<String> execute() async* {
    var sender = await UDP.bind(Endpoint.any(port: Port(65000)));

    await sender.send(
        "Hello World!".codeUnits, Endpoint.broadcast(port: Port(1900)));

    StreamSubscription sub;

    sender.listen((datagram) {
      var message = String.fromCharCodes(datagram.data);
    });
  }
}
