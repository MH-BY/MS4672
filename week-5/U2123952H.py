from opentrons import protocol_api

# Protocol metadata - required for all protocols
metadata = {
    'protocolName': 'Basic Liquid Handling',
    'author': 'Student Name',
    'description': 'Simple protocol for learning OT-2 operation',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    """
    This function defines what the robot will do.
    It's called automatically when the protocol runs.
    """
    
    # 1. Load labware (define what equipment is on the deck)
    # Slot numbers 1-11 refer to positions on the robot deck
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')
    
    # 2. Load pipette (define which pipette to use)
    # 'right' or 'left' refers to the pipette mount position
    pipette = protocol.load_instrument(
        'p300_single_gen2', 
        'left', 
        tip_racks=[tiprack]
    )
    
    # 3. Protocol steps (define the liquid handling operations)
    #Red
    #Pick up a top
    pipette.pick_up_tip(tiprack['A2'])

    #Aspirate 
    dispense_map_red = {'B1': 4, 'B2': 3, 'B3': 1, 'C12': 4, 'C11': 3, 'C10': 1}
    
    for well, count in dispense_map_red.items():
        for _ in range(count):
            pipette.aspirate(50, reservoir['A3'])
            pipette.dispense(50, plate[well])

    #Drop
    pipette.drop_tip()

    #Yellow
    #Pick up
    pipette.pick_up_tip(tiprack['A3'])

    #Aspirate
    dispense_map_yellow = {'B2': 1, 'B3': 3, 'B4': 4, 'B5': 3, 'B6': 2, 'B7': 1, 'C11': 1, 'C10': 3, 'C9': 4, 'C8': 3, 'C7': 2, 'C6': 1}
    
    for well, count in dispense_map_yellow.items():
        for _ in range(count):
            pipette.aspirate(50, reservoir['B3'])
            pipette.dispense(50, plate[well])

    #Drop
    pipette.drop_tip()

    #Green
    #Pick up
    pipette.pick_up_tip(tiprack['A4'])

    #Aspirate
    dispense_map_green = {'B5': 1, 'B6': 2, 'B7': 3, 'B8': 4, 'B9': 3, 'B10': 2, 'B11': 1, 'C8': 1, 'C7': 2, 'C6': 3, 'C5': 4, 'C4': 3, 'C3': 2, 'C2': 1,}
    
    for well, count in dispense_map_green.items():
        for _ in range(count):
            pipette.aspirate(50, reservoir['A4'])
            pipette.dispense(50, plate[well])

    #Drop
    pipette.drop_tip()

    #Blue
    #Pick up
    pipette.pick_up_tip(tiprack['A5'])

    #Aspirate
    dispense_map_blue = {'B9': 1, 'B10': 2, 'B11': 3, 'B12': 4, 'C4': 1, 'C3': 2, 'C2': 3, 'C1': 4}
    
    for well, count in dispense_map_blue.items():
        for _ in range(count):
            pipette.aspirate(50, reservoir['B4'])
            pipette.dispense(50, plate[well])

    #Drop
    pipette.drop_tip()