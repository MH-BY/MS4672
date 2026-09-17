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
    
    # 1. Load labware 
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')
    
    # 2. Load pipette 
    pipette = protocol.load_instrument(
        'p300_single_gen2', 
        'left', 
        tip_racks=[tiprack]
    )
    
    
    # Pick up a tip

    pipette.pick_up_tip(tiprack['B1'])
    
    #red
    for well in ['D1', 'E11']:
        pipette.aspirate(180, reservoir['A3'])
        pipette.dispense(180, plate[well])
    for well in ['D2', 'E10']:
        pipette.aspirate(120, reservoir['A3'])
        pipette.dispense(120, plate[well])
    for well in ['D3', 'E9']:
        pipette.aspirate(60, reservoir['A3'])
        pipette.dispense(60, plate[well])

    #yellow
    for well in ['D4', 'E8']:
        pipette.aspirate(240, reservoir['B3'])
        pipette.dispense(240, plate[well])
    for well in ['E7', 'D5', 'E9', 'D3']:
        pipette.aspirate(180, reservoir['B3'])
        pipette.dispense(180, plate[well])
    for well in ['D2', 'E10', 'D6', 'E6']:
        pipette.aspirate(120, reservoir['B3'])
        pipette.dispense(120, plate[well])
    for well in ['D7', 'E5', 'D1', 'E11']:
        pipette.aspirate(60, reservoir['B3'])
        pipette.dispense(60, plate[well])

    #green
    for well in ['D8', 'E4']:
        pipette.aspirate(240, reservoir['A4'])
        pipette.dispense(240, plate[well])
    for well in ['E5', 'D7', 'E3', 'D9']:
        pipette.aspirate(180, reservoir['A4'])
        pipette.dispense(180, plate[well])
    for well in ['E6', 'D6', 'E2', 'D10']:
        pipette.aspirate(120, reservoir['A4'])
        pipette.dispense(120, plate[well])
    for well in ['E7', 'D5', 'E1', 'D11']:
        pipette.aspirate(60, reservoir['A4'])
        pipette.dispense(60, plate[well])
        
    #blue 
    for well in ['E1', 'D11']:
        pipette.aspirate(180, reservoir['B4'])
        pipette.dispense(180, plate[well])
    for well in ['E2', 'D10']:
        pipette.aspirate(120, reservoir['B4'])
        pipette.dispense(120, plate[well])
    for well in ['E3', 'D9']:
        pipette.aspirate(60, reservoir['B4'])
        pipette.dispense(60, plate[well])

    # Drop the tip when finished
    #NOTE -  I didn't change tips between colour switches 
    pipette.drop_tip()