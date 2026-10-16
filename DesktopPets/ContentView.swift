import SwiftUI

struct ContentView: View {
    var body: some View {
        PetStageView()
            .ignoresSafeArea()
            .preferredColorScheme(.dark)
    }
}

#Preview("Portrait") {
    ContentView()
        .frame(width: 393, height: 852)
}

#Preview("Landscape") {
    ContentView()
        .frame(width: 852, height: 393)
}
