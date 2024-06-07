# lutron_hubitat_converter
Convert a Lutron Caseta Bridge Pro automation export file to a file compatible with the Hubitat Lutron integration.

At the moment, it only supports Picos, Dimmers, and Switches.

Note: For the converter to differentiate between a dimmer and a switch, it looks for the title "Dimmer" in the device name. So you may have to rename your existing devices if you like this option. If you already have a naming convention that allows for this differentiation, you can also just modify the script to make a decision based on that.

How to Use
1. Ensure you have Python 3 installed.
2. Download the .py file.
3. Follow the instructions here: https://docs.hubitat.com/index.php?title=Lutron_Integrator to the point where it describes creating an integration report.
4. Put the output of the integration report from #3 into a file (e.g., lutron_export.json).
5. Run the converter against the .json file from #4, specifying an output file. For example, "python3 lutron_hubitat_converter.py lutron_export.json hubitat_import.csv" ... lutron_export.json would be the file name you chose in step 4, and hubitat_import.csv is just where you want the output to go for use in step 6.
6. Copy and paste the contents from the output file into Hubitat as shown in the Hubitat instructions (linked above) in the "Use Configuration List" portion.
7. It should work!

All product names, logos, brands, trademarks and registered trademarks are property of their respective owners. All company, product and service names used in this website are for identification purposes only. Use of these names, trademarks and brands does not imply endorsement.
