# FWF UI Architecture

- Theme owner: `lib/core/theme/fwf_theme.dart`, `tokens.dart`, and `app_design_system.dart`.
- Expressive theme and shared atmosphere: `lib/core/theme/toxic_candy_theme.dart` and `lib/core/widgets/fwf_atmospheric_stage.dart`.
- Shell owner: `lib/presentation/widgets/common/snap_shell_scaffold.dart`.
- Global fart action: `lib/presentation/widgets/common/fart_button.dart`.
- Incoming listen/reaction: `lib/presentation/screens/social/incoming_fart_screen.dart` plus reaction capture service/provider.
- Public map: `lib/presentation/screens/map/fart_map_screen.dart` plus its provider/repository.
- Use presentation → domain → data dependency direction; widgets never access Supabase directly.
- Use existing Lucide-style utility icons and the app image asset for the product mark.
- Run build_runner after annotated provider/model changes.
