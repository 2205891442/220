# iOS 桌面宠物 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成一个可在 Xcode 中打开的 SwiftUI iOS 桌面宠物应用，两只宠物持续蹦跳，点击后暂停约 2 秒并显示摸头反馈。

**Architecture:** 使用 SwiftUI 的 `TimelineView(.animation)` 根据时间计算每只宠物的位移和旋转；每只宠物独立维护暂停状态与恢复任务。场景由渐变背景、状态文案、两个 `PetView` 和反馈贴纸组成，资源使用本地 PNG/WebP，不依赖网络或第三方库。

**Tech Stack:** Swift 5.9、SwiftUI、Xcode 15+、iOS 16+、Python Pillow（仅用于一次性图片处理与资源检查）。

**Spec:** `docs/superpowers/specs/2026-10-16-ios-desktop-pet-design.md`

## Global Constraints

- 应用内全屏桌面场景；不实现系统主屏幕悬浮宠物。
- 两只宠物相互独立；点击只暂停被点击的宠物。
- 点击后反馈显示约 2 秒并自动恢复蹦跳；重复点击刷新计时。
- 不引入第三方 Swift 依赖；动画不依赖网络。
- 资源外部白底需要透明化，宠物身体内部白色必须保留。
- 所有图片资源放入 `DesktopPets/Resources.xcassets`，名字固定为 `cat`、`budgie`、`pat-sticker`。

---

### Task 1: Scaffold the Xcode project and resource layout

**Files:**
- Create: `DesktopPets/DesktopPetsApp.swift`
- Create: `DesktopPets/ContentView.swift`
- Create: `DesktopPets/Resources.xcassets/Contents.json`
- Create: `DesktopPets/Resources.xcassets/cat.imageset/Contents.json`
- Create: `DesktopPets/Resources.xcassets/budgie.imageset/Contents.json`
- Create: `DesktopPets/Resources.xcassets/pat-sticker.imageset/Contents.json`
- Create: `DesktopPets.xcodeproj/project.pbxproj`
- Create: `DesktopPets/Info.plist`
- Create: `DesktopPets/README.md`

**Interfaces:**
- Produces an iOS application target named `DesktopPets` with `ContentView` as the root view.
- Asset catalog names are consumed by `Image("cat")`, `Image("budgie")`, and `Image("pat-sticker")`.

- [ ] **Step 1: Create the minimum app entry point**

```swift
import SwiftUI

@main
struct DesktopPetsApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

- [ ] **Step 2: Create a placeholder root view**

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Desktop Pets")
    }
}
```

- [ ] **Step 3: Add the Xcode project metadata**

Set the target platform to iOS, minimum deployment target to iOS 16.0, product name to `DesktopPets`, and include every Swift source and asset catalog path in the target’s build phase. Keep signing unset so the user can select their own team in Xcode.

- [ ] **Step 4: Verify the scaffold statically**

Run `rg -n "@main|WindowGroup|ContentView|IPHONEOS_DEPLOYMENT_TARGET|Resources.xcassets" DesktopPets DesktopPets.xcodeproj` and confirm each required entry exists exactly once.

- [ ] **Step 5: Commit the scaffold**

```text
git add DesktopPets DesktopPets.xcodeproj
git commit -m "feat: scaffold SwiftUI desktop pets app"
```

### Task 2: Process and validate the image assets

**Files:**
- Create: `work/process_assets.py`
- Create: `DesktopPets/Resources.xcassets/cat.imageset/cat.png`
- Create: `DesktopPets/Resources.xcassets/budgie.imageset/budgie.png`
- Create: `DesktopPets/Resources.xcassets/pat-sticker.imageset/pat-sticker.png`
- Modify: `DesktopPets/README.md`

**Interfaces:**
- Produces RGBA PNGs with the asset names from Task 1.
- The processor takes the two JPG paths from `D:\Downloads`, floods only edge-connected near-white pixels to alpha 0, and writes 1024px-bounded PNGs.

- [ ] **Step 1: Write the deterministic image processor**

Use Pillow to load each source as RGBA, perform a four-neighbor flood fill from all image edges with a near-white threshold of `red > 245`, `green > 245`, and `blue > 245`, set only the connected region alpha to zero, and save the result. Do not remove white pixels that are enclosed by non-white pixels.

- [ ] **Step 2: Produce the two pet PNGs**

Run `python work/process_assets.py --source-dir "D:\\Downloads" --out "DesktopPets\\Resources.xcassets"`. The script must select the file containing `MsgID=2324219253546966734` as the cat source and the file containing `MsgID=4784028547053439212` as the budgie source, failing with a clear message if either is missing.

- [ ] **Step 3: Add the pat sticker asset**

If `C:\Users\Administrator\Desktop\OIP.webp` is available, convert it to `pat-sticker.png`. If it is unavailable in the workspace, create a clearly documented temporary PNG with the same 474×474 canvas using a light speech-bubble background and a hand/paw mark, and record the replacement path in `DesktopPets/README.md` so the supplied image can be swapped without code changes.

- [ ] **Step 4: Verify asset properties**

Run a Pillow check that all three images open, have mode `RGBA`, have non-zero alpha pixels, and have width and height between 1 and 1024. Confirm the two pet assets have transparent pixels at all four corners.

- [ ] **Step 5: Commit the assets**

```text
git add DesktopPets/Resources.xcassets work/process_assets.py DesktopPets/README.md
git commit -m "feat: add transparent pet and pat sticker assets"
```

### Task 3: Implement the pet model and animated interaction

**Files:**
- Create: `DesktopPets/Pet.swift`
- Create: `DesktopPets/PetView.swift`
- Create: `DesktopPets/PatStickerView.swift`

**Interfaces:**
- `Pet` exposes `id`, `name`, `imageName`, `phase`, `baseScale`, and `accessibilityLabel`.
- `PetView` initializer is `PetView(pet: Pet, anchor: CGPoint, size: CGFloat)`; it owns its pause state and handles its own tap gesture.
- `PatStickerView` initializer is `PatStickerView(isVisible: Bool, size: CGFloat)`.
- `Motion` is an internal `Equatable` struct with `vertical`, `horizontal`, and `rotation` fields used to freeze the current frame.

- [ ] **Step 1: Add a pure pet model**

```swift
struct Pet: Identifiable, Hashable {
    let id: String
    let name: String
    let imageName: String
    let phase: Double
    let baseScale: CGFloat
    let accessibilityLabel: String
}
```

- [ ] **Step 2: Implement time-based motion**

In `PetView`, use `TimelineView(.animation)` and `TimelineView.Context.date.timeIntervalSinceReferenceDate`. Compute `wave = sin((time + pet.phase) * 2.2)`, `vertical = wave * 10`, `horizontal = cos((time + pet.phase) * 1.4) * 3`, and `rotation = Angle.degrees(sin((time + pet.phase) * 1.4) * 2)`. When paused, freeze the last computed offset and rotation.

- [ ] **Step 3: Implement independent pause and auto-resume**

Store `@State private var pausedUntil: Date?`, `@State private var frozenMotion: Motion = .zero`, and `@State private var resumeTask: Task<Void, Never>?`. On tap, capture the current motion, set `pausedUntil = Date().addingTimeInterval(2)`, cancel the previous task, then create a new `Task` that sleeps for 2 seconds and clears the state on the main actor. Disable animation only for the pet’s motion while paused; keep sticker transitions animated.

- [ ] **Step 4: Add the feedback sticker**

Overlay `PatStickerView` above the pet image, anchored near the top leading area. Animate `opacity` from 0 to 1 and `scaleEffect` from 0.78 to 1.0 when `pausedUntil != nil`; add a soft shadow and `allowsHitTesting(false)` so the sticker never blocks the pet tap target.

- [ ] **Step 5: Add accessibility and hit testing**

Wrap the image in a `contentShape(Rectangle())`, attach `.onTapGesture`, use `.accessibilityLabel(pet.accessibilityLabel)`, and expose `.accessibilityHint("点击后暂停约两秒并显示摸头表情")`.

- [ ] **Step 6: Commit the interaction component**

```text
git add DesktopPets/Pet.swift DesktopPets/PetView.swift DesktopPets/PatStickerView.swift
git commit -m "feat: add independent pet bounce and pat interaction"
```

### Task 4: Build the full desktop scene

**Files:**
- Modify: `DesktopPets/ContentView.swift`
- Create: `DesktopPets/PetStageView.swift`

**Interfaces:**
- `PetStageView` owns the two `Pet` values and renders two `PetView` instances in a `GeometryReader`.
- `ContentView` only provides safe-area handling and the root background.

- [ ] **Step 1: Add the responsive stage layout**

Use a `GeometryReader` with a `ZStack(alignment: .bottom)`; position the cat at `x = width * 0.30`, the budgie at `x = width * 0.70`, and use `y = height * 0.70` with each image sized to `min(width * 0.36, 170)`.

- [ ] **Step 2: Add the desktop visual treatment**

Create a `LinearGradient` from `Color(red: 0.28, green: 0.35, blue: 0.60)` to `Color(red: 0.10, green: 0.12, blue: 0.24)`, add two low-opacity blurred circles in the background, and add a bottom glass panel with the text `轻点小动物，摸摸头`.

- [ ] **Step 3: Render both pets with independent callbacks**

Pass `Pet(id: "cat", name: "猫", imageName: "cat", phase: 0, baseScale: 1.0, accessibilityLabel: "猫，点击摸摸头")` and `Pet(id: "budgie", name: "虎皮鹦鹉", imageName: "budgie", phase: 1.7, baseScale: 0.92, accessibilityLabel: "虎皮鹦鹉，点击摸摸头")` to the two `PetView` instances.

- [ ] **Step 4: Verify scene geometry in previews**

Add SwiftUI previews for a 393×852 portrait layout and a 852×393 landscape layout. Confirm no asset is clipped, the two tap targets do not overlap, and the bottom panel respects safe-area insets.

- [ ] **Step 5: Commit the scene**

```text
git add DesktopPets/ContentView.swift DesktopPets/PetStageView.swift
git commit -m "feat: compose responsive desktop pet scene"
```

### Task 5: Add documentation and run the verification pass

**Files:**
- Modify: `DesktopPets/README.md`
- Create: `work/verify_assets.py`

**Interfaces:**
- README explains how to open `DesktopPets.xcodeproj`, select a simulator, replace the sticker asset if needed, and run.
- Verification script checks asset names, alpha channels, and required Swift symbols.

- [ ] **Step 1: Document Xcode setup and behavior**

Include the minimum Xcode/iOS versions, the iOS home-screen limitation, the exact tap behavior, and the three asset names. Explain that the provided source images are bundled locally and no network access is needed.

- [ ] **Step 2: Run static verification**

Run `python work/verify_assets.py`; it must exit 0 and print a line for each image and each required Swift file. Run `rg -n "TimelineView|pausedUntil|PatStickerView|accessibilityLabel|LinearGradient" DesktopPets` and confirm all behavior anchors are present.

- [ ] **Step 3: Perform a clean-tree check**

Run `git status --short` and confirm only intentional source, asset, and documentation files are present. If macOS/Xcode is available later, open the project and run the iPhone 15 simulator checks listed in the design spec.

- [ ] **Step 4: Commit the verification documentation**

```text
git add DesktopPets/README.md work/verify_assets.py
git commit -m "docs: add run instructions and verification checks"
```
