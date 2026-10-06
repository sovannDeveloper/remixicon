# Remix Icon for Flutter: Knowledge Base

How to use this package and how to maintain it. The README is the short public intro. This
file holds everything else.

| | |
|---|---|
| Package | `remixicon` 1.4.0 |
| Upstream icon set | Remix Icon **v4.9.1** (2026-01-29), **3229 icons** |
| SDK | Dart `>=3.0.0 <4.0.0`, Flutter `>=3.10.0` |
| Repo (this fork) | `git@github.com:sovannDeveloper/remixicon.git` |
| Upstream icons | https://github.com/Remix-Design/RemixIcon · browse at https://remixicon.com |

---

## 1. Using the package

### 1.1 Install

The package is consumed from git, not pub.dev:

```yaml
dependencies:
  remixicon:
    git: https://github.com/sovannDeveloper/remixicon.git
    # Pin a commit or tag so upstream renumbering can't surprise you:
    # git:
    #   url: https://github.com/sovannDeveloper/remixicon.git
    #   ref: bfb6caa
```

To work on the package locally from another app, use `path: ../remixicon`.

### 1.2 Basic usage

```dart
import 'package:flutter/material.dart';
import 'package:remixicon/remixicon.dart';

Icon(Remix.home_3_line)
Icon(Remix.home_3_fill, size: 32, color: Colors.teal)

IconButton(
  icon: const Icon(Remix.settings_3_line),
  tooltip: 'Settings',
  onPressed: () {},
)
```

Every icon is a `static const IconData` on the `Remix` class. Anything that takes an
`IconData` accepts it: `Icon`, `IconButton`, `NavigationDestination`,
`BottomNavigationBarItem`, `ListTile(leading: …)`, `InputDecoration(prefixIcon: …)`, `Chip`,
`FloatingActionButton`, and so on.

### 1.3 Size, color, and theme

`Icon` takes its size and color from the nearest `IconTheme`, so you can style many icons at once:

```dart
IconTheme(
  data: const IconThemeData(size: 20, color: Colors.black54),
  child: Row(children: const [
    Icon(Remix.heart_line),
    Icon(Remix.share_line),
    Icon(Remix.bookmark_line),
  ]),
)
```

App-wide: set `ThemeData(iconTheme: …)`. The glyphs are drawn on a **24×24 grid**, so they
look sharpest at 24, 48, 12, and other multiples of 12.

### 1.4 Outlined vs. filled (active state)

Most icons come as a pair: `_line` (outlined) and `_fill` (filled). A common pattern is to
show the line version normally and the fill version when selected:

```dart
NavigationBar(
  destinations: const [
    NavigationDestination(
      icon: Icon(Remix.home_5_line),
      selectedIcon: Icon(Remix.home_5_fill),
      label: 'Home',
    ),
    NavigationDestination(
      icon: Icon(Remix.user_3_line),
      selectedIcon: Icon(Remix.user_3_fill),
      label: 'Profile',
    ),
  ],
)
```

```dart
Icon(isLiked ? Remix.heart_fill : Remix.heart_line,
     color: isLiked ? Colors.red : null)
```

### 1.5 Accessibility

Icon fonts carry no meaning for screen readers. Add a label when the icon is the only content:

```dart
const Icon(Remix.delete_bin_line, semanticLabel: 'Delete')
```

`IconButton(tooltip: …)` also supplies the semantics label.

### 1.6 Icons in text

```dart
Text.rich(TextSpan(children: [
  WidgetSpan(child: Icon(Remix.map_pin_line, size: 16)),
  const TextSpan(text: ' Phnom Penh'),
]))
```

### 1.7 Looking up icons by name (e.g. from an API)

Dart has no reflection in Flutter, so `Remix['home_line']` is not possible. Build your own map
of only the icons you need. Keep the values as **const references**:

```dart
const Map<String, IconData> kCategoryIcons = {
  'food': Remix.restaurant_line,
  'shop': Remix.shopping_bag_3_line,
  'car': Remix.car_line,
};

Icon(kCategoryIcons[category] ?? Remix.question_line)
```

**Never** construct `IconData(0xeXXX, fontFamily: 'Remix', fontPackage: 'remixicon')` at
runtime from a stored codepoint. This has two problems:
1. Release builds tree-shake icon fonts, so runtime `IconData` fails the build
   ("This application cannot tree shake icons fonts…"). The only escape is
   `--no-tree-shake-icons`, which ships the whole font.
2. Upstream **renumbers codepoints** between releases (see §3.4), so stored codepoints break
   after an upgrade. Store icon *names* instead.

---

## 2. Finding the right icon name

1. Search on https://remixicon.com. The site shows names like `ri-home-3-line`.
2. Convert the name: drop `ri-` and replace `-` with `_`. For example, `ri-home-3-line` becomes `Remix.home_3_line`.
3. Names that start with a digit are spelled out, because Dart identifiers can't begin with
   one:

   | Remix Icon CSS | Dart |
   |---|---|
   | `ri-24-hours-fill` / `-line` | `Remix.twenty_four_hours_fill` / `_line` |
   | `ri-4k-fill` / `-line` | `Remix.four_k_fill` / `_line` |

4. Suffixes:
   - `_line`: outlined version
   - `_fill`: filled version
   - no suffix: single-style icons, mostly editor/formatting ones (`bold`, `h_1`,
     `align_left`, `code_view`, `double_quotes_l`, `font_size`, …). 3078 of the 3229 icons
     have `_fill`/`_line`. The other 151 don't.

You can also search the source directly:

```sh
grep -o 'IconData [a-z0-9_]*wallet[a-z0-9_]*' lib/remixicon.dart
```

### Renamed/removed upstream

| Version | Change |
|---|---|
| 1.4.0 (RI 4.9.1) | `Remix.font_sans` **removed**. Use `Remix.font_sans_serif`. |

When an upgrade breaks a name, check the upstream release notes and add the change to this table and to
`CHANGELOG.md`.

---

## 3. Maintaining the package

### 3.1 File map

| Path | What it is | Edited by hand? |
|---|---|---|
| `lib/remixicon.dart` | The `Remix` class: one `static const IconData` per icon | **No.** Generated |
| `fonts/remixicon.css` | Upstream CSS, copied verbatim. Source of truth for names and codepoints | No |
| `fonts/Remix.ttf` | Upstream `remixicon.ttf`, renamed | No |
| `tool/generate.py` | Regenerates `lib/remixicon.dart` from the CSS | Yes |
| `pubspec.yaml` | Declares font family `Remix` → `fonts/Remix.ttf`, plus the package version | Yes |
| `CHANGELOG.md` | Per-release notes | Yes |
| `README.md` | Public intro. Contains the upstream version string | Yes |
| `example/` | Demo app (path dependency on `../`). Its title shows the RI version | Yes |
| `images/` | Logo/preview used by the README and the pubspec `screenshots` | Rarely |

How the pieces connect: `pubspec.yaml` registers the font as family **`Remix`**, and the
generated code uses `fontFamily: 'Remix', fontPackage: 'remixicon'`. Flutter resolves this to
`packages/remixicon/Remix`. If you rename the family, the package, or the font asset, change both
sides together.

### 3.2 Upgrading to a new Remix Icon release

1. Download `RemixIcon_Fonts_v<X.Y.Z>.zip` from
   https://github.com/Remix-Design/RemixIcon/releases.
2. From the zip, copy:
   - `remixicon.css` → `fonts/remixicon.css` (verbatim)
   - `remixicon.ttf` → `fonts/Remix.ttf` (renamed)
3. Regenerate:
   ```sh
   python3 tool/generate.py
   ```
4. Verify (see §3.3).
5. Look at the diff for **removed** identifiers. These are breaking changes:
   ```sh
   git diff lib/remixicon.dart | grep '^-  static const IconData' | sed -E 's/.*IconData ([a-z0-9_]+).*/\1/' | sort > /tmp/old
   git diff lib/remixicon.dart | grep '^+  static const IconData' | sed -E 's/.*IconData ([a-z0-9_]+).*/\1/' | sort > /tmp/new
   comm -23 /tmp/old /tmp/new   # removed names (breaking)
   comm -13 /tmp/old /tmp/new   # added names
   ```
   Changed codepoints show up as -/+ pairs with the same name. These are expected and not breaking.
6. Bump the versions and docs:
   - `pubspec.yaml` `version:`: minor for an icon update, and also note any breaking removals
   - `CHANGELOG.md`: new entry with the upstream version, date, number of added icons, and removals
   - `README.md`: the upstream version string and the icon count
   - `example/lib/main.dart`: the AppBar title version
   - this file: the header table and the "Renamed/removed upstream" table
   - check whether the upstream **license** changed (it moved from Apache 2.0 to the Remix Icon
     License 1.0 in 4.9.1)
7. Run the example app and check that an icon renders: `cd example && flutter run`.
8. Commit, e.g. `update to vX.Y.Z`.

### 3.3 Verification

- **Generator is deterministic.** On an unchanged CSS, `python3 tool/generate.py` must leave
  `git status` clean. This was checked against v4.9.1: the output matches byte for byte.
- **Icon count** matches the CSS:
  ```sh
  grep -c 'static const IconData' lib/remixicon.dart
  grep -c '^\.ri-.*:before' fonts/remixicon.css
  ```
- **Every codepoint exists in the TTF** (needs `pip install fonttools`):
  ```sh
  python3 - <<'PY'
  import re
  from fontTools.ttLib import TTFont
  cmap = TTFont('fonts/Remix.ttf').getBestCmap()
  cps = [int(h, 16) for h in re.findall(r'IconData\(0x([0-9a-f]+)', open('lib/remixicon.dart').read())]
  missing = [hex(c) for c in cps if c not in cmap]
  print(len(cps), 'codepoints,', len(missing), 'missing', missing[:10])
  PY
  ```
- `flutter analyze` from the repo root.

### 3.4 Generation rules (what `tool/generate.py` does)

- File header = the CSS's leading `/* … */` comment with every `-` replaced by `_`. This is
  inherited from the original generator and kept for byte compatibility.
- Parse `.ri-<name>:before { content: "\<hex>"; }` **in source order**.
- Identifier = `<name>` with `-` → `_`, plus the four numeric-leading exceptions in §2.
- One declaration per line. If the line is longer than **100 columns**, break after `=` and indent the
  `IconData(...)` by 6 spaces.
- Always regenerate the **whole file**. Never append new entries by hand. Upstream assigns
  codepoints sequentially, so removing one icon shifts everything after it. In 4.9.1, removing
  `font-sans` shifted 607 codepoints.

### 3.5 Gotchas

- **Don't format `lib/remixicon.dart`.** Don't run `dart format`, and don't save it in VS Code.
  `.vscode/settings.json` has `formatOnSave: true` for Dart, and the current SDK's "tall"
  formatter reflows the entire 4k-line file, which produces a huge meaningless diff. If it
  happens, run `python3 tool/generate.py` to restore it.
- Identifiers are `snake_case` on purpose (they match upstream names), so expect
  `non_constant_identifier_names` lint hints. They're harmless.
- `pubspec.yaml`'s `repository:` still points to the original `alialnaghmoush/remixicon`,
  and `LICENSE` is the inherited MIT (Jonny Borges, 2019) license for the Dart wrapper code.
  The icon glyphs themselves are covered by the Remix Icon License 1.0.
- `example/android` is from an old Flutter template. If the example won't build, regenerate the
  platform folders with `flutter create .` inside `example/`.

---

## 4. Version history (summary)

| Package | Remix Icon | Date | Notes |
|---|---|---|---|
| 1.4.0 | 4.9.1 | 2026-01-29 | +172 icons → 3229. `font_sans` removed. License changed to Remix Icon License 1.0 |
| 1.3.0 | 4.5.0 | 2024-10-28 | |
| 1.2.0 | 4.2.0 | 2024-02-25 | |
| 1.1.1 | – | – | Added the pubspec screenshot/logo |
| 1.1.0 | 4.1.0 | 2024-01-14 | |
| 1.0.0 | 2.5.0 | – | Initial build |

The full notes are in `CHANGELOG.md`.
