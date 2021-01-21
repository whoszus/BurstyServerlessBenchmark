func main(args: [String:Any]) -> [String:Any] {
    extension Date {
        var timeStamp : String {
            let timeInterval: TimeInterval = self.timeIntervalSince1970
            let timeStamp = Int(timeInterval)
            return "\(timeStamp)"
        }

        var milliStamp : String {
            let timeInterval: TimeInterval = self.timeIntervalSince1970
            let millisecond = CLongLong(round(timeInterval*1000))
            return "\(millisecond)"
        }
    }

    let startTime = Date().milliStamp
    if let name = args["name"] as? String {
        return [ "token" : "Hello \(name)!" , "startTime" : startTime]
    } else {
        return [ "token" : "Hello stranger!" , "startTime" : startTime]
    }
}

//不太会写，运行时说没运行完，待修改