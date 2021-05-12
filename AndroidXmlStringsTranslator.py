import json
import xml.etree.ElementTree as ET
from google_trans_new import google_translator

class Main:

    codeList = ["ar", "bg", "de", "el", "es", "fa", "fr", "hi", "hr", "it", "iw", "nl", "pl", "pt", "ru", "tr"]

    def readOriginal(self):
        originalList = []
        f = open("strings.xml", "r", encoding="utf-8")
        data = f.read()
        dataList = ET.fromstring(data.replace(",", "").replace("'", ''))
        for x in dataList:
            if x.tag == "string":
                datas = str(x.attrib).replace("}", ", '_data_' : '" + x.text + "'}")
                datas = (datas.replace("'", '"'))
                originalList.append(datas)
        return originalList

    def convertTexts(self, originalList):
        jsonList = json.loads(originalList.__str__().replace("'", ""))
        allText = "\n"
        for code in self.codeList:
            for son in jsonList:
                translatable = True
                if "translatable" in son:
                    if son["translatable"] == "false":
                        translatable = False

                translatedText = self.translate(text=son["_data_"], code=code)
                if not translatable:
                    translatedText = son["_data_"]
                row = self.createRow(name=son["name"], value=translatedText)
                allText += "\t" + row + "\n"


            print("All :", allText)
            f = open("strings_" + code + ".xml", "w", encoding="utf-8")
            f.write("<resources>\n" + allText + "\n</resources>")
            f.close()
            allText = "\n"


    def createRow(self, name, value):
        textFormat = '<string name="_name_here_">_value_here_</string>'
        try:
            turnedText = textFormat.replace("_name_here_", name).replace("_value_here_", value.strip().capitalize())
        except:
            return textFormat.replace("_name_here_", name).replace("_value_here_", value[0])
        return turnedText

    def translate(self, text, code):
        translator = google_translator()
        translate_text = translator.translate(text=text, lang_tgt=code)
        return translate_text

    def initialize(self):
        originalList = self.readOriginal()
        self.convertTexts(originalList=originalList)


if __name__ == '__main__':
    Main().initialize()
