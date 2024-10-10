import 'dart:io';

import 'package:client/core/constants/server_constants.dart';
import 'package:http/http.dart' as http;

class HomeRepository {
  Future<void> uploadSong(File selectedImage, File selectedAudio,) async {
    final request = http.MultipartRequest(
        'POST', Uri.parse('${ServerConstants.baseUrl}/song/upload'));

    request
      ..files.addAll(
        [
          await http.MultipartFile.fromPath(
              'song', selectedAudio.path),
          await http.MultipartFile.fromPath(
              'thumbnail', selectedImage.path),
        ],
      )
      ..fields.addAll(
        {
          'artist': 'Taylor',
          'song_name': 'Love Story',
          'hex_code': '#FFFFFF',
        },
      )
      ..headers.addAll(
        {
          'x-auth-token':
              'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjliMDY5ZmY0LWI0ZmUtNDc4ZS1iOGU5LWJkNzUzNzQyMWNmZiJ9.Q2vts1hcmaTORCh9085YXf6HGozCwM5GJ77zrdXigUI'
        },
      );

    final res = await request.send();
    print(res);
  }
}
