# Minecraft Modpack Manager (mmm.py)

## What is this?

This is a simple script to manage modpacks for Minecraft. It is designed to be used with any modpack that uses the CurseForge API. Main thing is that it does not create a new instance of Minecraft, but instead installs mods into the existing instance. This means you don't have to lose 5GB of space for mods that you already have stored.

## How do I use it?

1. Put the script in its own folder (it will create data files in the same folder).
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Download the desired modpack from CurseForge and put it in the same folder as `mmm.py`, since relative paths are still broken.
4. (Optional) If you have installed mods before, run `python mmm.py import` to add them to the internal database.
5. Run `python mmm.py use <modpack zip file>`.
6. Hope that your mods are intact, and run Minecraft!

## Planned features

- [ ] Install modpacks from URLs
- [ ] Progress bar for downloads and installs
- [ ] Unused mods cleanup
- [ ] Use a modpack from internal storage if it already is there
- [ ] Add relative modpack paths
