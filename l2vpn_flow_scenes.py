from manim import (
    Scene,
    Text,
    VGroup,
    Line,
    Dot,
    Create,
    Write,
    FadeIn,
    FadeOut,
    MoveAlongPath,
    Transform,
    ReplacementTransform,
    Group,
    SurroundingRectangle,
    LaggedStart,
    Arrow,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    GREY_BROWN,
    YELLOW_C,
    BLUE_E,
    GREEN_C, 
    PINK, 
    config,
    Rectangle, 
    Brace, 
    AnimationGroup, 
)

# Project specific imports
from l2vpn_elements import (
    create_router,
    create_packet_representation, 
    CUSTOMER_COLOR,
    PROVIDER_COLOR,
    PACKET_COLOR,
    LABEL_COLOR,
)

# Configure default font size for slides if needed
config.font_size = 28

# --- Helper function for Topology ---
def create_l2vpn_topology():
    """Creates and returns a VGroup of the L2 VPN topology."""
    ce_a1 = create_router("CE-A1", CUSTOMER_COLOR).scale(0.8)
    pe_1 = create_router("PE1", PROVIDER_COLOR).scale(0.8)
    p_1 = create_router("P1", PROVIDER_COLOR).scale(0.8)
    p_2 = create_router("P2", PROVIDER_COLOR).scale(0.8)
    pe_2 = create_router("PE2", PROVIDER_COLOR).scale(0.8)
    ce_b1 = create_router("CE-B1", CUSTOMER_COLOR).scale(0.8)

    ce_a1.move_to(LEFT * 6 + DOWN * 0.5) 
    pe_1.move_to(LEFT * 3.5 + DOWN * 0.5)
    p_1.move_to(LEFT * 1 + DOWN * 0.5)
    p_2.move_to(RIGHT * 1.5 + DOWN * 0.5) 
    pe_2.move_to(RIGHT * 4 + DOWN * 0.5) 
    ce_b1.move_to(RIGHT * 6.5 + DOWN * 0.5) 

    routers = VGroup(ce_a1, pe_1, p_1, p_2, pe_2, ce_b1)

    lines = VGroup(
        Line(ce_a1.get_right(), pe_1.get_left(), color=WHITE, stroke_width=2),
        Line(pe_1.get_right(), p_1.get_left(), color=WHITE, stroke_width=2),
        Line(p_1.get_right(), p_2.get_left(), color=WHITE, stroke_width=2),
        Line(p_2.get_right(), pe_2.get_left(), color=WHITE, stroke_width=2),
        Line(pe_2.get_right(), ce_b1.get_left(), color=WHITE, stroke_width=2)
    )

    site_a_label = Text("Customer Site A", font_size=20).next_to(ce_a1, UP, buff=0.2)
    site_b_label = Text("Customer Site B", font_size=20).next_to(ce_b1, UP, buff=0.2)
    provider_label = Text("Provider Network Core", font_size=20).next_to(VGroup(p_1, p_2), UP, buff=1.2)
    labels = VGroup(site_a_label, site_b_label, provider_label)

    return VGroup(routers, lines, labels)

# --- Helper function for creating packet segments ---
def create_packet_segment(label_text, width, height, color, text_color=WHITE, font_size=16):
    rect = Rectangle(width=width, height=height, color=color, fill_color=color, fill_opacity=0.7)
    label = Text(label_text, font_size=font_size, color=text_color).move_to(rect.get_center())
    return VGroup(rect, label)

# --- Function to construct a full L2VPN Packet ---
def create_full_l2vpn_packet(t_label_text="T-L1"):
    p_hdr = create_packet_segment("P-Hdr", 1.0, 0.5, PROVIDER_COLOR)
    t_label = create_packet_segment(t_label_text, 0.8, 0.5, BLUE_E) 
    vc_label = create_packet_segment("VC-L", 0.8, 0.5, LABEL_COLOR) 
    cw = create_packet_segment("CW", 0.6, 0.5, GREY_BROWN) 
    eth_hdr = create_packet_segment("Eth Hdr", 1.2, 0.5, CUSTOMER_COLOR) 
    payload = create_packet_segment("Payload", 1.8, 0.5, PACKET_COLOR) 
    
    full_packet = VGroup(p_hdr, t_label, vc_label, cw, eth_hdr, payload).arrange(RIGHT, buff=0)
    return full_packet

# --- Function to construct a packet after PHP ---
def create_php_packet():
    p_hdr = create_packet_segment("P-Hdr", 1.0, 0.5, PROVIDER_COLOR)
    vc_label = create_packet_segment("VC-L", 0.8, 0.5, LABEL_COLOR)
    cw = create_packet_segment("CW", 0.6, 0.5, GREY_BROWN)
    eth_hdr = create_packet_segment("Eth Hdr", 1.2, 0.5, CUSTOMER_COLOR)
    payload = create_packet_segment("Payload", 1.8, 0.5, PACKET_COLOR)
    
    packet = VGroup(p_hdr, vc_label, cw, eth_hdr, payload).arrange(RIGHT, buff=0)
    return packet

class PacketFlowScene_CE1_to_PE1(Scene):
    def construct(self):
        title = Text("Packet Flow: Site A to PE1", font_size=40).to_edge(UP)
        self.play(Write(title))
        topology = create_l2vpn_topology().scale(0.9).shift(DOWN*0.5)
        ce_a1, pe_1 = topology[0][0], topology[0][1] 
        self.play(Create(topology[0]), Create(topology[1]), Write(topology[2])) 
        self.wait(0.5)
        origination_text = Text("Host A (Site A) sends an Ethernet frame to Host B (Site B).", font_size=24)
        origination_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(origination_text))
        self.wait(0.5)
        eth_hdr = create_packet_segment("Eth Hdr", 1.2, 0.5, CUSTOMER_COLOR)
        payload = create_packet_segment("Payload", 1.8, 0.5, PACKET_COLOR)
        customer_packet = VGroup(eth_hdr, payload).arrange(RIGHT, buff=0)
        customer_packet.scale(0.7).next_to(ce_a1, RIGHT, buff=0.1)
        host_a_dot = Dot(color=CUSTOMER_COLOR).next_to(ce_a1, LEFT, buff=0.2)
        self.play(FadeIn(host_a_dot))
        packet_origin_point = ce_a1.get_right() + RIGHT*0.01 
        customer_packet.move_to(packet_origin_point + RIGHT * customer_packet.width/2)
        self.play(Create(customer_packet))
        self.wait(0.5)
        self.play(FadeOut(host_a_dot)) 
        link_ce1_pe1 = topology[1][0] 
        self.play(
            MoveAlongPath(customer_packet, Line(customer_packet.get_center(), pe_1.get_left() - LEFT*customer_packet.width/2 - LEFT*0.1)),
            link_ce1_pe1.animate.set_color(YELLOW_C), run_time=2 )
        self.play(link_ce1_pe1.animate.set_color(WHITE)) 
        self.wait(2)

class PacketFlowScene_PE1_Encapsulation(Scene):
    def construct(self):
        title = Text("Packet Encapsulation at PE1 (Ingress PE)", font_size=40).to_edge(UP)
        self.play(Write(title))
        full_topology = create_l2vpn_topology().scale(0.9).shift(DOWN*1.5)
        pe_1_router = full_topology[0][1] 
        other_elements = VGroup( full_topology[0][0], full_topology[0][2:], full_topology[1], full_topology[2] )
        self.play(Create(pe_1_router), FadeIn(other_elements, lag_ratio=0.1, run_time=1))
        self.play(other_elements.animate.set_opacity(0.3))
        self.play(pe_1_router.animate.scale(1.2).move_to(LEFT*3 + UP*0.5)) 
        self.wait(0.5)
        eth_hdr = create_packet_segment("Eth Hdr", 1.2, 0.5, CUSTOMER_COLOR)
        payload = create_packet_segment("Payload", 1.8, 0.5, PACKET_COLOR)
        current_packet = VGroup(eth_hdr, payload).arrange(RIGHT, buff=0).scale(0.7)
        current_packet.next_to(pe_1_router, RIGHT, buff=0.5).shift(DOWN*0.2)
        self.play(FadeIn(current_packet))
        arrival_text = Text("Ethernet frame arrives at PE1.", font_size=24).next_to(title, DOWN, buff=0.3)
        self.play(Write(arrival_text))
        self.wait(1)
        encap_text = Text("PE1 identifies L2 VPN service and encapsulates the frame:", font_size=24)
        encap_text.next_to(arrival_text, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(ReplacementTransform(arrival_text, encap_text)) 
        self.play(current_packet.animate.move_to(ORIGIN + DOWN*0.5).scale(1.1)) 
        self.wait(0.5)
        packet_segments_to_add = [
            ("CW", 0.6, GREY_BROWN), ("VC-L", 0.8, LABEL_COLOR),
            ("T-L1", 0.8, BLUE_E), ("P-Hdr", 1.0, PROVIDER_COLOR) ]
        for label_text, width, color in packet_segments_to_add:
            segment = create_packet_segment(label_text, width, 0.5, color)
            segment.next_to(current_packet, LEFT, buff=0.1, coor_mask=UP).align_to(current_packet, DOWN).shift(LEFT*0.1)
            self.play(FadeIn(segment, shift=RIGHT*0.5))
            new_packet_group = VGroup(segment, current_packet).arrange(RIGHT, buff=0)
            self.play( current_packet.animate.next_to(segment, RIGHT, buff=0),
                segment.animate.move_to(new_packet_group[0].get_center()) )
            current_packet = new_packet_group 
            self.wait(0.5)
        result_text = Text("Fully encapsulated L2 VPN packet:", font_size=24)
        result_text.next_to(encap_text, DOWN, buff=0.5 + current_packet.height)
        self.play(Write(result_text))
        final_packet_brace = Brace(current_packet, direction=DOWN, buff=0.2)
        final_packet_label = final_packet_brace.get_text("L2 VPN Packet", font_size=20)
        self.play(Create(final_packet_brace), Write(final_packet_label))
        self.wait(3)

class PacketFlowScene_Core_Transit_Part1(Scene):
    def construct(self):
        title = Text("Core Transit: PE1 -> P1 -> P2 (Transport Label Focus)", font_size=36).to_edge(UP)
        self.play(Write(title))
        topology = create_l2vpn_topology().scale(0.9).shift(DOWN*0.5)
        pe_1, p_1, p_2, pe_2 = topology[0][1], topology[0][2], topology[0][3], topology[0][4]
        ce_elements = VGroup(topology[0][0], topology[0][5], topology[2][0], topology[2][1]) 
        self.play( Create(VGroup(pe_1, p_1, p_2, pe_2)), Create(VGroup(topology[1][1], topology[1][2], topology[1][3])),
            Write(topology[2][2]), FadeIn(ce_elements.set_opacity(0.3)) )
        self.wait(0.5)
        packet = create_full_l2vpn_packet(t_label_text="T-L1").scale(0.8)
        packet.next_to(pe_1, RIGHT, buff=0.1)
        self.play(FadeIn(packet))
        text_pe1_forward = Text("PE1 forwards packet based on T-L1.", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_pe1_forward))
        t_label1_visual = packet[1] 
        highlight_rect_tl1 = SurroundingRectangle(t_label1_visual, color=YELLOW_C, buff=0.05)
        self.play(Create(highlight_rect_tl1))
        link_pe1_p1 = topology[1][1]
        self.play( MoveAlongPath(packet, Line(packet.get_center(), p_1.get_left() - LEFT*packet.width/2 - LEFT*0.1)),
            link_pe1_p1.animate.set_color(YELLOW_C), FadeOut(highlight_rect_tl1), run_time=2 )
        self.play(link_pe1_p1.animate.set_color(WHITE))
        self.play(FadeOut(text_pe1_forward))
        self.wait(0.5)
        text_at_p1 = Text("P1 inspects T-L1 and swaps it with T-L2.", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_at_p1))
        old_t_label = packet[1]
        new_t_label_visual = create_packet_segment("T-L2", old_t_label[0].width, old_t_label[0].height, GREEN_C)
        new_t_label_visual.move_to(old_t_label.get_center())
        self.play(FadeOut(old_t_label[1])) 
        self.play( Transform(old_t_label[0], new_t_label_visual[0]), FadeIn(new_t_label_visual[1]) )
        packet.submobjects[1] = new_t_label_visual 
        self.wait(1)
        self.play(FadeOut(text_at_p1))
        text_p1_forward = Text("P1 forwards packet using new T-L2.", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_p1_forward))
        t_label2_visual = packet[1]
        highlight_rect_tl2 = SurroundingRectangle(t_label2_visual, color=YELLOW_C, buff=0.05)
        self.play(Create(highlight_rect_tl2))
        link_p1_p2 = topology[1][2]
        self.play( MoveAlongPath(packet, Line(packet.get_center(), p_2.get_left() - LEFT*packet.width/2 - LEFT*0.1)),
            link_p1_p2.animate.set_color(YELLOW_C), FadeOut(highlight_rect_tl2), run_time=2 )
        self.play(link_p1_p2.animate.set_color(WHITE))
        self.play(FadeOut(text_p1_forward))
        self.wait(2)

class PacketFlowScene_Core_Transit_Part2(Scene):
    def construct(self):
        title = Text("Core Transit: P2 -> PE2 (PHP)", font_size=36).to_edge(UP)
        self.play(Write(title))
        topology = create_l2vpn_topology().scale(0.9).shift(DOWN*0.5)
        p_1, p_2, pe_2 = topology[0][2], topology[0][3], topology[0][4] 
        other_core_routers = VGroup(topology[0][1]) 
        ce_elements = VGroup(topology[0][0], topology[0][5], topology[2][0], topology[2][1]) 
        active_routers = VGroup(p_1, p_2, pe_2) 
        active_links = VGroup(topology[1][2], topology[1][3]) 
        self.play( Create(active_routers), Create(active_links), Write(topology[2][2]),
            FadeIn(ce_elements.set_opacity(0.3)), FadeIn(other_core_routers.set_opacity(0.3)) )
        self.wait(0.5)
        packet = create_full_l2vpn_packet(t_label_text="T-L2").scale(0.8)
        packet[1][0].set_fill(GREEN_C, opacity=0.7); packet[1][0].set_stroke(GREEN_C); packet[1][1].set_color(WHITE) 
        packet.move_to(p_2.get_left() - LEFT*packet.width/2 - LEFT*0.1) 
        self.play(FadeIn(packet))
        text_at_p2_inspect = Text("P2 inspects T-L2.", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_at_p2_inspect))
        t_label2_visual = packet[1]
        highlight_rect_tl2_at_p2 = SurroundingRectangle(t_label2_visual, color=YELLOW_C, buff=0.05)
        self.play(Create(highlight_rect_tl2_at_p2)); self.wait(0.5)
        self.play(FadeOut(highlight_rect_tl2_at_p2)); self.play(FadeOut(text_at_p2_inspect))
        text_php = Text("P2 performs Penultimate Hop Popping (PHP), removing T-L2.", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_php))
        t_label_to_remove = packet[1] 
        new_packet_parts = VGroup()
        for i, part in enumerate(packet):
            if i != 1: new_packet_parts.add(part.copy()) 
        new_packet_parts.arrange(RIGHT, buff=0).move_to(packet.get_center()) 
        self.play( FadeOut(t_label_to_remove, shift=DOWN*0.5), 
            AnimationGroup(*[ReplacementTransform(packet[i], new_packet_parts[j if i > 1 else i]) for j, i in enumerate([0,2,3,4,5])]),
            run_time=1.5 )
        packet = new_packet_parts
        self.wait(1); self.play(FadeOut(text_php))
        text_p2_forwards = Text("P2 forwards packet (now without T-Label) to PE2.", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_p2_forwards))
        vc_label_visual_php = packet[1] 
        highlight_rect_vcl = SurroundingRectangle(vc_label_visual_php, color=PINK, buff=0.05)
        self.play(Create(highlight_rect_vcl))
        link_p2_pe2 = topology[1][3]
        self.play( MoveAlongPath(packet, Line(packet.get_center(), pe_2.get_left() - LEFT*packet.width/2 - LEFT*0.1)),
            link_p2_pe2.animate.set_color(YELLOW_C), FadeOut(highlight_rect_vcl), run_time=2 )
        self.play(link_p2_pe2.animate.set_color(WHITE)); self.play(FadeOut(text_p2_forwards))
        self.wait(2)

class PacketFlowScene_PE2_Decapsulation(Scene):
    """
    Scene 5: Decapsulation of the packet at PE2 (Egress PE).
    """
    def construct(self):
        title = Text("Packet Decapsulation at PE2 (Egress PE)", font_size=36).to_edge(UP)
        self.play(Write(title))

        topology = create_l2vpn_topology().scale(0.9).shift(DOWN*1.5) # Shift down for more space
        pe_2 = topology[0][4]
        ce_b1 = topology[0][5]
        
        # Dim other routers and CE_A1 elements
        dimmed_routers = VGroup(topology[0][0], topology[0][1], topology[0][2], topology[0][3]) # CE_A1, PE1, P1, P2
        dimmed_links = VGroup(topology[1][0], topology[1][1], topology[1][2]) # Links up to P2
        dimmed_labels = VGroup(topology[2][0], topology[2][2]) # Site A label, Provider label

        self.play(
            Create(VGroup(pe_2, ce_b1)), # Active routers PE2, CE_B1
            Create(topology[1][4]), # Link PE2-CE_B1
            Write(topology[2][1]), # Site B label
            FadeIn(dimmed_routers.set_opacity(0.3)),
            FadeIn(dimmed_links.set_opacity(0.3)),
            FadeIn(dimmed_labels.set_opacity(0.3))
        )
        self.play(pe_2.animate.scale(1.2).move_to(LEFT*2 + UP*0.5), # Make PE2 prominent
                  ce_b1.animate.move_to(RIGHT*2.5 + UP*0.5)) # Position CE_B1 for later
        self.wait(0.5)

        # Packet after PHP arrives at PE2
        # Structure: [P-Hdr (0)][VC-L (1)][CW (2)][Eth Hdr (3)][Payload (4)]
        current_packet = create_php_packet().scale(0.9)
        current_packet.next_to(pe_2, RIGHT, buff=0.5).shift(UP*0.5) # Position near PE2, higher up
        self.play(FadeIn(current_packet))

        text_arrival = Text("Packet arrives at PE2 (Egress PE).", font_size=24).next_to(title, DOWN, buff=0.2)
        self.play(Write(text_arrival))
        self.wait(1)

        text_inspect_vc = Text("PE2 inspects VC Label for L2 VPN service and customer interface.", font_size=24)
        text_inspect_vc.next_to(text_arrival, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(ReplacementTransform(text_arrival, text_inspect_vc))

        # Highlight VC Label
        vc_label_visual = current_packet[1] # VC-L is the second element
        highlight_rect_vcl = SurroundingRectangle(vc_label_visual, color=PINK, buff=0.05)
        self.play(Create(highlight_rect_vcl))
        self.wait(1)
        self.play(FadeOut(highlight_rect_vcl))

        # Decapsulation steps
        # Center the packet for transformations
        self.play(current_packet.animate.center().shift(DOWN*0.5))
        self.wait(0.5)
        
        decap_steps_text_y_pos = text_inspect_vc.get_y() - text_inspect_vc.height - 0.5

        # 1. Remove Provider Header (P-Hdr)
        p_hdr_to_remove = current_packet[0]
        text_remove_phdr = Text("1. Remove Provider Header (P-Hdr)", font_size=22).set_y(decap_steps_text_y_pos).to_edge(LEFT, buff=0.5)
        self.play(Write(text_remove_phdr))
        
        remaining_after_phdr = VGroup(*current_packet.submobjects[1:]).copy()
        remaining_after_phdr.arrange(RIGHT, buff=0).move_to(current_packet.get_center() + p_hdr_to_remove.width/2 * RIGHT)

        self.play(
            FadeOut(p_hdr_to_remove, shift=LEFT*0.5),
            current_packet.submobjects[1:].animate.move_to(remaining_after_phdr.get_center())
        )
        current_packet = VGroup(*current_packet.submobjects[1:]) # Update current_packet reference
        self.wait(1)
        self.play(FadeOut(text_remove_phdr))

        # 2. Remove VC Label (VC-L)
        vc_label_to_remove = current_packet[0] # VC-L is now the first element
        text_remove_vcl = Text("2. Remove VC Label (VC-L)", font_size=22).set_y(decap_steps_text_y_pos).to_edge(LEFT, buff=0.5)
        self.play(Write(text_remove_vcl))
        
        remaining_after_vcl = VGroup(*current_packet.submobjects[1:]).copy()
        remaining_after_vcl.arrange(RIGHT, buff=0).move_to(current_packet.get_center() + vc_label_to_remove.width/2 * RIGHT)

        self.play(
            FadeOut(vc_label_to_remove, shift=LEFT*0.5),
            current_packet.submobjects[1:].animate.move_to(remaining_after_vcl.get_center())
        )
        current_packet = VGroup(*current_packet.submobjects[1:])
        self.wait(1)
        self.play(FadeOut(text_remove_vcl))

        # 3. Remove Control Word (CW)
        cw_to_remove = current_packet[0] # CW is now the first element
        text_remove_cw = Text("3. Remove Control Word (CW)", font_size=22).set_y(decap_steps_text_y_pos).to_edge(LEFT, buff=0.5)
        self.play(Write(text_remove_cw))

        original_customer_frame = VGroup(*current_packet.submobjects[1:]).copy() # Eth Hdr, Payload
        original_customer_frame.arrange(RIGHT, buff=0).move_to(current_packet.get_center() + cw_to_remove.width/2 * RIGHT)

        self.play(
            FadeOut(cw_to_remove, shift=LEFT*0.5),
            current_packet.submobjects[1:].animate.move_to(original_customer_frame.get_center())
        )
        current_packet = VGroup(*current_packet.submobjects[1:]) # Now it's the original Eth Frame
        self.wait(1)
        self.play(FadeOut(text_remove_cw))
        
        # Result
        text_recovered = Text("Original Customer Ethernet Frame is recovered!", font_size=28, color=YELLOW_C)
        text_recovered.next_to(current_packet, UP, buff=0.5)
        
        frame_brace = Brace(current_packet, direction=DOWN, buff=0.2)
        frame_label = frame_brace.get_text("Customer Ethernet Frame", font_size=22)
        
        self.play(Write(text_recovered), Create(frame_brace), Write(frame_label))
        self.wait(3)

class PacketFlowScene_PE2_to_CE2(Scene):
    """
    Scene 6: Packet delivery from PE2 to CE_B1 (Customer Site B).
    """
    def construct(self):
        title = Text("Packet Delivery to Site B", font_size=40).to_edge(UP)
        self.play(Write(title))

        topology = create_l2vpn_topology().scale(0.9).shift(DOWN*0.5)
        pe_2 = topology[0][4]
        ce_b1 = topology[0][5]
        link_pe2_ceb1 = topology[1][4]
        site_b_label_topo = topology[2][1]

        # Dim other elements
        dimmed_elements = VGroup(
            topology[0][0], topology[0][1], topology[0][2], topology[0][3], # CE_A1, PE1, P1, P2
            topology[1][0], topology[1][1], topology[1][2], topology[1][3], # Links up to PE2
            topology[2][0], topology[2][2] # Site A label, Provider label
        )
        self.play(
            Create(VGroup(pe_2, ce_b1)),
            Create(link_pe2_ceb1),
            Write(site_b_label_topo),
            FadeIn(dimmed_elements.set_opacity(0.3))
        )
        self.wait(0.5)

        # Original Customer Ethernet Frame at PE2
        eth_hdr = create_packet_segment("Eth Hdr", 1.2, 0.5, CUSTOMER_COLOR)
        payload = create_packet_segment("Payload", 1.8, 0.5, PACKET_COLOR)
        customer_frame = VGroup(eth_hdr, payload).arrange(RIGHT, buff=0).scale(0.8)
        customer_frame.next_to(pe_2, RIGHT, buff=0.1)
        self.play(FadeIn(customer_frame))

        # Text: PE2 forwards to CE_B1
        text_pe2_forwards = Text("PE2 forwards the original Ethernet frame to CE_B1.", font_size=24)
        text_pe2_forwards.next_to(title, DOWN, buff=0.3)
        self.play(Write(text_pe2_forwards))
        self.wait(0.5)

        # Move packet PE2 to CE_B1
        self.play(
            MoveAlongPath(customer_frame, Line(customer_frame.get_center(), ce_b1.get_left() - LEFT*customer_frame.width/2 - LEFT*0.1)),
            link_pe2_ceb1.animate.set_color(YELLOW_C),
            run_time=2
        )
        self.play(link_pe2_ceb1.animate.set_color(WHITE))
        self.wait(0.5)

        # Arrival at Site B
        text_arrival_ceb1 = Text("Frame arrives at CE_B1 (Customer Site B).", font_size=24)
        text_arrival_ceb1.next_to(text_pe2_forwards, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(ReplacementTransform(text_pe2_forwards, text_arrival_ceb1))

        host_b_dot = Dot(color=CUSTOMER_COLOR).next_to(ce_b1, RIGHT, buff=0.2)
        text_delivered_host_b = Text("Delivered to Host B!", font_size=22, color=GREEN_C)
        text_delivered_host_b.next_to(host_b_dot, UP, buff=0.2)

        self.play(FadeIn(host_b_dot), Write(text_delivered_host_b))
        self.play(FadeOut(customer_frame.move_to(host_b_dot.get_center()))) # Packet moves into host
        
        self.wait(3)

# To run these scenes:
# manim -pql l2vpn_flow_scenes.py PacketFlowScene_PE2_Decapsulation
# manim -pql l2vpn_flow_scenes.py PacketFlowScene_PE2_to_CE2
# manim -pql l2vpn_flow_scenes.py (to run all scenes in the file)
