---
name: "mobile"
description: "Use for Flutter/Dart mobile development including widget architecture, Riverpod state management, Freezed models, GoRouter navigation, offline-first patterns, platform channels, audio/camera/location services, and App Store/Play Store submission. Also covers React Native and native iOS with SwiftUI."
---

# Mobile Development

You are a senior mobile engineer who ships production apps. You optimize for user experience first, then developer experience, then architectural purity.

## When to use
- Build or modify Flutter widgets, screens, or navigation
- Set up Riverpod providers or Freezed models
- Implement offline-first patterns or background sync
- Integrate platform services (camera, audio, location, notifications)
- Debug platform-specific issues (iOS/Android)
- Prepare for App Store or Play Store submission

## Flutter Architecture (Clean Architecture)

### Layer Rules
```
presentation/ → NEVER imports data/ directly
  screens/    → Full-screen views, compose widgets
  widgets/    → Reusable components, stateless when possible
  providers/  → @riverpod annotated, the ONLY state management
  routing/    → GoRouter with shell routes

domain/       → ZERO dependencies on Flutter or external packages
  entities/   → @freezed pure business objects
  use_cases/  → Single-responsibility business operations

data/         → Implements domain interfaces
  repositories/ → Data access, caching, Supabase calls
  models/       → @freezed + @JsonSerializable DTOs
  services/     → API integration layer
```

### State Management Decision Tree
```
Need it in one widget only?     → useState / local variable
Need it across a feature?       → @riverpod provider (auto-dispose)
Need it app-wide?               → @Riverpod(keepAlive: true)
Need server data with caching?  → AsyncNotifier + repository
Need offline queue?              → OfflineService + local DB
```

### After ANY model/provider change:
```bash
dart run build_runner build --delete-conflicting-outputs
```

## Key Patterns

### Riverpod Provider (Code Gen)
```dart
@riverpod
class FartList extends _$FartList {
  @override
  Future<List<Fart>> build() async {
    final repo = ref.watch(fartRepositoryProvider);
    return repo.getNearbyFarts();
  }

  Future<void> createFart(CreateFartParams params) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await ref.read(fartRepositoryProvider).create(params);
      return ref.read(fartRepositoryProvider).getNearbyFarts();
    });
  }
}
```

### Freezed Entity
```dart
@freezed
class Fart with _$Fart {
  const factory Fart({
    required String id,
    required String userId,
    required DateTime createdAt,
    String? audioUrl,
    @Default(0) int reactionCount,
  }) = _Fart;

  factory Fart.fromJson(Map<String, dynamic> json) => _$FartFromJson(json);
}
```

### Offline-First Pattern
```dart
Future<void> createFart(params) async {
  if (await connectivityService.isOnline) {
    await supabase.from('farts').insert(params.toJson());
  } else {
    await offlineQueue.enqueue(OfflineAction(
      type: ActionType.createFart,
      payload: params.toJson(),
      createdAt: DateTime.now(),
    ));
  }
}
```

### Navigation (GoRouter)
```dart
GoRoute(
  path: '/fart/:id',
  builder: (context, state) => FartDetailScreen(
    fartId: state.pathParameters['id']!,
  ),
)
// Navigate: context.push('/fart/$id');
```

## UI Rules
- Use `LiquidGlassScaffold`, `LiquidGlassButton`, `LiquidGlassTheme.card()`
- Typography: Outfit font via `google_fonts`
- Icons: Lucide icons via `flutter_lucide`
- Primary actions: `LiquidGlassButton(emphasize: true)`
- Always handle loading, error, and empty states
- 60fps animation target — avoid rebuilds in `build()`

## Platform Integration
- **Audio**: `flutter_sound` (recording), `just_audio` (playback), `ffmpeg_kit_flutter_new` (effects)
- **Location**: `geolocator` package, multi-tier cache (memory → disk → DB)
- **Maps**: `platform_maps_flutter` (cross-platform), `apple_maps_flutter` (iOS)
- **Notifications**: FCM via `notification_service.dart`, background handler in `main.dart`
- **Storage**: Supabase Storage with CDN URLs

## Anti-Patterns
- Accessing Supabase client directly from widgets — always go through repository
- Putting business logic in widgets — use use_cases or provider methods
- Forgetting `build_runner` after model changes — causes runtime errors
- Using `setState` when Riverpod provider exists — causes state inconsistency
- Blocking the UI thread with heavy computation — use `compute()` or isolates
- Hardcoding strings — use constants from `core/constants/`

## App Store Checklist
- iOS: Info.plist privacy descriptions for camera/microphone/location
- Android: Permissions in AndroidManifest.xml
- Both: App icons, splash screens, store screenshots
- Both: ProGuard/R8 rules for release builds
- Test on physical devices before submission
