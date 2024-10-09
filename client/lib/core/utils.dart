import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

void showSnackBar(BuildContext context, String content, Color color) {
  ScaffoldMessenger.of(context)
    ..hideCurrentMaterialBanner()
    ..showSnackBar(
      SnackBar(
        content: Text(content),
        backgroundColor: color,
      ),
    );
}

Future<File?> pickImage() async {
  try {
    final filePickerResult = await FilePicker.platform.pickFiles(
      type: FileType.image,
      allowedExtensions: ['jpg', 'jpeg', 'png'],
    );

    if (filePickerResult != null) {
      return File(filePickerResult.files.first.xFile.path);
    }
    return null;
  } catch (e) {
    return null;
  }
}

Future<File?> pickAudio() async {
  try {
    final filePickerResult = await FilePicker.platform.pickFiles(
      type: FileType.audio,
      allowedExtensions: ['mp3'],
    );

    if (filePickerResult != null) {
      return File(filePickerResult.files.first.xFile.path);
    }
    return null;
  } catch (e) {
    return null;
  }
}
