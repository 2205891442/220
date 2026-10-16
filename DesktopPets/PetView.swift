import SwiftUI

struct PetView: View {
    let pet: Pet
    let anchor: CGPoint
    let size: CGFloat

    @State private var pausedUntil: Date?
    @State private var frozenMotion = Motion.zero
    @State private var resumeTask: Task<Void, Never>?

    private var isPaused: Bool {
        guard let pausedUntil else { return false }
        return pausedUntil > Date()
    }

    var body: some View {
        TimelineView(.animation) { context in
            let liveMotion = motion(at: context.date)
            let displayedMotion = isPaused ? frozenMotion : liveMotion

            ZStack(alignment: .topLeading) {
                Image(pet.imageName)
                    .resizable()
                    .scaledToFit()
                    .scaleEffect(pet.baseScale)
                    .frame(width: size, height: size * 1.18)
                    .contentShape(Rectangle())

                PatStickerView(isVisible: isPaused, size: size * 0.72)
                    .offset(x: size * 0.20, y: -size * 0.52)
            }
            .frame(width: size, height: size * 1.18)
            .position(
                x: anchor.x + displayedMotion.horizontal,
                y: anchor.y + displayedMotion.vertical
            )
            .rotationEffect(.degrees(displayedMotion.rotation))
            .contentShape(Rectangle())
            .onTapGesture {
                pat(at: context.date, motion: liveMotion)
            }
            .accessibilityElement(children: .ignore)
            .accessibilityLabel(pet.accessibilityLabel)
            .accessibilityHint("点击后暂停约两秒并显示摸头表情")
            .accessibilityAddTraits(.isButton)
        }
        .onDisappear {
            resumeTask?.cancel()
        }
    }

    private func motion(at date: Date) -> Motion {
        let time = date.timeIntervalSinceReferenceDate
        let phaseTime = time + pet.phase
        return Motion(
            horizontal: CGFloat(cos(phaseTime * 1.4) * 3),
            vertical: CGFloat(sin(phaseTime * 2.2) * 10),
            rotation: sin(phaseTime * 1.4) * 2
        )
    }

    private func pat(at date: Date, motion: Motion) {
        frozenMotion = isPaused ? frozenMotion : motion
        pausedUntil = date.addingTimeInterval(2)
        resumeTask?.cancel()
        resumeTask = Task { @MainActor in
            do {
                try await Task.sleep(nanoseconds: 2_000_000_000)
            } catch {
                return
            }
            guard !Task.isCancelled else { return }
            pausedUntil = nil
            resumeTask = nil
        }
    }
}
