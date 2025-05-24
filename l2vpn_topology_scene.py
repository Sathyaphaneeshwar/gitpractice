from manim import (
    Scene,
    Text,
    VGroup,
    Line,
    Create,
    Write,
    FadeIn,
    FadeOut,
    LaggedStart,
    SurroundingRectangle,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    config,
    Transform,
    Group,
)

# Assuming l2vpn_elements.py is in the same directory or accessible in PYTHONPATH
from l2vpn_elements import (
    create_router,
    CUSTOMER_COLOR,
    PROVIDER_COLOR,
    PACKET_COLOR, # Though not explicitly used, good to have if expanding
    LABEL_COLOR,
)

# Configure default font size for slides if needed
config.font_size = 36

class L2VPNTopologyScene(Scene):
    """
    Scene to illustrate L2 VPN topology components and their connected layout.
    """
    def construct(self):
        # --- Part 1: Introduce Components ---
        title_components = Text("L2 VPN Topology Components", font_size=48).to_edge(UP)
        self.play(Write(title_components))
        self.wait(0.5)

        # CE Router
        ce_router_example = create_router("CE1", CUSTOMER_COLOR).scale(0.8)
        ce_label = Text("CE: Customer Edge Router", font_size=28).next_to(ce_router_example, RIGHT, buff=0.5)
        ce_desc = Text("At customer premise, connects to provider.", font_size=24, color=LABEL_COLOR).next_to(ce_label, DOWN, buff=0.2, aligned_edge=LEFT)
        ce_group = VGroup(ce_router_example, ce_label, ce_desc).move_to(ORIGIN + UP * 1.5)

        self.play(Create(ce_router_example))
        self.play(Write(ce_label))
        self.play(FadeIn(ce_desc, shift=DOWN*0.2))
        self.wait(1)

        # PE Router
        pe_router_example = create_router("PE1", PROVIDER_COLOR).scale(0.8)
        pe_label = Text("PE: Provider Edge Router", font_size=28).next_to(pe_router_example, RIGHT, buff=0.5)
        pe_desc = Text("At provider network edge, L2 VPN functions happen here.", font_size=24, color=LABEL_COLOR).next_to(pe_label, DOWN, buff=0.2, aligned_edge=LEFT)
        pe_group = VGroup(pe_router_example, pe_label, pe_desc).move_to(ORIGIN - UP * 0.5)
        
        # Adjust description to fit
        pe_desc_line2 = Text("(encapsulation/decapsulation)", font_size=20, color=LABEL_COLOR).next_to(pe_desc, DOWN, buff=0.1, aligned_edge=LEFT)
        pe_desc_full = VGroup(pe_desc, pe_desc_line2)


        self.play(Create(pe_router_example))
        self.play(Write(pe_label))
        self.play(FadeIn(pe_desc_full, shift=DOWN*0.2))
        self.wait(1)
        
        # P Router
        p_router_example = create_router("P", PROVIDER_COLOR).scale(0.8)
        p_label = Text("P: Provider Router", font_size=28).next_to(p_router_example, RIGHT, buff=0.5)
        p_desc = Text("Core provider router, MPLS switching, unaware of customer VPNs.", font_size=24, color=LABEL_COLOR).next_to(p_label, DOWN, buff=0.2, aligned_edge=LEFT)
        p_group = VGroup(p_router_example, p_label, p_desc).move_to(ORIGIN - UP * 2.5)

        self.play(Create(p_router_example))
        self.play(Write(p_label))
        self.play(FadeIn(p_desc, shift=DOWN*0.2))
        self.wait(2)

        # Group all component descriptions for easy fade out
        components_explained = VGroup(ce_group, pe_group, p_group)

        # --- Transition ---
        self.play(
            FadeOut(components_explained),
            FadeOut(title_components)
        )
        self.wait(0.5)

        # --- Part 2: Show Connected Topology ---
        title_topology = Text("L2 VPN Connected Topology", font_size=48).to_edge(UP)
        self.play(Write(title_topology))
        self.wait(0.5)

        # Create router instances for the topology
        ce_a1 = create_router("CE-A1", CUSTOMER_COLOR).scale(0.9)
        pe_1 = create_router("PE1", PROVIDER_COLOR).scale(0.9)
        p_1 = create_router("P1", PROVIDER_COLOR).scale(0.9)
        p_2 = create_router("P2", PROVIDER_COLOR).scale(0.9)
        pe_2 = create_router("PE2", PROVIDER_COLOR).scale(0.9)
        ce_b1 = create_router("CE-B1", CUSTOMER_COLOR).scale(0.9)

        # Position routers
        ce_a1.move_to(LEFT * 5.5 + UP * 1)
        pe_1.move_to(LEFT * 2.5 + UP * 1)
        p_1.move_to(ORIGIN + UP * 1) # Center P1 slightly
        p_2.move_to(RIGHT * 2.5 + UP * 1)
        pe_2.move_to(RIGHT * 5.5 + UP * 1) # Mistake here, PE2 should be closer to P2
        # Corrected pe_2 position
        pe_2.move_to(RIGHT * 2.5 + DOWN * 1.5) # Let's try a different layout for core
        p_1.move_to(LEFT * 1 + DOWN * 0.25)
        p_2.move_to(RIGHT * 1 + DOWN * 0.25)
        pe_1.move_to(LEFT * 3.5 + DOWN * 0.25)
        pe_2.move_to(RIGHT * 3.5 + DOWN * 0.25)
        
        ce_a1.move_to(LEFT * 5.5 + DOWN * 0.25)
        ce_b1.move_to(RIGHT * 5.5 + DOWN * 0.25)


        # Provider Network Visual Grouping (optional)
        provider_core_routers = VGroup(pe_1, p_1, p_2, pe_2)
        provider_network_rect = SurroundingRectangle(
            provider_core_routers, 
            color=PROVIDER_COLOR, 
            buff=0.5, 
            corner_radius=0.2,
            stroke_width=2,
            fill_color=PROVIDER_COLOR,
            fill_opacity=0.1
        )
        provider_network_label = Text("Provider Network", font_size=24).next_to(provider_network_rect, UP, buff=0.2)
        
        # Animate router appearances
        # Customer Site A elements
        site_a_label = Text("Customer Site A", font_size=24).next_to(ce_a1, UP, buff=0.3)
        
        # Customer Site B elements
        site_b_label = Text("Customer Site B", font_size=24).next_to(ce_b1, UP, buff=0.3)

        self.play(
            LaggedStart(
                Create(ce_a1), Write(site_a_label),
                Create(pe_1),
                Create(p_1),
                Create(p_2),
                Create(pe_2),
                Create(ce_b1), Write(site_b_label),
                Create(provider_network_rect), Write(provider_network_label),
                lag_ratio=0.3,
                run_time=4
            )
        )
        self.wait(0.5)

        # Create and animate lines
        lines = VGroup(
            Line(ce_a1.get_right(), pe_1.get_left(), color=WHITE, stroke_width=3),
            Line(pe_1.get_right(), p_1.get_left(), color=WHITE, stroke_width=3),
            Line(p_1.get_right(), p_2.get_left(), color=WHITE, stroke_width=3),
            Line(p_2.get_right(), pe_2.get_left(), color=WHITE, stroke_width=3),
            Line(pe_2.get_right(), ce_b1.get_left(), color=WHITE, stroke_width=3)
        )

        self.play(Create(lines), run_time=3)
        self.wait(3)

# To run this scene:
# manim -pql l2vpn_topology_scene.py L2VPNTopologyScene
# Use -pqm for medium quality, -pqh for high quality.
