# Codingame Challenge Solutions

My solutions for various Codingame challenges. This repository aims to track my journey and share examples of solutions for learning purposes. It also comes with some tools that you can use in your own journey.

## Using as a Template

You can use this repository as a template for your own Codingame solutions. To do so, click the "Use this template" button at the top of the repository page. This will create a new repository in your account with the same structure as this one. You can then launch the `reset_repository` script to remove all the solutions and reinitialize the directories.

## Structure

The repository is structured as follows:
 * `.cg_local_app` (locally created by `launch_cg_local_app`, contains the CG Local Application)
 * `src`
    * `clash` (empty files for Clash of Code challenges, initialized by `create_clash_files`)
    * `lab` (available space for your experiments)
    * `bot_programming` (solutions for Bot Programming challenges)
    * `codegolf` (solutions for Code Golf challenges)
      * `easy`
      * `medium`
      * `hard`
      * `expert`
    * `optimization` (solutions for Optimization challenges)
    * `puzzles` (solutions for Puzzles)
      * `easy`
      * `medium`
      * `hard`
      * `expert`

## Tools

* **`languages.ini`**: A list of programming languages supported by Codingame. Enable/disable languages as needed.
* **`create_clash_files`**: Creates empty files for Clash of Code.
* **`get_random_language`**: Randomly selects a programming language.
* **`launch_cg_local_app`**: Downloads (if necessary) and launches the latest version of the [CG Local Application](https://github.com/jmerle/cg-local-app) for coding solutions locally.
* **`clean_files`**: Removes `src` files (Clash, Lab, Solutions, or Everything).
* **`init_directories`**: Initializes the `src` directories.
* **`reset_repository`**: Removes all `src` files and initializes the directories.

## Requirements

### General

- **Java Runtime Environment (JRE)**: Required for CG Local Application.
- **[CG Local Extension](https://github.com/jmerle/cg-local-ext)**: Needed for communicating with the CG Local Application.

### Windows

- **PowerShell**: For executing `.ps1` scripts.

### Linux/macOS

- **Bash**: For executing `.sh` scripts.
- **curl**: Needed by `launch_cg_local_app.sh` to fetch the latest app version.
- **jq**: Required by `launch_cg_local_app.sh` for parsing JSON data.

## Usage

* Open your local IDE.
* Launch the CG Local Application with `launch_cg_local_app`.
* Configure it (prefer `Use one file for all puzzles` for Clashs, but not for other Challenges).
* Select a challenge in the Codingame platform.
* Choose a programming language (or let `get_random_language` decide).
* Create a new file in the appropriate directory (or use the `clash` empty file).
* From your browser, on the Codingame IDE, click on your `Enable CG Local` extension button.
* You can now code locally and test/submit your solution in the Codingame platform.

## Known Issues


### Linux

#### `java.awt.HeadlessException: No X11 DISPLAY variable was set, or no headful library support was found, but this program performed an operation which requires it`

  Due to a headless JRE. Uninstall your headless JRE and install a headfull JRE.
  ```sh
  sudo apt remove openjdk-<version>-jre-headless
  sudo apt install openjdk-<version>-jre
  ```

#### `java: symbol lookup error: (...)/libpthread.so.0: undefined symbol: __libc_pthread_init, version GLIBC_PRIVATE`:

  Due to VSCode taking over `GTK_PATH`. Should be fixed by `.vscode/settings.json`. If not you can always unset it manually.
  ```sh
  unset GTK_PATH
  ```

