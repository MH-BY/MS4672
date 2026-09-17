from opentrons import protocol_api

metadata = {
    'protocolName': 'Rainbow Color Mixing',
    'author': 'Student Name',
    'description': 'Two-row rainbow gradient, one tip per source color',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):

    # 1. Labware
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    reservoir = protocol.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')

    # 2. Pipette
    pipette = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=[tiprack])

    # >>> Set this to the first unused tip before each run <
    # Each run consumes 4 tips (one per color), going down the column:
    #   A1 -> uses A1, B1, C1, D1
    #   E1 -> uses E1, F1, G1, H1
    #   A2 -> uses A2, B2, C2, D2   ... etc.
    pipette.starting_tip = tiprack['A2']

    # 3. Rainbow definition
    # Source tubes in rainbow order: red -> yellow -> green -> blue
    colors = ['A3', 'B3', 'A4', 'B4']

    # Volume of each color in each of the 12 wells (µL), total = 250 µL/well.
    # Columns: red, yellow, green, blue
    gradient = [
        [250,   0,   0,   0],   # col 1  pure red
        [180,  70,   0,   0],   # col 2
        [115, 135,   0,   0],   # col 3
        [ 45, 205,   0,   0],   # col 4
        [  0, 230,  20,   0],   # col 5  ~pure yellow
        [  0, 160,  90,   0],   # col 6
        [  0,  90, 160,   0],   # col 7
        [  0,  20, 230,   0],   # col 8  ~pure green
        [  0,   0, 205,  45],   # col 9
        [  0,   0, 135, 115],   # col 10
        [  0,   0,  70, 180],   # col 11
        [  0,   0,   0, 250],   # col 12 pure blue
    ]

    # Row A: left -> right, Row B: mirrored (right -> left)
    row_A = plate.rows_by_name()['B']              # B1 ... B12
    row_B = plate.rows_by_name()['C'][::-1]        # C12 ... C1

    # 4. Liquid handling: one fresh tip per color
    for color_idx, source in enumerate(colors):
        pipette.pick_up_tip()      # next tip from starting_tip onward

        for well_A, well_B, vols in zip(row_A, row_B, gradient):
            vol = vols[color_idx]
            if vol == 0:
                continue
            pipette.aspirate(vol, reservoir[source])
            pipette.dispense(vol, well_A)
            pipette.aspirate(vol, reservoir[source])
            pipette.dispense(vol, well_B)

        pipette.drop_tip()