# MGT-RigBot

## Installation

1. [Download](https://www.blender.org/download/release/Blender4.3/blender-4.3.0-windows-x64.zip/) Blender Version 4.3.0
2. Extract into a dedicated folder for development.
3. Inside this folder, create a subfolder named `config` in the `\4.3` directory to keep this install isolated.
4. Create a Python virtual environment for this Blender installation:

   ```shell
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

5. Configure Blender to use this virtual environment:

   Open Blender > Preferences > File Paths > Python Scripts.
   Set the path to your virtual environment's `site-packages` folder.

### Building the Extension

1. Open the directory containing the add-on code or theme file.
2. Use the [Blender command-line tool](https://docs.blender.org/manual/en/latest/advanced/command_line/extension_arguments.html#command-line-args-extension-build) to build the extension .zip file.

To build the package defined in the current directory use the following commands:

```shell
blender --command extension build
```

To validate the manifest without building the package:

```shell
blender --command extension validate
```

You may also validate a package without having to extract it first.

```shell
blender --command extension validate add-on-package.zip`
```
