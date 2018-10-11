# Kiko

Kiko stands for Keys-In-Keys-Out. It was designed specifically to handle animation curves data in a pipeline-friendly way, but it can do much more.
With Kiko you can define operators that can handle different kind of data per item or channel and can work automatically across different DCCs.

Currently Autodesk Maya and The Foundry Nuke are supported. 

Kiko was designed and implemented by Toolchefs LTD. We have decided to contribute to the 3D Industry making it open source.

Kiko is written completely in python.

### Current status of the project

Kiko has already been used on Maya 2016 onwards and on Nuke 11. 
We are looking for contributors who could help us making it work on others DCCs (i.e. Modo, Houdini) and writing new operators.

Few things are missing, like UIs for Nuke, cross app tests, etc.

Please note, every DCC handles animation curves differently, for this reason transferring animation curves between different apps might not always re-create similar curves.

## Getting started

### Installing
Installing in Maya is quite easy.
```
- copy the kiko/python/kiko folder in your maya scripts folder.
- copy the the kikoUndoer.py file in your maya plug-ins folder.
- you can launch the maya importer and exporter UIs by running the code under kiko/extras/maya.
```

## Running the tests
We use nose for our unit tests. Currently we support windows, osx and linux.
Your MAYA_PLUG_IN_PATH and proper python paths must be set for the unit tests to succeed.

Once you environment is set up, you can run the run_win.py, run_osx.py or run_linux.py files inside the kiko/unittests folder. Please note, you might have to edit these files to point to your maya and nuke executables, you might also need to edit your PYTHONPATH to include all relevant paths.

## Documentation
If you are a developer and would like to know more, please read the [wiki](https://github.com/danielefederico/kiko/wiki) and write to us at support@toolchefs.com in case you have any question.

The base classes are documented, but comments for inherited classes are not provided.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under [the LPGP license](http://www.gnu.org/licenses/).

## Contact us

Please feel free to contact us at support@toolchefs.com in case you would like contribute or simply have questions.

The rig used in the unit tests is courtesy of Alex Puente.

### ENJOY!





