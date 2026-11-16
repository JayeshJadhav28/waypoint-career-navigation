from dotenv import load_dotenv
from groq import Groq
from career_advisor import get_career_advice
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import os


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:

    console.print(
        Panel(
            "[bold red]❌ GROQ_API_KEY is missing.[/bold red]\n\n"
            "Please add your Groq API key to the .env file.",
            box=box.ROUNDED
        )
    )

    raise SystemExit

client = Groq(api_key=api_key)

console = Console()


console.print(
    Panel(
        "[bold cyan]🤖 AI CAREER ADVISOR[/bold cyan]\n"
        "[dim]Personalized career guidance powered by AI[/dim]",
        box=box.ROUNDED
    )
)


console.print(
    "\n[bold yellow]Tell me about yourself:[/bold yellow]"
)

console.print(
    "[dim]Include your education, skills, interests, "
    "experience and career goal.[/dim]\n"
)

user_profile = console.input("[bold green]> [/bold green]")


try:

    with console.status(
        "[bold cyan]Analyzing your profile...[/bold cyan]"
    ):

        career_advice = get_career_advice(
            client,
            user_profile
        )

except ValueError as e:

    console.print(
        Panel(
            f"[bold red]❌ Error[/bold red]\n\n{e}",
            box=box.ROUNDED
        )
    )

    raise SystemExit

except RuntimeError as e:

    console.print(
        Panel(
            f"[bold red]❌ Service Error[/bold red]\n\n{e}",
            box=box.ROUNDED
        )
    )

    raise SystemExit


# Career Recommendations

console.print(
    "\n[bold cyan]🎯 CAREER RECOMMENDATIONS[/bold cyan]\n"
)

career_table = Table(
    box=box.ROUNDED,
    show_header=True
)

career_table.add_column(
    "Career",
    style="bold"
)

career_table.add_column(
    "Suitability",
    justify="center"
)

career_table.add_column(
    "Why It Fits"
)

for recommendation in career_advice.recommended_careers:

    career_table.add_row(
        recommendation.career,
        f"{recommendation.suitability_score}/100",
        recommendation.reason
    )

console.print(career_table)


# Skills

console.print(
    "\n[bold cyan]🧠 SKILLS TO LEARN[/bold cyan]"
)

for skill in career_advice.skills_to_learn:

    console.print(
        f"  [green]•[/green] {skill}"
    )


# Certifications

console.print(
    "\n[bold cyan]📜 RECOMMENDED CERTIFICATIONS[/bold cyan]"
)

for certification in career_advice.recommended_certifications:

    console.print(
        f"  [green]•[/green] {certification}"
    )


# Learning Resources

console.print(
    "\n[bold cyan]📚 LEARNING RESOURCES[/bold cyan]\n"
)

resource_table = Table(
    box=box.ROUNDED
)

resource_table.add_column(
    "Resource",
    style="bold"
)

resource_table.add_column(
    "Type"
)

for resource in career_advice.learning_resources:

    resource_table.add_row(
        resource.resource,
        resource.type
    )

console.print(resource_table)


# Roadmap

console.print(
    "\n[bold cyan]🗺️ LEARNING ROADMAP[/bold cyan]\n"
)

roadmap_table = Table(
    box=box.ROUNDED
)

roadmap_table.add_column(
    "Step",
    style="bold"
)

roadmap_table.add_column(
    "Time Required"
)

for step in career_advice.roadmap:

    roadmap_table.add_row(
        step.step,
        step.time_required
    )

console.print(roadmap_table)


# Transition Time

console.print(
    Panel(
        f"[bold]Estimated Transition Time:[/bold] "
        f"[green]{career_advice.estimated_transition_time}[/green]",
        box=box.ROUNDED
    )
)