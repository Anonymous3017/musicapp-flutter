import 'dart:io';
import 'package:client/core/providers/current_user_notifier.dart';
import 'package:client/core/utils.dart';
import 'package:client/features/home/models/song_model.dart';
import 'package:client/features/home/repositories/home_local_repository.dart';
import 'package:client/features/home/repositories/home_repository.dart';
import 'package:flutter/material.dart';
import 'package:fpdart/fpdart.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'home_viewmodel.g.dart';

@riverpod
Future<List<SongModel>> getAllSongs(GetAllSongsRef ref) async {
  final token = ref.watch(currentUserNotifierProvider)?.token ?? '';
  final res = await ref.watch(homeRepositoryProvider).getAllSongs(
        token: token,
      );
  final val = switch (res) {
    Left(value: final l) => throw l.message,
    Right(value: final r) => r,
  };

  return val;
}

@riverpod
class HomeViewModel extends _$HomeViewModel {
  late HomeRepository _homeRepository;
  late HomeLocalRepository _homeLocalRepository;

  @override
  AsyncValue? build() {
    _homeRepository = ref.watch(homeRepositoryProvider);
    _homeLocalRepository = ref.watch(homeLocalRepositoryProvider);
    return null;
  }

  Future<void> uploadSong({
    required File selectedThumbnail,
    required File selectedAudio,
    required String artist,
    required String songName,
    required Color selectedColor,
  }) async {
    state = const AsyncValue.loading();

    final res = await _homeRepository.uploadSong(
      selectedThumbnail: selectedThumbnail,
      selectedAudio: selectedAudio,
      artist: artist,
      songName: songName,
      hexCode: rgbToHex(selectedColor),
      token: ref.read(currentUserNotifierProvider)?.token ?? '',
    );

    final val = switch (res) {
      Left(value: final l) => state =
          AsyncValue.error(l.message, StackTrace.current),
      Right(value: final r) => state = AsyncValue.data(r),
    };

    print(val);
  }

  List<SongModel> getRecentlyPlayedSongs() {
    final songs = _homeLocalRepository.loadSongs();
    return songs;
  }
}
