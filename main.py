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
                        "FastHTML is a new next-generation web framework for fast, scalable web applications with minimal, compact code. It builds on top of popular foundations like ASGI and HTMX. You can now deploy FastHTML with Vercel CLI or by pushing new changes to your git repository.",
                    ),
                ),
                Button("Cliquez-moi", hx_post="/hello-world", hx_target="#result", cls="btn btn-warning"),
                Div(id="result"),  # Moved outside of Group
                header=(Titled("FastHTML + Vercel + remi")),
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
    return P(f"Hello World! Button clicked at {current_time}")

serve()
