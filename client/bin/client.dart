import 'dart:convert';

import 'package:client/api/auth.dart';
import 'package:client/api/chat.dart';

final bToken =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NjkyODgwLCJpYXQiOjE3MTQzOTY4ODAsImp0aSI6ImNkYjY0NWY0ZDM1MDQ4NzY5NjU4MDAwNTkzM2QxY2M0IiwidXNlcl9pZCI6M30.L3u8wKzbchE47n_536tCiI3KZ9WSpzJJ9BELFO2Bs4M";

void main(List<String> arguments) async {
  ChatApi.connect(bToken);
  ChatApi.listen((event) {
    final data = jsonDecode(event);
    final text = data['message']['text'];
    final room = data['message']['room'];
    final defaultText = "Hello, i got yuour message";

    print('Received: $text');
    print('Room: $room');
    print("Default text: $defaultText");
    if (text != defaultText) {
      ChatApi.sendMessage({"group_id": room, "text": defaultText});
    }
  });
}
