from fasthtml.common import *
from datetime import datetime


# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app, rt = fast_app(hdrs=(tlink, dlink, picolink), ws_hdr=True)  # Ajout de htmx

@rt("/")
def get():
    return (
        Socials(
            title="Vercel + FastHTML",
            site_name="Vercel",
            description="A demo of Vercel and FastHTML integration",
            image="https://vercel.fyi/fasthtml-og",
            url="https://fasthtml-template.vercel.app",
            twitter_site="@vercel",
        ),
        Container(
            Card(
                Group(
                    P(
                        "Ceci est une démonstration d'intégration en temps réel avec les réseaux sociaux.\n "
                        "À chaque clic sur le bouton ci-dessous, un post sera publié sur mon compte X."
                        "Explorez les possibilités offertes par cette intégration !",
                    ),


                    


                    

                ),
                Br(),
                                
                Button("Cliquez-moi", hx_post="/hello-world", hx_target="#result", cls="btn btn-warning"),

                Br(),

                Br(),

                Div(id="result"),  # Moved outside of Group

                Br(),

                header=(Titled("X-ai-project")),
                footer=(
                    P(
                        A(
                            "Deploy your own",
                            href="https://vercel.com/templates/python/fasthtml-python-boilerplate",
                        ),
                        " or ",
                        A("learn more", href="https://docs.fastht.ml/"),
                        "about FastHTML.",
                    )
                ),

            ),
        ),
    )

@rt("/hello-world", methods=["POST"])
def hello_world():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Button( f"Hello World! Button clicked at {current_time}", cls="btn btn-outline btn-success"),

serve()
