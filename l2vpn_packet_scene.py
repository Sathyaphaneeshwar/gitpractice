from manim import (
    Scene,
    Text,
    VGroup,
    Rectangle,
    Line,
    Brace,
    Create,
    Write,
    FadeIn,
    AddTextLetterByLetter,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    GREY_BROWN,
    config,
    Group,
    Tex
)

# Assuming l2vpn_elements.py is in the same directory or accessible in PYTHONPATH
from l2vpn_elements import (
    CUSTOMER_COLOR,
    PROVIDER_COLOR,
    PACKET_COLOR, # General packet color, can be base for customer frame
    LABEL_COLOR,  # For MPLS labels
)

# Configure default font size for slides if needed
config.font_size = 28 # Adjusted for potentially more text on screen

class L2VPNPacketStructureScene(Scene):
    """
    Scene to detail the L2 VPN packet structure layer by layer.
    """
    def construct(self):
        # Title
        title = Text("L2 VPN Packet Structure", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Initial y_position for packet components
        packet_y_pos = 0

        # --- 1. Customer Ethernet Frame ---
        # Define segments and their labels
        frame_segments_data = [
            ("Dest MAC", 1.5), ("Src MAC", 1.5), ("VLAN (opt)", 1.0),
            ("EtherType", 1.0), ("Payload", 2.5)
        ]
        
        customer_frame_parts = VGroup()
        current_x = 0
        for label_text, width in frame_segments_data:
            part = Rectangle(width=width, height=0.8, color=CUSTOMER_COLOR, fill_color=CUSTOMER_COLOR, fill_opacity=0.3)
            part_label = Text(label_text, font_size=16).move_to(part.get_center())
            part_group = VGroup(part, part_label).shift(current_x * RIGHT)
            customer_frame_parts.add(part_group)
            current_x += width

        customer_frame_parts.move_to(ORIGIN + DOWN * 0.5).center().shift(DOWN * 0.5) # Center the whole frame
        
        self.play(Create(customer_frame_parts), run_time=2)
        self.wait(0.5)
        
        # Brace for Customer Ethernet Frame
        brace_customer_frame = Brace(customer_frame_parts, direction=DOWN, buff=0.2)
        label_customer_frame = brace_customer_frame.get_text("Customer Ethernet Frame", font_size=24)
        self.play(Create(brace_customer_frame), Write(label_customer_frame))
        self.wait(1)

        # Group all current elements to move them up later if needed
        current_packet_visual = VGroup(customer_frame_parts)
        current_braces_labels = VGroup(brace_customer_frame, label_customer_frame)

        # --- 2. Control Word (Optional) ---
        cw_width = 0.8
        control_word_rect = Rectangle(width=cw_width, height=0.8, color=GREY_BROWN, fill_color=GREY_BROWN, fill_opacity=0.5)
        control_word_label = Text("CW", font_size=18).move_to(control_word_rect.get_center())
        control_word = VGroup(control_word_rect, control_word_label)
        
        # Position to the left of the customer frame
        control_word.next_to(customer_frame_parts, LEFT, buff=0)
        
        cw_annotation_text = Text("Control Word (Optional: sequencing, OAM)", font_size=20)
        cw_annotation_text.next_to(control_word, UP, buff=0.3)

        self.play(
            FadeIn(control_word, shift=RIGHT*0.5),
            Write(cw_annotation_text)
        )
        self.wait(0.5)
        
        # Update current packet visual
        current_packet_visual.add_to_back(control_word) # Add to back to maintain order for next_to
        current_packet_visual.arrange(RIGHT, buff=0) # Re-arrange to ensure no gaps

        # --- 3. VC Label (Inner Label) ---
        vc_label_width = 1.0
        vc_label_rect = Rectangle(width=vc_label_width, height=0.8, color=LABEL_COLOR, fill_color=LABEL_COLOR, fill_opacity=0.6)
        vc_label_text = Text("VC Label", font_size=18).move_to(vc_label_rect.get_center())
        vc_label = VGroup(vc_label_rect, vc_label_text)

        vc_label.next_to(current_packet_visual, LEFT, buff=0) # Current packet visual now includes CW
        
        vc_annotation_text = Text("VC Label (Identifies L2 VPN service)", font_size=20)
        vc_annotation_text.next_to(vc_label, UP, buff=0.3)

        self.play(
            FadeIn(vc_label, shift=RIGHT*0.5),
            Write(vc_annotation_text)
        )
        self.wait(0.5)
        current_packet_visual.add_to_back(vc_label)
        current_packet_visual.arrange(RIGHT, buff=0)

        # --- 4. Transport Label (Outer Label) ---
        t_label_width = 1.0
        # Using a slightly different shade/look for T-Label if possible, or just text
        transport_label_rect = Rectangle(width=t_label_width, height=0.8, color=LABEL_COLOR, fill_color=LABEL_COLOR, fill_opacity=0.8) # Darker opacity
        transport_label_text = Text("T-Label", font_size=18).move_to(transport_label_rect.get_center())
        transport_label = VGroup(transport_label_rect, transport_label_text)

        transport_label.next_to(current_packet_visual, LEFT, buff=0)

        t_annotation_text = Text("Transport Label (Provider core transit)", font_size=20)
        t_annotation_text.next_to(transport_label, UP, buff=0.3)
        
        self.play(
            FadeIn(transport_label, shift=RIGHT*0.5),
            Write(t_annotation_text)
        )
        self.wait(0.5)
        current_packet_visual.add_to_back(transport_label)
        current_packet_visual.arrange(RIGHT, buff=0)

        # Group MPLS Labels for a brace
        mpls_labels_group = VGroup(vc_label, transport_label) # Order might be visual, not strict addition order
        # Recreate mpls_labels_group based on current_packet_visual for correct order
        mpls_labels_group_for_brace = VGroup(current_packet_visual[0], current_packet_visual[1]) # Assuming T-Label then VC-Label if added to front

        # Adjusting for current_packet_visual structure:
        # current_packet_visual contains: T-Label, VC-Label, CW, CustFrameParts
        # So, mpls_labels_group_for_brace should be transport_label and vc_label
        
        # Let's get them by reference
        actual_t_label_in_packet = transport_label
        actual_vc_label_in_packet = vc_label
        
        brace_mpls_labels = Brace(VGroup(actual_t_label_in_packet, actual_vc_label_in_packet), direction=UP, buff=0.1)
        # Need to ensure the VGroup for brace has the correct elements in order.
        # Since they are added to the front and then arranged, they should be the first elements.
        
        # Let's re-center the packet and move annotations
        self.play(
            current_packet_visual.animate.center().shift(DOWN*0.5),
            # Move annotations along with their respective labels
            cw_annotation_text.animate.next_to(control_word, UP, buff=0.3),
            vc_annotation_text.animate.next_to(vc_label, UP, buff=0.3),
            t_annotation_text.animate.next_to(transport_label, UP, buff=0.3),
            current_braces_labels.animate.next_to(customer_frame_parts, DOWN, buff=0.2)
        )
        self.wait(0.5)
        
        # Now create brace for MPLS labels based on new positions
        # Ensure the group for the brace is correctly formed from the items in current_packet_visual
        mpls_brace_group = VGroup(current_packet_visual.submobjects[0], current_packet_visual.submobjects[1])
        brace_mpls = Brace(mpls_brace_group, direction=UP, buff=0.2)
        label_mpls = brace_mpls.get_text("MPLS Labels", font_size=24)
        self.play(Create(brace_mpls), Write(label_mpls))
        self.wait(1)
        current_braces_labels.add(brace_mpls, label_mpls)


        # --- 5. Provider Network Header ---
        # Calculate width to encapsulate everything so far
        provider_hdr_width = 1.5
        provider_header_rect = Rectangle(
            width=provider_hdr_width, height=0.8, 
            color=PROVIDER_COLOR, fill_color=PROVIDER_COLOR, fill_opacity=0.4
        )
        provider_header_text = Text("Provider L3/L2 Hdr", font_size=16).move_to(provider_header_rect.get_center())
        provider_header = VGroup(provider_header_rect, provider_header_text)
        
        provider_header.next_to(current_packet_visual, LEFT, buff=0)

        prov_annotation_text = Text("Provider Network Header (e.g., MPLS, IP)", font_size=20)
        prov_annotation_text.next_to(provider_header, UP, buff=0.3)

        self.play(
            FadeIn(provider_header, shift=RIGHT*0.5),
            Write(prov_annotation_text)
        )
        self.wait(0.5)
        current_packet_visual.add_to_back(provider_header)
        current_packet_visual.arrange(RIGHT, buff=0)

        # Final re-centering and brace for provider header
        self.play(
            current_packet_visual.animate.center().shift(DOWN*0.5),
            # Move all annotations
            cw_annotation_text.animate.next_to(control_word, UP, buff=0.3),
            vc_annotation_text.animate.next_to(vc_label, UP, buff=0.3),
            t_annotation_text.animate.next_to(transport_label, UP, buff=0.3),
            prov_annotation_text.animate.next_to(provider_header, UP, buff=0.3),
            current_braces_labels.animate.next_to(current_packet_visual, DOWN, buff=0.2) # This might need adjustment
        )
        
        # Adjust brace for customer frame as it's part of current_packet_visual
        # customer_frame_parts is still the correct VGroup for this brace.
        # The brace_mpls also needs to follow its group.
        
        # Re-position all braces based on the final layout of current_packet_visual
        self.play(
            brace_customer_frame.animate.next_to(customer_frame_parts, DOWN, buff=0.2),
            label_customer_frame.animate.next_to(brace_customer_frame, DOWN, buff=0.1),
            # mpls_brace_group should be updated if object references changed
            brace_mpls.animate.next_to(VGroup(current_packet_visual.submobjects[1], current_packet_visual.submobjects[2]), UP, buff=0.2), # Assumes ProviderHdr, T-Label, VC-Label ...
            # Let's use the actual objects: provider_header, transport_label, vc_label
            # Order in current_packet_visual: provider_header, transport_label, vc_label, control_word, customer_frame_parts
            brace_mpls.animate.next_to(VGroup(transport_label, vc_label), UP, buff=0.2),
            label_mpls.animate.next_to(brace_mpls, UP, buff=0.1)
        )


        brace_provider_hdr = Brace(provider_header, direction=UP, buff=0.2)
        label_provider_hdr = brace_provider_hdr.get_text("Provider Encapsulation", font_size=24)
        
        # Ensure annotations are not overlapping braces
        self.play(
            prov_annotation_text.animate.next_to(provider_header, UP, buff=0.8), # Move it higher
            t_annotation_text.animate.next_to(transport_label, UP, buff=0.8),
            vc_annotation_text.animate.next_to(vc_label, UP, buff=0.8),
            cw_annotation_text.animate.next_to(control_word, UP, buff=0.8)
        )

        self.play(Create(brace_provider_hdr), Write(label_provider_hdr))
        self.wait(3)

# To run this scene:
# manim -pql l2vpn_packet_scene.py L2VPNPacketStructureScene
# Use -pqm for medium quality, -pqh for high quality.
