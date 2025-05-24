from manim import (
    Scene,
    Text,
    VGroup,
    UL,
    Line,
    Dot,
    Ellipse,
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
    config,
)

# Assuming l2vpn_elements.py is in the same directory or accessible in PYTHONPATH
from l2vpn_elements import (
    create_router,
    CUSTOMER_COLOR,
    PROVIDER_COLOR,
    LABEL_COLOR,
)

# Configure default font size for slides if needed
config.font_size = 36


class L2VPNIntroScene1(Scene):
    """
    Scene 1: Introduction to L2 VPNs.
    Displays the title and key characteristics of L2 VPNs.
    """
    def construct(self):
        # Title
        title = Text("What is an L2 VPN?", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Bullet points
        bullet_points_text = [
            "Connects geographically separate customer Layer 2 networks.",
            "Uses a Service Provider's Layer 3 (MPLS) backbone.",
            "Makes multiple sites appear as if they are on the same LAN.",
        ]

        bullets = VGroup()
        for i, point_text in enumerate(bullet_points_text):
            dot = Dot(radius=0.05).next_to(ORIGIN, LEFT, buff=0)
            text = Text(point_text, font_size=32, PURE_BLACK=LABEL_COLOR).next_to(dot, RIGHT, buff=0.2) # Pure black for text
            bullet_item = VGroup(dot, text).scale(0.8) # Scale down for better fit
            bullets.add(bullet_item)
        
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.7)

        for bullet in bullets:
            self.play(FadeIn(bullet, shift=RIGHT*0.5), run_time=0.7)
            self.wait(0.3)
            
        self.wait(3) # Hold the slide for a few seconds


class L2VPNIntroScene2(Scene):
    """
    Scene 2: Benefits of L2 VPNs and a simple diagram.
    Displays the title, key benefits, and a basic architectural diagram.
    """
    def construct(self):
        # Title
        title = Text("Why use L2 VPNs?", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Benefits bullet points
        benefits_text = [
            "Simplicity for the customer (extends L2 domain easily).",
            "Provider manages the complexity of the core network.",
            "Cost-effective way to connect sites.",
        ]

        benefits_bullets = VGroup()
        for i, point_text in enumerate(benefits_text):
            dot = Dot(radius=0.05).next_to(ORIGIN, LEFT, buff=0)
            text = Text(point_text, font_size=32, PURE_BLACK=LABEL_COLOR).next_to(dot, RIGHT, buff=0.2)
            benefit_item = VGroup(dot, text).scale(0.8)
            benefits_bullets.add(benefit_item)
        
        benefits_bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5).align_to(LEFT, LEFT).shift(LEFT*3.5) # Shift left for diagram space

        for bullet in benefits_bullets:
            self.play(FadeIn(bullet, shift=RIGHT*0.5), run_time=0.7)
            self.wait(0.3)
        
        self.wait(1)

        # Diagram elements
        # Customer Site A
        site_a_router = create_router("CE A", CUSTOMER_COLOR).scale(0.7)
        site_a_label = Text("Customer Site A", font_size=24).next_to(site_a_router, DOWN, buff=0.2)
        site_a_group = VGroup(site_a_router, site_a_label).shift(LEFT * 4 + DOWN * 1.5)

        # Customer Site B
        site_b_router = create_router("CE B", CUSTOMER_COLOR).scale(0.7)
        site_b_label = Text("Customer Site B", font_size=24).next_to(site_b_router, DOWN, buff=0.2)
        site_b_group = VGroup(site_b_router, site_b_label).shift(RIGHT * 4 + DOWN * 1.5)

        # Provider Cloud
        provider_cloud_shape = Ellipse(width=4.5, height=2.5, color=PROVIDER_COLOR, fill_color=PROVIDER_COLOR, fill_opacity=0.3)
        provider_cloud_label = Text("Service Provider Network (MPLS)", font_size=24).move_to(provider_cloud_shape.get_center())
        provider_cloud_group = VGroup(provider_cloud_shape, provider_cloud_label).shift(UP * 1.0) # Shifted up slightly

        # Position diagram elements relative to text or screen center
        diagram_group = VGroup(site_a_group, site_b_group, provider_cloud_group)
        diagram_group.move_to(ORIGIN).shift(DOWN*0.5 + RIGHT*2) # Adjust position to fit next to text

        # Animations for diagram
        self.play(Create(site_a_group), Create(site_b_group), run_time=1)
        self.play(Create(provider_cloud_group), run_time=1.5)
        self.wait(0.5)

        # Lines connecting sites to the cloud
        line_a_to_cloud = Line(site_a_router.get_top(), provider_cloud_shape.get_left(), color=WHITE, stroke_width=3)
        line_b_to_cloud = Line(site_b_router.get_top(), provider_cloud_shape.get_right(), color=WHITE, stroke_width=3)
        
        self.play(Create(line_a_to_cloud), Create(line_b_to_cloud))
        
        self.wait(3) # Hold the slide

# To run these scenes from the command line (ensure Manim is installed):
# manim -pql l2vpn_intro_scenes.py L2VPNIntroScene1
# manim -pql l2vpn_intro_scenes.py L2VPNIntroScene2
# manim -pql l2vpn_intro_scenes.py L2VPNIntroScene1 L2VPNIntroScene2
# (The -pql flag means preview, quality low. Use -pqm for medium, -pqh for high)
