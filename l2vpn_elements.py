from manim import (
    Scene,
    Text,
    Square,
    Circle,
    Rectangle,
    VGroup,
    Create,
    FadeIn,
    FadeOut,
    ManimColor,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

# Color Definitions
CUSTOMER_COLOR = ManimColor("#007bff")  # A nice blue, similar to BLUE_C
PROVIDER_COLOR = ManimColor("#28a745")  # A standard green, similar to GREEN_C
PACKET_COLOR = ManimColor("#ffc107")  # A vibrant yellow, similar to YELLOW_A
LABEL_COLOR = ManimColor("#fd7e14")  # A distinct orange, similar to ORANGE_C

# Network Element Styles
def create_router(label_text: str, color: ManimColor) -> VGroup:
    """
    Creates a router representation.

    Args:
        label_text: The text label for the router.
        color: The color of the router.

    Returns:
        A VGroup representing the router.
    """
    router_shape = Square(side_length=1.0, color=color, fill_color=color, fill_opacity=0.2)
    router_label = Text(label_text, color=ManimColor("#FFFFFF"), font_size=24).move_to(router_shape.get_center())
    return VGroup(router_shape, router_label)

# Packet Representation
def create_packet_representation(initial_text: str = "Packet") -> VGroup:
    """
    Creates a basic packet representation.

    Args:
        initial_text: The initial text to display on the packet.

    Returns:
        A VGroup representing the packet.
    """
    packet_shape = Rectangle(width=2.0, height=0.5, color=PACKET_COLOR, fill_color=PACKET_COLOR, fill_opacity=0.3)
    packet_label = Text(initial_text, color=ManimColor("#000000"), font_size=20).move_to(packet_shape.get_center())
    return VGroup(packet_shape, packet_label)

# Example Usage (can be removed or commented out later)
class TestScene(Scene):
    def construct(self):
        # Test router creation
        customer_router = create_router("CE1", CUSTOMER_COLOR).shift(LEFT * 3)
        provider_router = create_router("PE1", PROVIDER_COLOR)
        
        # Test packet creation
        packet = create_packet_representation("Data").shift(UP * 2)

        self.play(Create(customer_router))
        self.play(Create(provider_router))
        self.play(FadeIn(packet))
        self.wait(2)
        self.play(FadeOut(customer_router), FadeOut(provider_router), FadeOut(packet))
        self.wait(1)

if __name__ == "__main__":
    # This part is for local testing if you run the script directly.
    # It won't be used when importing these elements into another Manim scene.
    pass
    # To render this test scene, you would typically run from the command line:
    # manim -pql l2vpn_elements.py TestScene
    # However, this execution within the tool environment might be different.
    # For now, the definitions are the key part.
