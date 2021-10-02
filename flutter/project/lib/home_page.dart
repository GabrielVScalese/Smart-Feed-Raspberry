import 'package:flutter/material.dart';
import 'package:project/udp_socket.dart';
import 'client.dart';

class HomePage extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<HomePage> {
  // Textos que serao exibidos
  var informationText = "Aqui aparece a resposta";
  var apiText = "Aqui aparece a resposta";

  // Dados obtidos apos broadcast
  String ip = "";
  int port;

  findInformation() async {
    UDPSocket socket = new UDPSocket(1900);
    var machine = await socket.findMachine();

    return machine;
  }

  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;

    return Scaffold(
        appBar: AppBar(
          title: Text('Consumindo Raspberry Pi'),
          centerTitle: true,
        ),
        body: Container(
          height: size.height,
          width: size.width,
          child: Column(
            children: [
              SizedBox(
                height: size.height * 0.1,
              ),
              Container(
                child: Text(
                  'Descobrir dados da máquina:',
                  style: TextStyle(fontSize: size.height * 0.02),
                ),
              ),
              SizedBox(
                height: size.height * 0.02,
              ),
              Container(
                  child: Text(
                this.informationText,
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
                      var ret = await findInformation();
                      this.ip = ret[0];
                      this.port = ret[1];

                      this.informationText =
                          'IP: ${this.ip} | Port: ${this.port}';

                      print(informationText);
                      setState(() {});
                    } catch (err) {
                      print(err);
                    }
                  },
                  child: Text(
                    'Broadcast',
                    style: TextStyle(fontSize: size.height * 0.021),
                  ),
                ),
              ),
              SizedBox(
                height: size.height * 0.04,
              ),
              Divider(
                thickness: size.height * 0.01,
              ),
              SizedBox(
                height: size.height * 0.04,
              ),
              Container(
                child: Text(
                  'Consumir API:',
                  style: TextStyle(fontSize: size.height * 0.02),
                ),
              ),
              SizedBox(
                height: size.height * 0.02,
              ),
              Container(
                  child: Text(
                this.apiText,
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
                      var client = new Client(); // Cliente

                      var animal =
                          await client.setValue(key: 'animal', value: 'person');
                      var mode = await client.setValue(
                          key: 'mode', value: 'Aproximação');
                      var quantity =
                          await client.setValue(key: 'quantity', value: 100);

                      var getMode = await client.getValue('mode');

                      this.apiText = 'Resposta: ${quantity.toString()}';
                      setState(() {});
                    } catch (err) {
                      print(err);
                    }
                  },
                  child: Text(
                    'API Flask',
                    style: TextStyle(fontSize: size.height * 0.021),
                  ),
                ),
              ),
            ],
          ),
        ));
  }
}
