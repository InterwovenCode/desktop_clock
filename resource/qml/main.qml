import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

// ApplicationWindow {
Rectangle {
    id: root
    visible: true
    width: 200
    height: 200
    // x: screen.desktopAvailableWidth - width - 12
    // y: screen.desktopAvailableHeight - height - 48
    // title: "Clock"
    // flags: Qt.FramelessWindowHint | Qt.Window
    property var hms: {'hours': 0, 'minutes': 0, 'seconds': 0 }
    property QtObject backend

    color: "transparent"

    Image {
        id: clockface
        sourceSize.width: parent.width
        fillMode: Image.PreserveAspectFit
        source: "qrc:/desktop_clock/images/clockface.png"

        Image {
            x: clockface.width/2 - width/2
            y: (clockface.height/2) - height/2
            scale: clockface.width/465
            source: "qrc:/desktop_clock/images/hour.png"
            transform: Rotation {
                    origin.x: 12.5; origin.y: 166;
                    angle: (hms.hours * 30) + (hms.minutes * 0.5)
            }
        }

        Image {
            x: clockface.width/2 - width/2
            y: clockface.height/2 - height/2
            source: "qrc:/desktop_clock/images/minute.png"
            scale: clockface.width/465
            transform: Rotation {
                    origin.x: 5.5; origin.y: 201;
                    angle: hms.minutes * 6
                    Behavior on angle {
                        SpringAnimation { spring: 1; damping: 0.2; modulus: 360 }
                    }
                }
        }

        Image {
            x: clockface.width/2 - width/2
            y: clockface.height/2 - height/2
            source: "qrc:/desktop_clock/images/second.png"
            scale: clockface.width/465
            transform: Rotation {
                    origin.x: 2; origin.y: 202;
                    angle: hms.seconds * 6
                    Behavior on angle {
                        SpringAnimation { spring: 3; damping: 0.2; modulus: 360 }
                    }
                }
        }

        Image {
            x: clockface.width/2 - width/2
            y: clockface.height/2 - height/2
            source: "qrc:/desktop_clock/images/cap.png"
            scale: clockface.width/465
        }
    }

    Connections {
        target: backend

        function onHms(hours, minutes, seconds) {
            hms = {'hours': hours, 'minutes': minutes, 'seconds': seconds }
        }
    }

    MouseArea {
        anchors.fill: parent
        property var mousePos: Qt.point(0, 0)
        property var windowPos: Qt.point(0, 0)
        
        onPressed: {
            mousePos = Qt.point(mouse.x, mouse.y)
        }
        
        onPositionChanged: {
            windowPos = Qt.point(root.x, root.y)
            root.x = windowPos.x + (mouse.x - mousePos.x)
            root.y = windowPos.y + (mouse.y - mousePos.y)
        }
    }
}