import xml.dom.minidom as mini

doc = mini.parse('example.xml')
print(doc.nodeName)
print(doc.firstChild.tagName)
words = doc.getElementsByTagName("word")
for n in words:
    print(n)
