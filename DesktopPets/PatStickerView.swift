import SwiftUI

struct PatStickerView: View {
    let isVisible: Bool
    let size: CGFloat

    var body: some View {
        Image("pat-sticker")
            .resizable()
            .scaledToFit()
            .frame(width: size, height: size)
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: size * 0.18))
            .clipShape(RoundedRectangle(cornerRadius: size * 0.18))
            .shadow(color: .black.opacity(0.28), radius: 14, y: 8)
            .scaleEffect(isVisible ? 1 : 0.78)
            .opacity(isVisible ? 1 : 0)
            .allowsHitTesting(false)
            .animation(.spring(response: 0.36, dampingFraction: 0.74), value: isVisible)
    }
}
