[![Pipeline status on GitLab CI][pipeline-badge]][pipeline-link]

# Graph-based Android Pattern Brute Force
A tool for brute forcing an Android security pattern through TWRP recovery based on a graph-traversal model (credit to https://github.com/psarna).

During a holiday trip my phone did a dive too deep and the screen broke. By the time the screen was fixed I had forgotten what security pattern I had set. But I remembered some parts of my pattern and used Tim's code (timvisee/apbf) and Piotrs help to build a python version of apbf.
I succeeded to crack my 5x5 pattern in about XX.XX hours (at the time of writing it's still running on a small Linux Mint machine...will update if/when successful).

## Requirements
- A pattern lock
- Android 8.0 (Nougat) or above
- [TWRP][twrp] recovery
- [`adb`][adb] (with connectivity to phone in TWRP)
- [`git`][git]
- [`python`][python] `v3.11.4` or higher

## Speed
TWRP recovery enforces a hidden timeout of 10 seconds for each pattern attempt,
all consecutive attempts within that time fail with no warning. Because of this
a brute force attempt will take a long while when the pattern search space is
large.

It is highly recommended to constrain the search space as much as possible if
you partially know the pattern to greatly improve the brute force duration.

In the [`config.json`](./config.json) file you can tweak a few constants for:
- Grid size
- Minimum pattern length
- Maximum pattern length
- Path prefix
- Path suffix
- Nodes to exclude
- Delay between attempts

This tool does brute forcing on the actual device. A brute force attempt could
probably be greatly sped up by performing the attempt locally on a computer,
to work around the timeouts. That's however a lot more work to implement (if
even possible), so it's outside the scope of this project.

## Usage
- Make sure you meet the [requirements](#requirements)
- Clone the repository, and build the project
  ```bash
  # Clone repository
  git clone git@github.com:robsteward/gapbf.git
  cd gapbf
  ```

- Tweak properties in [`config.json`](./config.json):
  ```bash
  # Edit configuration
  code config.json
  ```

  Constrain it as much as possible to reduce pattern search space, which greatly
  improves brute force speed. See [speed](#speed).

- Freshly boot phone into TWRP recovery
- Make sure your phone is connected through ADB
  ```bash
  # Device must be visible in list
  adb devices
  ```

- Start brute forcing
  ```bash
  # Run tool
  python main.py
  ```

- Wait for a successful attempt, this may take a long while
- If the program gets interrupted, check the log file for the last successful attempt
  ```bash
  # Check log file
  cat log.csv
  ```

## To Do
* Test DummyHandler
* Build CountPathHandler
* In ADBHandler read attemptedPaths csv to set and check current path against attemptedPaths and skip if found
* ~~Replace grid with predefined substistued grids (3,4,5,6)~~
* ~~Remove substitue function~~

## License
This project is released under the GNU GPL-3.0 license.
Check out the [LICENSE](LICENSE) file for more information.

[adb]: https://developer.android.com/studio/command-line/adb
[git]: https://git-scm.com/
[twrp]: https://twrp.me/
[pipeline-badge]: https://gitlab.com/timvisee/apbf/badges/master/pipeline.svg
[pipeline-link]: https://gitlab.com/timvisee/apbf/pipelines