---
title: Using Remix Icon
doc_id: using_remixicon
package: remixicon
topic: ui
summary: How to use the Remix Icon Flutter package to integrate icon assets into your Flutter applications.
keywords: [remix icon, icon, flutter, ui, icons, remixicon]
related: []
---

## Remix Icon: overview

Remix Icon is a set of open-source neutral-style system symbols elaborately crafted for designers and developers. This Flutter package provides easy integration of these icons into your Flutter applications. The package includes the Remix Icon font and utilities to use the icons in your UI.

## Remix Icon: basic usage

To use Remix Icons in your Flutter application, you need to import the package and use the icon widgets.

```dart
import 'package:flutter/material.dart';
import 'package:remixicon/remixicon.dart';

class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Remix Icon Example'),
      ),
      body: Center(
        child: Icon(
          Remix.icon,
          size: 48,
          color: Colors.blue,
        ),
      ),
    );
  }
}
```

1. Import the remixicon package in your Dart file
2. Use `Icon(Remix.icon)` to display any icon from the collection
3. Customize the size and color using standard Flutter properties

## Remix Icon: icon categories

The Remix Icon collection is organized into several categories for easy navigation:

- **System Icons**: Basic system icons like home, settings, etc.
- **Editor Icons**: Text editing and formatting icons
- **Media Icons**: Audio, video, and media related icons
- **Device Icons**: Computer, phone, and device related icons
- **Business Icons**: Business and financial related icons
- **Health Icons**: Health and medical related icons

## Remix Icon: rules and pitfalls

- Always ensure the font is properly loaded before using icons
- Some icons may require specific Flutter versions or configurations
- The package uses the official Remix Icon font, so icon availability depends on the version

## Remix Icon: FAQ

**How do I find a specific icon?**
Use the Remix Icon website at remixicon.com to browse and search for icons, then use the corresponding constant from the package.

**Can I customize the icon appearance?**
Yes, you can customize the icon size, color, and other properties using standard Flutter widget properties.

**What Flutter versions are supported?**
The package supports Flutter SDK version 3.10.0 and above.