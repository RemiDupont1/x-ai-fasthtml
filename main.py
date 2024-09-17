from fasthtml.common import *
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import main_X

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app, rt = fast_app(hdrs=(tlink, dlink, picolink), ws_hdr=True)  # Ajout de htmx

# Start timing
start_time = time.time()

# Database setup
DATABASE_URL = os.environ.get("POSTGRES_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Click(Base):
    __tablename__ = 'clicks'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


# End timing
first_time = True


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

                # Replace the direct click_list with a loading indicator and a div for the clicks
                Div(
                    Div(cls="loading loading-spinner loading-lg"),
                    id="clicks-container",
                    hx_get="/load-clicks",
                    hx_trigger="load",
                ),

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
                    ),
                    H3("Click History:"),
                    #click_list
                    
                ),

            ),
        ),
    )


# Add a new route to load clicks
@rt("/load-clicks")
def load_clicks():
    global first_time
    if first_time:
        Base.metadata.create_all(engine)
        first_time = False

    clicks = get_all_clicks()
    click_list = Ul(*[Li(f"Click at {click.timestamp}") for click in clicks])
    return click_list

@rt("/hello-world", methods=["POST"])
def hello_world():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to database
    # session = Session()
    # new_click = Click()
    # session.add(new_click)
    # session.commit()
    # session.close()
    main_X.main()
    
    return Button(f"Hello World! Button clicked at {current_time}", cls="btn btn-outline btn-success")

def get_all_clicks():
    session = Session()
    clicks = session.query(Click).all()
    session.close()
    return clicks

serve()
