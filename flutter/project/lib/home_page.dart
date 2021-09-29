import 'package:flutter/material.dart';
import 'package:project/client.dart';

class HomePage extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<HomePage> {
  var text = "Aqui aparece a resposta"; // Texto que sera exibido

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
                      var client = new Client(); // Cliente

                      var animal =
                          await client.setValue(key: 'animal', value: 'Cão');
                      var mode = await client.setValue(
                          key: 'mode', value: 'Aproximação');
                      var quantity =
                          await client.setValue(key: 'quantity', value: 100);

                      var getMode = await client.getValue('mode');

                      this.text = 'Resposta: ${quantity.toString()}';
                      setState(() {});
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
