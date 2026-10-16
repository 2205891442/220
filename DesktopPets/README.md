# Desktop Pets

这是一个使用 SwiftUI 编写的 iOS 桌面宠物示例。打开工程后，猫和虎皮鹦鹉会在应用内的桌面场景中持续轻微蹦跳。

## 运行

1. 在 macOS 上使用 Xcode 15 或更高版本打开 `DesktopPets.xcodeproj`。
2. 选择 iOS 16 或更高版本的 iPhone 模拟器或真机。
3. 在 Signing & Capabilities 中选择你自己的开发团队，然后运行 `DesktopPets` target。

## 交互

- 点击猫或虎皮鹦鹉后，被点击的宠物会立即停住。
- 头顶会出现 `pat-sticker` 摸头贴纸，约 2 秒后贴纸消失，宠物自动恢复蹦跳。
- 两只宠物互相独立，点击其中一只不会停止另一只。
- 这是一个应用内桌面场景。iOS 普通应用不能在系统主屏幕上持续绘制可交互的漂浮宠物。

## 资源

资源目录是 `Resources.xcassets`，固定使用以下名字：

- `cat`：第一张猫的图片，已将外部白底处理为透明。
- `budgie`：第二张虎皮鹦鹉图片，已将外部白底处理为透明。
- `pat-sticker`：参照你提供的摸头表情绘制的本地贴纸。原始 `OIP.webp` 未出现在当前工作区，所以用本地绘制版本保证工程可以直接运行；替换时只需要用同名 PNG 覆盖 `pat-sticker.imageset/pat-sticker.png`，无需修改 Swift 代码。

本地贴纸的构图参考了你提供的图片和开放素材库 OpenMoji 的手部图形风格；应用不运行时下载网络资源，也不会把图片上传到任何网站。
