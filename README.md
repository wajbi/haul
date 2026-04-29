# haul

A lightweight CLI for syncing dotfiles across machines with conflict resolution.

---

## Installation

```bash
pip install haul
```

Or install from source:

```bash
git clone https://github.com/yourname/haul && cd haul && pip install .
```

---

## Usage

Initialize a new haul repository in your home directory:

```bash
haul init
```

Track a dotfile:

```bash
haul add ~/.bashrc
```

List all tracked dotfiles:

```bash
haul list
```

Sync dotfiles to another machine:

```bash
haul sync
```

When conflicts are detected, haul will prompt you to resolve them interactively:

```
Conflict detected: ~/.bashrc
  [l] Keep local   [r] Keep remote   [d] Show diff   [m] Merge
> _
```

Push or pull changes manually:

```bash
haul push
haul pull
```

---

## Configuration

haul reads from `~/.haulrc` for remote repository settings and sync preferences. Run `haul config --help` for available options.

---

## License

MIT © [yourname](https://github.com/yourname)
