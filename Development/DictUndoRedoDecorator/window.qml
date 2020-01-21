import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import QtQuick.Window 2.0

Window {
    property var hello: ["Hello World", "Hallo Welt", "Hei maailma", "Hola Mundo"]

    visible: true
    width: 200
    height: 200

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Label { id: label; text: "Initial label text3" }

        Button {
            text: "Click me"
            onClicked: label.text = helloMessage.randomHello()
        }
    }
}
