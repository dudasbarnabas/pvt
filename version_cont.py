import json
import tkinter as tk
import webbrowser
from tkinter import messagebox
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CURRENT_VERSION = "1.0.4"
GITHUB_OWNER = "dudasbarnabas"
GITHUB_REPO = "pvt"


def parse_version(version: str) -> tuple[int, ...]:
    """
    A 'v1.2.3' vagy '1.2.3' formátumot számsorrá alakítja.
    Ez az egyszerű MWE normál verziószámokra készült.
    """
    clean_version = version.strip().lower().removeprefix("v")
    return tuple(int(part) for part in clean_version.split("."))


def get_latest_release() -> dict:
    api_url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    )

    request = Request(
        api_url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{GITHUB_REPO}-update-checker",
        },
    )

    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def check_for_updates() -> None:
    try:
        release = get_latest_release()

        latest_tag = release["tag_name"]
        latest_version = latest_tag.removeprefix("v")
        release_url = release["html_url"]

        if parse_version(latest_version) > parse_version(CURRENT_VERSION):
            open_release = messagebox.askyesno(
                title="Frissítés érhető el",
                message=(
                    f"Új verzió érhető el!\n\n"
                    f"Jelenlegi verzió: {CURRENT_VERSION}\n"
                    f"Legújabb verzió: {latest_version}\n\n"
                    f"Megnyissam a letöltési oldalt?"
                ),
            )

            if open_release:
                webbrowser.open(release_url)

        else:
            # pass
            messagebox.showinfo(
                title="Nincs frissítés",
                message=(
                    f"A program naprakész.\n\n"
                    f"Jelenlegi verzió: {CURRENT_VERSION}\n"
                    f"GitHub-verzió: {latest_version}"
                ),
            )

    except HTTPError as error:
        if error.code == 404:
            message = (
                "Nem található kiadott GitHub Release."
            )
        else:
            message = f"GitHub HTTP-hiba: {error.code}"

        messagebox.showerror("Frissítésellenőrzési hiba", message)

    except URLError as error:
        messagebox.showerror(
            "Kapcsolati hiba",
            f"Nem sikerült kapcsolódni a GitHubhoz.\n\n{error.reason}",
        )

    except (KeyError, ValueError, TypeError) as error:
        messagebox.showerror(
            "Adathiba",
            f"Nem sikerült értelmezni a GitHub válaszát.\n\n{error}",
        )


def main() -> None:
    root = tk.Tk()
    root.withdraw()

    check_for_updates()

    root.destroy()


if __name__ == "__main__":
    main()