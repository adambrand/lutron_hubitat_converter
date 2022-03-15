"""Convert Lutron Caseta Smart Bridge Pro export file to Hubitat import file.
See full integration steps here: https://docs.hubitat.com/index.php?title=Lutron_Integrator"""
import argparse
import os
import sys
import getopt
import csv
import json


# Handle command line arguments.
def process_commandline_options(python_file_name, command_line_args):
    command_line_parser = argparse.ArgumentParser(
        description="Convert Lutron Caseta Smart Bridge Pro export file to Hubitat format.")
    command_line_parser.add_argument('lutron_in', metavar='<lutron_json_export.json>', type=str, nargs='+',
                                     help='a file containing the exported Lutron data')
    command_line_parser.add_argument('hubitat_out', metavar='<new_hubitat_file.csv>', type=str, nargs='+',
                                     help='the name of the file you want to export Hubitat data to')
    parsed_args = command_line_parser.parse_args()

    return parsed_args.lutron_in[0], parsed_args.hubitat_out[0]


# Convert the Lutron JSON-like format into the Hubitat CSV format.
def convert_lutron_to_hubitat(python_file_name, command_line_args):
    # Parse command line arguments to get input and output files.
    lutron_input_filename, hubitat_output_filename = process_commandline_options(python_file_name, command_line_args)

    # Get a file handle, read the file into a string, then load it into a JSON object.
    lutron_input_file = open(lutron_input_filename)
    lutron_export_string = lutron_input_file.read()
    lutron_export_json_full = json.loads(lutron_export_string)

    # Convert Devices (picos etc)
    lutron_export_json_devices = lutron_export_json_full['LIPIdList']['Devices']
    hubitat_devices = []

    for lutron_device in lutron_export_json_devices:
        # Skip the first ID as it has only virtual devices.
        if lutron_device['ID'] != 1:
            device_entry = {
                'code': 'p',
                'id': lutron_device['ID'],
                'name': lutron_device['Area']['Name'] + ' ' + lutron_device['Name']
            }
            hubitat_devices.append(device_entry)

    # Convert Zones (Switches/Dimmers)
    lutron_export_json_zones = lutron_export_json_full['LIPIdList']['Zones']
    hubitat_zones = []

    for lutron_zone in lutron_export_json_zones:
        # If a zone has Dimmer in the name, we assume it is a dimmer.
        code = 'd' if 'Dimmer' in lutron_zone['Name'] else 's'
        zone_entry = {
            'code': code,
            'id': lutron_zone['ID'],
            'name': lutron_zone['Area']['Name'] + ' ' + lutron_zone['Name']
        }
        hubitat_zones.append(zone_entry)

    # Write out the CSV file.
    fieldnames = ['code', 'id', 'name']

    with open(hubitat_output_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(hubitat_devices)
        writer.writerows(hubitat_zones)


# Entrypoint
if __name__ == '__main__':
    convert_lutron_to_hubitat(sys.argv[0], sys.argv[1:])
