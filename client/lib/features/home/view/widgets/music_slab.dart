import 'package:client/core/providers/current_song_notifier.dart';
import 'package:client/core/theme/app_pallete.dart';
import 'package:client/core/utils.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class MusicSlab extends ConsumerWidget {
  const MusicSlab({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentSong = ref.watch(currentSongNotifierProvider);
    final songNotifier = ref.read(currentSongNotifierProvider.notifier);

    if (currentSong == null) {
      return const SizedBox();
    }
    return Stack(
      children: [
        Container(
          height: 66,
          width: MediaQuery.of(context).size.width - 16,
          decoration: BoxDecoration(
            color: hexToColor(currentSong.hex_code),
            borderRadius: BorderRadius.circular(4),
          ),
          padding: const EdgeInsets.all(9),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    width: 48,
                    decoration: BoxDecoration(
                      image: DecorationImage(
                        image: NetworkImage(currentSong.thumbnail_url),
                        fit: BoxFit.cover,
                      ),
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        currentSong.song_name,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      Text(
                        currentSong.artist,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 14,
                          fontWeight: FontWeight.w400,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              Row(
                children: [
                  IconButton(
                    onPressed: () {},
                    icon: const Icon(
                      CupertinoIcons.heart,
                      color: Pallete.whiteColor,
                    ),
                  ),
                  IconButton(
                    onPressed: songNotifier.playPause,
                    icon: Icon(
                      songNotifier.isPlaying
                          ? CupertinoIcons.pause_fill
                          : CupertinoIcons.play_fill,
                      color: Pallete.whiteColor,
                    ),
                  ),
                ],
              )
            ],
          ),
        ),
        StreamBuilder(
            stream: songNotifier.audioPlayer?.positionStream,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const SizedBox();
              }
              final position = snapshot.data;
              final duration = songNotifier.audioPlayer!.duration;
              double sliderValue = 0.0;
              if (position != null && duration != null) {
                sliderValue = position.inMicroseconds / duration.inMicroseconds;
              }
              return Positioned(
                bottom: 0,
                left: 8,
                child: Container(
                  height: 2,
                  width: (MediaQuery.of(context).size.width - 32) * sliderValue,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(7),
                  ),
                ),
              );
            }),
        Positioned(
            bottom: 0,
            right: 8,
            child: Container(
              height: 2,
              width: MediaQuery.of(context).size.width - 32,
              decoration: BoxDecoration(
                color: Pallete.inactiveSeekColor,
                borderRadius: BorderRadius.circular(7),
              ),
            ))
      ],
    );
  }
}
