import SwiftUI

struct PetStageView: View {
    private let cat = Pet(
        id: "cat",
        name: "猫",
        imageName: "cat",
        phase: 0,
        baseScale: 1.0,
        accessibilityLabel: "猫，点击摸摸头"
    )

    private let budgie = Pet(
        id: "budgie",
        name: "虎皮鹦鹉",
        imageName: "budgie",
        phase: 1.7,
        baseScale: 0.92,
        accessibilityLabel: "虎皮鹦鹉，点击摸摸头"
    )

    var body: some View {
        GeometryReader { proxy in
            let size = min(proxy.size.width * 0.36, 170)
            let baseline = proxy.size.height * 0.70

            ZStack {
                background

                PetView(
                    pet: cat,
                    anchor: CGPoint(x: proxy.size.width * 0.30, y: baseline),
                    size: size
                )

                PetView(
                    pet: budgie,
                    anchor: CGPoint(x: proxy.size.width * 0.70, y: baseline),
                    size: size * 0.90
                )

                VStack(spacing: 6) {
                    Text("DESKTOP PETS")
                        .font(.system(size: 12, weight: .semibold, design: .rounded))
                        .tracking(2.4)
                        .foregroundStyle(.white.opacity(0.62))

                    Text("轻点小动物，摸摸头")
                        .font(.system(size: 17, weight: .medium, design: .rounded))
                        .foregroundStyle(.white.opacity(0.94))
                }
                .padding(.horizontal, 24)
                .padding(.vertical, 16)
                .background(.ultraThinMaterial, in: Capsule())
                .overlay(Capsule().stroke(.white.opacity(0.16), lineWidth: 1))
                .shadow(color: .black.opacity(0.16), radius: 20, y: 10)
                .frame(maxHeight: .infinity, alignment: .bottom)
                .padding(.bottom, max(proxy.safeAreaInsets.bottom, 20))
            }
        }
    }

    private var background: some View {
        ZStack {
            LinearGradient(
                colors: [
                    Color(red: 0.28, green: 0.35, blue: 0.60),
                    Color(red: 0.10, green: 0.12, blue: 0.24)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            Circle()
                .fill(Color.white.opacity(0.12))
                .frame(width: 260)
                .blur(radius: 8)
                .offset(x: -130, y: -230)

            Circle()
                .fill(Color.cyan.opacity(0.12))
                .frame(width: 220)
                .blur(radius: 8)
                .offset(x: 150, y: 160)
        }
        .ignoresSafeArea()
    }
}
