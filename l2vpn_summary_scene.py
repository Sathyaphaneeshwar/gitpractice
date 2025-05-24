from manim import (
    Scene,
    Text,
    VGroup,
    Line,
    Dot,
    Ellipse,
    Create,
    Write,
    FadeIn,
    FadeOut,
    LaggedStart,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    YELLOW_C,
    config,
)

# Project specific imports
from l2vpn_elements import (
    create_router,
    CUSTOMER_COLOR,
    PROVIDER_COLOR,
    LABEL_COLOR, # For dot points or highlights if needed
)

# Configure default font size for slides if needed
config.font_size = 30 # Adjusted for summary slide

class L2VPNSummaryScene(Scene):
    """
    Scene to summarize the key takeaways of the L2 VPN animation.
    """
    def construct(self):
        # Title
        title = Text("L2 VPN: Key Takeaways", font_size=44, color=YELLOW_C).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Summary Points
        summary_points_text = [
            "Connects separate Layer 2 customer networks over a provider's Layer 3 MPLS core.",
            "Customer traffic (Ethernet frames) is encapsulated and tunneled by PEs.",
            "Provider Edge (PE) routers are key: perform encapsulation/decapsulation.",
            "Provider Core (P) routers switch MPLS packets based on labels, unaware of customer data.",
            "Control plane (e.g., LDP, BGP) sets up VPN tunnels and labels between PEs.",
            "Benefits: Extends L2 domains, simplifies customer network, leverages provider infrastructure."
        ]

        bullet_items = VGroup()
        for i, point_text in enumerate(summary_points_text):
            dot = Dot(radius=0.06, color=LABEL_COLOR).next_to(ORIGIN, LEFT, buff=0)
            text = Text(point_text, font_size=26, PURE_BLACK=WHITE).next_to(dot, RIGHT, buff=0.25) # Using WHITE for text
            bullet_item = VGroup(dot, text).scale(0.9) # Scale down for better fit
            bullet_items.add(bullet_item)
        
        bullet_items.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        bullet_items.next_to(title, DOWN, buff=0.5).align_to(LEFT, LEFT).shift(LEFT*1.5) # Shift left for diagram space

        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT*0.3) for item in bullet_items], lag_ratio=0.5, run_time=len(summary_points_text)*0.8))
        self.wait(2) # Hold points for a bit

        # Optional Concluding Diagram (from L2VPNIntroScene2)
        # Customer Site A
        site_a_router = create_router("CE A", CUSTOMER_COLOR).scale(0.6)
        site_a_label_text = Text("Site A", font_size=20).next_to(site_a_router, DOWN, buff=0.15)
        site_a_group = VGroup(site_a_router, site_a_label_text)

        # Customer Site B
        site_b_router = create_router("CE B", CUSTOMER_COLOR).scale(0.6)
        site_b_label_text = Text("Site B", font_size=20).next_to(site_b_router, DOWN, buff=0.15)
        site_b_group = VGroup(site_b_router, site_b_label_text)

        # Provider Cloud
        provider_cloud_shape = Ellipse(width=3.5, height=1.8, color=PROVIDER_COLOR, fill_color=PROVIDER_COLOR, fill_opacity=0.3)
        provider_cloud_label_text = Text("Provider MPLS Core", font_size=20).move_to(provider_cloud_shape.get_center())
        provider_cloud_group = VGroup(provider_cloud_shape, provider_cloud_label_text)

        # Position diagram elements
        diagram_group = VGroup(site_a_group, site_b_group, provider_cloud_group)
        diagram_group.arrange(RIGHT, buff=1.5).scale(0.8) # Arrange horizontally and scale
        diagram_group.next_to(bullet_items, RIGHT, buff=1.0, aligned_edge=UP).shift(RIGHT*0.5)
        
        # Lines connecting sites to the cloud (adjust endpoints based on new diagram layout)
        # Need to re-position after arrange to get correct points
        site_a_group.move_to(diagram_group[0].get_center()) # Ensure they are where arrange placed them
        provider_cloud_group.move_to(diagram_group[1].get_center())
        site_b_group.move_to(diagram_group[2].get_center())
        
        # Re-arranging for a more typical cloud diagram
        site_a_group.move_to(LEFT*1.5 + DOWN * 0.8).scale(0.9) # Relative to diagram center
        site_b_group.move_to(RIGHT*1.5 + DOWN * 0.8).scale(0.9)
        provider_cloud_group.move_to(ORIGIN + UP * 0.2).scale(0.9)
        
        # Group and position the whole diagram
        full_diagram = VGroup(site_a_group, site_b_group, provider_cloud_group)
        full_diagram.scale(0.9).next_to(bullet_items, RIGHT, buff=0.7, aligned_edge=UP).shift(RIGHT*0.8 + DOWN*0.5)


        line_a_to_cloud = Line(site_a_router.get_top(), provider_cloud_shape.get_bottom(), color=WHITE, stroke_width=2)
        line_b_to_cloud = Line(site_b_router.get_top(), provider_cloud_shape.get_bottom(), color=WHITE, stroke_width=2)
        
        diagram_elements_to_create = VGroup(full_diagram, line_a_to_cloud, line_b_to_cloud)

        self.play(Create(diagram_elements_to_create), run_time=2)
        self.wait(1)

        # Final Text
        thank_you_text = Text("Thank You for Watching!", font_size=38, color=YELLOW_C)
        thank_you_text.next_to(bullet_items, DOWN, buff=1.0).align_to(ORIGIN, RIGHT) # Shift to center area
        
        # If diagram is present, shift thank you text
        if diagram_elements_to_create:
            thank_you_text.next_to(VGroup(bullet_items, diagram_elements_to_create), DOWN, buff=0.8)

        self.play(Write(thank_you_text))
        self.wait(3)

# To run this scene:
# manim -pql l2vpn_summary_scene.py L2VPNSummaryScene
# Use -pqm for medium quality, -pqh for high quality.
