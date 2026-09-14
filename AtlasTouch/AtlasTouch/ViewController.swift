import UIKit

class ViewController: UIViewController {

    private let bridgeURL = URL(string: "http://192.168.1.159:8080/touch")!

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = touches.first else { return }

        let location = touch.location(in: view)

        let touchEvent: [String: Any] = [
            "type": "touch",
            "timestamp": ISO8601DateFormatter().string(from: Date()),
            "source": "iphone",
            "gesture": "began",
            "location": [
                "x": location.x,
                "y": location.y
            ]
        ]

        sendToBridge(touchEvent)
    }

    private func sendToBridge(_ touchEvent: [String: Any]) {
        guard let jsonData = try? JSONSerialization.data(
            withJSONObject: touchEvent,
            options: []
        ) else {
            print("Failed to encode touch event")
            return
        }

        var request = URLRequest(url: bridgeURL)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Bridge error: \(error.localizedDescription)")
                return
            }

            guard let data = data,
                  let responseString = String(data: data, encoding: .utf8) else {
                print("Bridge returned no readable response")
                return
            }

            print("Bridge response: \(responseString)")
        }.resume()
    }
}
