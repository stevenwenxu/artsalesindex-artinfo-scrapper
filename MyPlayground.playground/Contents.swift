import Foundation

let fileURL = Bundle.main.url(forResource: "ceramics_metalware_sculpture_combined", withExtension: "csv")!
let entries = try! String(contentsOf: fileURL, encoding: String.Encoding.utf8).components(separatedBy: "\n")

let people = entries.map {
    $0.components(separatedBy: ",").first!
}

var dict = [String:Int]()
for p in people {
    dict[p, default: 0] += 1
}
let newDict = dict.filter { (key, value) in
    return value >= 5
}
print(newDict.count)
print(Array(newDict.keys).joined(separator: ","))
print(newDict.map {$0.value}.reduce(0, +))

let filteredEntries = entries.filter {
    let name = $0.components(separatedBy: ",").first!
    return newDict.keys.contains(name)
}
filteredEntries.count
filteredEntries[0]

let documentDirectory = try! FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
let newFile = documentDirectory.appendingPathComponent("new.csv")

try! filteredEntries.joined(separator: "\n").write(to: newFile, atomically: false, encoding: .utf8)

