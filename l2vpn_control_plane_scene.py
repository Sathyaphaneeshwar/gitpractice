from manim import (
    Scene,
    Text,
    VGroup,
    Line,
    DashedLine,
    Dot,
    Create,
    Write,
    FadeIn,
    FadeOut,
    MoveAlongPath,
    LaggedStart,
    Arrow,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
    BLUE, # For signaling lines
    YELLOW_C, # For highlighting text
    config,
    Ellipse, # For provider cloud
    ShowPassingFlash,
)

# Project specific imports
from l2vpn_elements import (
    create_router,
    PROVIDER_COLOR,
    LABEL_COLOR,
)

# Configure default font size for slides if needed
config.font_size = 32 # Slightly larger default for this conceptual scene

class L2VPNControlPlaneScene(Scene):
    """
    Scene to give a brief overview of the L2 VPN control plane.
    Focuses on the conceptual PE-PE negotiation.
    """
    def construct(self):
        # Title
        title = Text("L2 VPN Control Plane (Simplified)", font_size=44).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Visuals - Routers
        pe1 = create_router("PE1", PROVIDER_COLOR).scale(1.1)
        pe2 = create_router("PE2", PROVIDER_COLOR).scale(1.1)
        
        # Position PE routers
        pe1.move_to(LEFT * 3.5 + UP * 0.5)
        pe2.move_to(RIGHT * 3.5 + UP * 0.5)

        # Optional Provider Core (dimmed cloud)
        provider_core_cloud = Ellipse(width=4.5, height=2.0, color=PROVIDER_COLOR, fill_opacity=0.1)
        provider_core_cloud.move_to(ORIGIN + UP * 0.5)
        provider_core_label = Text("Provider Core", font_size=20, color=PROVIDER_COLOR).move_to(provider_core_cloud.get_center())
        core_group = VGroup(provider_core_cloud, provider_core_label).set_opacity(0.5)


        self.play(
            LaggedStart(
                Create(pe1),
                Create(pe2),
                FadeIn(core_group),
                lag_ratio=0.4
            )
        )
        self.wait(0.5)

        # Explanatory Text (Part 1)
        text_intro_1 = Text(
            "Before data can flow, Provider Edge (PE) routers must exchange information.",
            font_size=28
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(text_intro_1))
        self.wait(0.5)

        text_intro_2 = Text(
            "This is done via a Control Plane protocol (e.g., LDP, BGP).",
            font_size=28
        ).next_to(text_intro_1, DOWN, buff=0.3)
        self.play(Write(text_intro_2))
        self.wait(1)

        # Visuals - Signaling
        # Dashed lines with moving dots to represent messages
        signaling_path_1 = DashedLine(pe1.get_right(), pe2.get_left(), color=BLUE, stroke_width=3, dash_length=0.2)
        signaling_path_2 = DashedLine(pe2.get_left(), pe1.get_right(), color=BLUE, stroke_width=3, dash_length=0.2).shift(UP*0.1) # Slightly offset

        message_dot_1 = Dot(color=YELLOW_C, radius=0.08)
        message_dot_2 = Dot(color=YELLOW_C, radius=0.08)

        self.play(Create(signaling_path_1), Create(signaling_path_2))
        self.play(
            MoveAlongPath(message_dot_1, signaling_path_1),
            run_time=1.5
        )
        self.play(
            MoveAlongPath(message_dot_2, signaling_path_2.reverse_direction()), # Move from PE2 to PE1
            run_time=1.5
        )
        self.play(FadeOut(message_dot_1), FadeOut(message_dot_2))
        self.wait(0.5)
        
        # Could also use ShowPassingFlash on the lines or routers
        self.play(
            ShowPassingFlash(signaling_path_1.copy().set_color(YELLOW_C), time_width=0.5, run_time=1),
            ShowPassingFlash(signaling_path_2.copy().set_color(YELLOW_C), time_width=0.5, run_time=1),
        )
        self.wait(0.5)


        # Explanatory Text (Part 2)
        text_agreement_intro = Text("They agree on:", font_size=28).next_to(text_intro_2, DOWN, buff=0.7)
        text_agreement_intro.align_to(text_intro_1, LEFT)
        self.play(Write(text_agreement_intro))
        self.wait(0.3)

        bullet_points_text = [
            "VC Labels (to identify the L2 VPN).",
            "How to reach each other (establishing the MPLS tunnel).",
        ]
        
        bullets = VGroup()
        for i, point_text in enumerate(bullet_points_text):
            dot = Dot(radius=0.05, color=LABEL_COLOR).next_to(ORIGIN, LEFT, buff=0) # Small dot for bullet
            text = Text(point_text, font_size=26).next_to(dot, RIGHT, buff=0.2)
            bullet_item = VGroup(dot, text)
            bullets.add(bullet_item)
        
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(text_agreement_intro, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(LaggedStart(*[FadeIn(bullet, shift=RIGHT*0.3) for bullet in bullets], lag_ratio=0.5))
        self.wait(1)

        # Final Text
        text_pseudowire = Text(
            "This sets up the 'pseudowire' or L2 VPN tunnel.",
            font_size=28, color=YELLOW_C
        ).next_to(bullets, DOWN, buff=0.5)
        self.play(Write(text_pseudowire))
        
        # Highlight the tunnel/signaling path again
        tunnel_highlight = VGroup(signaling_path_1, signaling_path_2).copy()
        self.play(tunnel_highlight.animate.set_stroke(width=5, color=GREEN_C))
        self.play(Indicate(tunnel_highlight, color=GREEN_C, scale_factor=1.1))

        self.wait(3)

# To run this scene:
# manim -pql l2vpn_control_plane_scene.py L2VPNControlPlaneScene
# Use -pqm for medium quality, -pqh for high quality.
