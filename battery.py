import os
import xml.dom.minidom as ES
import customtkinter
from CTkMessagebox import CTkMessagebox
import subprocess

#Window Settings
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

#Send this into subprocess.run under creationflags= to hide cmd window
DETACHED_PROCESS = 0x00000008

#Setting up Main Window
root = customtkinter.CTk()
root.title("Battery Health")
root.geometry('750x450')



#health bar, passing in bhealth get the bar with alt+219
def health_bar(health):
    bar = '█' * int(int(health)/10) + '---' * int((100- int(health))/10)
    print(f"|{bar}| {health}% Usable Battery")
    return(f"|{bar}| {health}% Usable Battery")

#Creates report and displays file location
def generateReport():
    create_report = 'powercfg /batteryreport'
    # os.system(create_report)
    subprocess.run(create_report, creationflags=DETACHED_PROCESS)
    cwd = os.getcwd()
    CTkMessagebox(title='Report', message=f"Saved to file path: \n \n {cwd}.")


def main():
    #reconstructed to not use batch file.
    create_report = 'powercfg /batteryreport /xml'
    subprocess.run(create_report, creationflags=DETACHED_PROCESS)
    # os.system(create_report)

    #Opening up the battery report and getting all my elements
    doc = ES.parse('battery-report.xml')
    batteryCap = doc.getElementsByTagName('DesignCapacity')
    actualCap = doc.getElementsByTagName('FullChargeCapacity')

    #pulling data and assigning to variables
    aCap = int(batteryCap[0].firstChild.data)
    bCap = int(actualCap[0].firstChild.data)
    bHealth = int((bCap/aCap)*100)

    #print block with information
    # print(f"Design Capacity: {aCap} mWh")
    # print(f"Actual Capacity: {bCap} mWh")
    # health_bar(bHealth)
    
    #cleaning up and closing files
    os.remove("battery-report.xml")

    #Setting up each piece of the new window
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill='both', expand=True)
    
    #Top Label
    label = customtkinter.CTkLabel(master=frame, text="Battery Health", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    #Health Bar set using bhealth, range is 0-1
    displayBar = customtkinter.CTkProgressBar(master=frame, orientation="horizontal", width=300, height=50,corner_radius=20, border_width=2, border_color="white", fg_color="red", progress_color='green', mode='determinate', determinate_speed=5, indeterminate_speed=.5)
    displayBar.pack(pady=20)
    displayBar.set(bHealth/100)

    #Separate frame to display bottom half
    lowFrame = customtkinter.CTkFrame(master=frame)
    lowFrame.pack(pady=20, padx=5)

    #labels for written information
    label = customtkinter.CTkLabel(master=lowFrame, text=f"Design Capacity: {aCap} mWh            Actual Capacity: {bCap} mWh", font=("Roboto", 12))
    label.pack(pady=12, padx=10)

    label = customtkinter.CTkLabel(master=lowFrame, text=f"Usable Battery: {bHealth}%", font=("Roboto", 12))
    label.pack(pady=12, padx=10)

    #Calls the Generate Report Function at the top
    button = customtkinter.CTkButton(master=frame, width=120, height=32, border_width=0,corner_radius=8, text="Generate Full Report", command=generateReport)
    button.pack(pady=10, padx=20)
    

    root.mainloop()

if __name__ == "__main__":
    main()