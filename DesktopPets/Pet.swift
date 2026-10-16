import CoreGraphics

struct Pet: Identifiable, Hashable {
    let id: String
    let name: String
    let imageName: String
    let phase: Double
    let baseScale: CGFloat
    let accessibilityLabel: String
}

struct Motion: Equatable {
    let horizontal: CGFloat
    let vertical: CGFloat
    let rotation: Double

    static let zero = Motion(horizontal: 0, vertical: 0, rotation: 0)
}
