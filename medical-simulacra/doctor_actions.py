import math

def move_doctor_to_player(player_pos, doctor_name, description, doctors, dialogue_manager):
    """
    Moves a specified doctor close to the player's position and initiates a conversation.
    """
    doctor = next((d for d in doctors if d.name == doctor_name), None)
    if not doctor:
        print(f"Doctor {doctor_name} not found.")
        return False

    dx = player_pos[0] - doctor.pos[0]
    dy = player_pos[1] - doctor.pos[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance <= 2:
        print(f"Doctor {doctor_name} is already close to the player.")
    else:
        # Normalize the direction vector
        dx /= distance
        dy /= distance

        # Move the doctor to a position 2 units away from the player
        new_x = player_pos[0] - int(3 * dx)
        new_y = player_pos[1] - int(3 * dy)

        # Update the doctor's position
        doctor.pos = [new_x, new_y]
        print(f"Doctor {doctor_name} moved to position ({new_x}, {new_y})")

    # Start the conversation
    #dialogue_manager.start_conversation_with(doctor)
    #initial_message = f"Hello, I'm Dr. {doctor_name}. {description}"
    #dialogue_manager.start_dialogue("NPC", initial_message)

    print(f"Started conversation with Dr. {doctor_name}: {description}")
    return True