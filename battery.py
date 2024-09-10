import os
import xml.dom.minidom as ES


#reconstructed to not use batch file.
create_report = 'powercfg /batteryreport /xml'
os.system(create_report)

#Opening up the battery report and getting all my elements
doc = ES.parse('battery-report.xml')
batteryCap = doc.getElementsByTagName('DesignCapacity')
actualCap = doc.getElementsByTagName('FullChargeCapacity')

#pulling data and assigning to variables
aCap = int(batteryCap[0].firstChild.data)
bCap = int(actualCap[0].firstChild.data)
bHealth = int((bCap/aCap)*100)

#print block with information
print(f"Design Capacity: {aCap} mWh")
print(f"Actual Capacity: {bCap} mWh")
print(f"{bHealth}%") 

#cleaning up and closing files
os.remove("battery-report.xml")



