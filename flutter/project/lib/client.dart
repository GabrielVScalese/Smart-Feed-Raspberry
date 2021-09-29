import 'package:dio/dio.dart';

// Classe cliente para consumo de API Flask
class Client {
  Dio dio;

  // No construtor se define o objeto de consumo de api
  Client() {
    this.dio = new Dio();
    dio.options.headers = {
      "content-type": "application/json"
    }; // Seta headers para aceitar envio de JSON
  }

  // Requisicao para setar valores do Raspberry PI a partir do key (animal, mode, quantity or schedules)
  getValue(String key) async {
    try {
      var response = await dio.get('http://192.168.0.12:5000/$key');

      return response.data;
    } catch (err) {}
  }

  // Requisicao para setar valores do Raspberry PI a partir do key (animal, mode, quantity or schedules)
  setValue({String key, dynamic value}) async {
    try {
      var response = await dio
          .post('http://192.168.0.12:5000/$key', data: {'$key': value});

      return response.data;
    } catch (err) {}
  }
}
