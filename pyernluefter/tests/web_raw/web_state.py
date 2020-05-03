import datetime

RAW = {
    "Date": "03.05.2020",
    "Time": "20:56:38",
    "DeviceName": "ECFABC01111",
    "MAC": "A020A6199C99",
    "LocalIP": "192.168.178.137",
    "RSSI": "-60",
    "FW_MainController": "1838000A",
    "FW_WiFi": "WS181130",
    "SystemMode": "Kellermode",
    "Speed_In": "01",
}

PROCESSED = {
    "Date": datetime.date(2020, 5, 3),
    "Time": datetime.time(20, 56, 38),
    "DeviceName": "ECFABC01111",
    "MAC": "A020A6199C99",
    "LocalIP": "192.168.178.137",
    "RSSI": -60,
    "FW_MainController": "1838000A",
    "FW_WiFi": "WS181130",

}
