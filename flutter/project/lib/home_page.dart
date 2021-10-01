import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:udp/udp.dart';
import 'package:upnp/upnp.dart';

class HomePage extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<HomePage> {
  var text = "Aqui aparece a resposta"; // Texto que sera exibido

  String host = "239.255.255.250";
  int port = 1900;

  String msg = "M-SEARCH * HTTP/1.1\r\n" +
      "HOST:239.255.255.250:1900\r\n" +
      "MAN:\"ssdp:discover\"\r\n" +
      "MX: 2\r\n" +
      "ST: ssdp:all\r\n\r\n";

  findDevices() async {
    var sender = await UDP.bind(Endpoint.any(port: Port(65000)));

    await sender.send(
        "Hello World!".codeUnits, Endpoint.broadcast(port: Port(1900)));

    var url = '';

    await sender.listen((datagram) {
      var message = String.fromCharCodes(datagram.data);
      url = message;
    }, timeout: Duration(seconds: 1));

    return url;
  }

  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;

    return Scaffold(
        appBar: AppBar(
          title: Text('Consumo de API Flask'),
          centerTitle: true,
        ),
        body: Container(
          height: size.height,
          width: size.width,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                  child: Text(
                this.text,
                style: TextStyle(fontSize: size.height * 0.02),
              )),
              SizedBox(
                height: size.height * 0.04,
              ),
              Container(
                height: 50,
                width: 120,
                child: ElevatedButton(
                  onPressed: () async {
                    try {
                      // var client = new Client(); // Cliente

                      // var animal =
                      //     await client.setValue(key: 'animal', value: 'person');
                      // var mode = await client.setValue(
                      //     key: 'mode', value: 'Aproximação');
                      // var quantity =
                      //     await client.setValue(key: 'quantity', value: 100);

                      // var getMode = await client.getValue('mode');

                      // this.text = 'Resposta: ${quantity.toString()}';
                      // setState(() {});
                      var url = await findDevices();
                    } catch (err) {
                      print(err);
                    }
                  },
                  child: Text(
                    'Consumir',
                    style: TextStyle(fontSize: size.height * 0.021),
                  ),
                ),
              ),
            ],
          ),
        ));
  }
}
