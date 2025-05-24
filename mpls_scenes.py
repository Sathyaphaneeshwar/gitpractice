from manim import (
    Scene,
    Text,
    VGroup,
    Rectangle,
    Create,
    Write,
    FadeIn,
    FadeOut,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    BLUE,
    GREEN,
    YELLOW,
    Group,
    MoveToTarget,
    AnimationGroup,
    ReplacementTransform,
    config,
)

# Assuming l2vpn_elements.py is in the same directory or accessible in PYTHONPATH
from l2vpn_elements import (
    create_packet_representation,
    PROVIDER_COLOR,
    PACKET_COLOR, # For customer packet base
    LABEL_COLOR,  # For MPLS labels
    CUSTOMER_COLOR
)

# Configure default font size for slides if needed
config.font_size = 36

class MPLSBasicsScene1(Scene):
    """
    Scene 1: Introduction to MPLS and its labels.
    """
    def construct(self):
        # Title
        title = Text("MPLS: Multi-Protocol Label Switching", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Explanatory text
        explanation_text_1 = Text(
            "Used in provider networks to forward packets based on short labels, not IP addresses.",
            font_size=28
        ).next_to(title, DOWN, buff=0.5)
        explanation_text_2 = Text(
            "Improves forwarding speed and enables VPNs, Traffic Engineering.",
            font_size=28
        ).next_to(explanation_text_1, DOWN, buff=0.2)
        
        self.play(FadeIn(explanation_text_1, shift=DOWN*0.2))
        self.play(FadeIn(explanation_text_2, shift=DOWN*0.2))
        self.wait(1)

        # Introduce labels conceptually
        labels_intro_title = Text("Key MPLS Labels in L2 VPNs:", font_size=32, color=YELLOW).next_to(explanation_text_2, DOWN, buff=0.7)
        self.play(Write(labels_intro_title))
        self.wait(0.5)

        # Transport Label
        transport_label_title = Text("Transport Label (Outer Label):", font_size=28, weight="BOLD").next_to(labels_intro_title, DOWN, buff=0.4, aligned_edge=LEFT)
        transport_label_desc = Text("Guides packet across provider core (PE to PE).", font_size=24, color=LABEL_COLOR).next_to(transport_label_title, RIGHT, buff=0.3)
        
        # VC Label
        vc_label_title = Text("VC Label (Inner/Service Label):", font_size=28, weight="BOLD").next_to(transport_label_title, DOWN, buff=0.5, aligned_edge=LEFT)
        vc_label_desc = Text("Identifies the specific L2 VPN service for a customer.", font_size=24, color=LABEL_COLOR).next_to(vc_label_title, RIGHT, buff=0.3)

        # Visual representations for labels
        t_label_visual = Rectangle(width=1.5, height=0.6, color=PROVIDER_COLOR, fill_color=PROVIDER_COLOR, fill_opacity=0.3)
        t_label_text = Text("T-Label", font_size=20).move_to(t_label_visual.get_center())
        t_label_group = VGroup(t_label_visual, t_label_text).next_to(transport_label_desc, DOWN, buff=0.3, aligned_edge=LEFT).shift(LEFT*2)

        vc_label_visual = Rectangle(width=1.5, height=0.6, color=CUSTOMER_COLOR, fill_color=CUSTOMER_COLOR, fill_opacity=0.3) # Different color for VC
        vc_label_text = Text("VC-Label", font_size=20).move_to(vc_label_visual.get_center())
        vc_label_group = VGroup(vc_label_visual, vc_label_text).next_to(vc_label_desc, DOWN, buff=0.3, aligned_edge=LEFT).shift(LEFT*2)
        
        # Align groups for better visual
        labels_group = VGroup(
            VGroup(transport_label_title, transport_label_desc), 
            VGroup(vc_label_title, vc_label_desc)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(labels_intro_title, DOWN, buff=0.4)
        
        t_label_group.next_to(labels_group[0], DOWN, buff=0.2, aligned_edge=LEFT)
        vc_label_group.next_to(labels_group[1], DOWN, buff=0.2, aligned_edge=LEFT)


        self.play(Write(labels_group[0]))
        self.play(FadeIn(t_label_group, shift=UP*0.2))
        self.wait(0.5)
        self.play(Write(labels_group[1]))
        self.play(FadeIn(vc_label_group, shift=UP*0.2))
        
        self.wait(3)


class MPLSLabelingScene(Scene):
    """
    Scene 2: MPLS Packet Labeling Process.
    Shows how MPLS labels are pushed onto a customer packet.
    """
    def construct(self):
        # Title
        title = Text("MPLS Packet Labeling", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Customer Packet
        customer_packet = create_packet_representation("Cust. Data").scale(0.8)
        customer_packet.set_color(PACKET_COLOR) # Ensure base color
        customer_packet_label = Text("Customer L2 Frame", font_size=20).next_to(customer_packet, DOWN, buff=0.2)
        customer_packet_group = VGroup(customer_packet, customer_packet_label).move_to(ORIGIN + RIGHT * 2)
        
        self.play(FadeIn(customer_packet_group, shift=UP*0.5))
        self.wait(0.5)

        # MPLS Labels
        vc_label_rect = Rectangle(width=1.2, height=customer_packet[0].height, color=CUSTOMER_COLOR, fill_color=CUSTOMER_COLOR, fill_opacity=0.5)
        vc_label_text_obj = Text("VC L", font_size=20).move_to(vc_label_rect.get_center())
        vc_label = VGroup(vc_label_rect, vc_label_text_obj).next_to(customer_packet_group, LEFT, buff=0.5).shift(UP*2) # Start above

        transport_label_rect = Rectangle(width=1.2, height=customer_packet[0].height, color=PROVIDER_COLOR, fill_color=PROVIDER_COLOR, fill_opacity=0.5)
        transport_label_text_obj = Text("T L", font_size=20).move_to(transport_label_rect.get_center())
        transport_label = VGroup(transport_label_rect, transport_label_text_obj).next_to(vc_label, UP, buff=0.3) # Start above VC label

        self.play(FadeIn(vc_label), FadeIn(transport_label))
        self.wait(0.5)

        # Text explaining the process
        explanation_text = Text("Labels are 'pushed' onto the packet by the Provider Edge (PE) router.", font_size=28)
        explanation_text.next_to(customer_packet_group, DOWN, buff=1.5, aligned_edge=ORIGIN).to_edge(DOWN, buff=0.5)
        self.play(Write(explanation_text))
        self.wait(0.5)

        # Animate VC Label prepending
        target_vc_label_pos = customer_packet.get_left() - vc_label_rect.get_width()/2 * RIGHT + vc_label_rect.get_width()/2 * LEFT
        
        self.play(vc_label.animate.next_to(customer_packet, LEFT, buff=0))
        self.wait(0.2)
        
        # Group VC Label and Customer Packet
        labeled_packet_vc = VGroup(vc_label, customer_packet).arrange(RIGHT, buff=0)
        # No need to explicitly add and remove, just animate position of original objects then group for next step
        
        self.play(labeled_packet_vc.animate.move_to(ORIGIN + RIGHT * (vc_label_rect.width/2 + customer_packet[0].width/2)/2 ))
        self.wait(0.5)

        # Animate Transport Label prepending
        self.play(transport_label.animate.next_to(labeled_packet_vc, LEFT, buff=0))
        self.wait(0.2)

        # Final Labeled Packet
        full_mpls_packet = VGroup(transport_label, labeled_packet_vc).arrange(RIGHT, buff=0)
        self.play(full_mpls_packet.animate.move_to(ORIGIN).scale(0.9)) # Center and slightly shrink
        
        # Show final structure text
        final_structure_text = Text("[T-Label][VC-Label][Cust. Data]", font_size=24, color=LABEL_COLOR)
        final_structure_text.next_to(full_mpls_packet, DOWN, buff=0.3)
        self.play(Write(final_structure_text))

        self.wait(3)

# To run these scenes:
# manim -pql mpls_scenes.py MPLSBasicsScene1
# manim -pql mpls_scenes.py MPLSLabelingScene
# manim -pql mpls_scenes.py MPLSBasicsScene1 MPLSLabelingScene
