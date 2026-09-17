from opentrons import protocol_api

metadata = {
    'protocolName': 'Rainbow Color Mixing smart',
    'author': 'Student Name',
    'description': 'Two-row rainbow gradient, one tip per source color',
    'apiLevel': '2.13'
}


def run(protocol: protocol_api.ProtocolContext):

    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    reservoir = protocol.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')

    pipette = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=[tiprack])
    pipette.starting_tip = tiprack['A3']     # first unused tip on the rack

    colors = ['A3', 'B3', 'A4', 'B4']        # red -> yellow -> green -> blue
    TOTAL_VOL = 250

    row_A = plate.rows_by_name()['B']
    row_B = plate.rows_by_name()['C'][::-1]  # mirrored
    n = len(row_A)

    for c, source in enumerate(colors):
        pipette.pick_up_tip()
        for i, (well_A, well_B) in enumerate(zip(row_A, row_B)):
            t = i * (len(colors) - 1) / (n - 1)
            vol = TOTAL_VOL * max(0, 1 - abs(t - c))
            if vol:
                pipette.transfer(vol, reservoir[source], [well_A, well_B], new_tip='never')
        pipette.drop_tip()





