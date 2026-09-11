from opentrons import protocol_api


metadata = {
    'protocolName': 'Rainbow Color Mixing',
    'author': 'Siddharth Choudhary (U2223021B)',
    'description': 'Rainbow colour gradient in two rows of a 96-well plate',
    'apiLevel': '2.13'
}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    reservoir = protocol.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')

    pipette = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=[tiprack])
    pipette.starting_tip = tiprack['A1']

    # Source tubes: red, yellow, green, blue.
    colors = ['A3', 'B3', 'A4', 'B4']
    TOTAL_VOLUME = 250

    # Each list is [red, yellow, green, blue] in microlitres.
    gradient = [
        [250, 0, 0, 0],
        [180, 70, 0, 0],
        [115, 135, 0, 0],
        [45, 205, 0, 0],
        [0, 230, 20, 0],
        [0, 160, 90, 0],
        [0, 90, 160, 0],
        [0, 20, 230, 0],
        [0, 0, 205, 45],
        [0, 0, 135, 115],
        [0, 0, 70, 180],
        [0, 0, 0, 250],
    ]

    # The second row is filled in the opposite direction.
    row_one = plate.rows_by_name()['B']
    row_two = plate.rows_by_name()['C'][::-1]

    # Use one tip for each colour to avoid mixing colours in the sources.
    for color_index, source in enumerate(colors):
        pipette.pick_up_tip()

        for first_well, second_well, volumes in zip(row_one, row_two, gradient):
            volume = volumes[color_index]
            if volume == 0:
                continue

            pipette.aspirate(volume, reservoir[source])
            pipette.dispense(volume, first_well)
            pipette.aspirate(volume, reservoir[source])
            pipette.dispense(volume, second_well)

        pipette.drop_tip()
