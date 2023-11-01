![icon](https://github.com/digreatbrian/xkivy/blob/main/assets/xkivy.jpg)

# XKivy

A kivy and kivymd extension module for easy accessibility, creation of new widgets and also adding more functionality. 

This module containing new advanced widgets that are readily available to suit your needs.

You may use this module with kivymd module for the best experience.This module was built to incorporate new widgets to kivy and kivymd ,to provide flexibility with widgets ,to add functionality and to fix some problems with kivymd.

## Getting Started

You can get this module to run on your machine through installing it with pip. 

Using Pip

    python -m pip install xkivy
	
 
### Prerequisites

There is only the need of kivy and kivymd for this module to be running. 

```
kivymd >= 1.2.0
kivy >= 2.0.0

```

### Installing

Installing is simple, through downloading the necessary files and then install or through pip. 

Using Pip

```
pip install xkivy

```

Downloading and then installing
Through Git 

```
git clone https://github.com/digreatbrian/xkivy.git
cd xkivy
python setup.py install

```
<b>or</b> 

```
git clone https://github.com/digreatbrian/xkivy.git
cd xkivy
pip install .
```
##
<b>Or Through tar.gz file</b>
```
pip install xkivy-1.0.1.tar.gz

```

## Deployment

To use this module, you just have to do the same procedure when creating a kivy/kivymd App. 

Example
```
    from kivy.app import App
    from xkivy.uix.button import XRectangularButton as XButton

    class TestApp(App):
        def build(self):
            return XButton(text='Test Button') 

    app=TestApp() 
    app.run()
```
## Contributing

Please read [CONTRIBUTING.md](https://github.com/digreatbrian/xkivy/contributors) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Brian Musakwa** - *Initial work* - [digreatbrian](https://github.com/digreatbrian)

See also the list of [contributors](https://github.com/digreatbrian/xkivy/contributors) who participated in this project.

## Widgets
To see the flexible widgets that xkivy has ,please follow [UIX-WIDGETS](https://github.com/digreatbrian/xkivy/blob/main/UIXDocumentation.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/digreatbrian/xkivy/blob/main/LICENSE) file for details

## Acknowledgments

* I hereby thank everyone who has contributed to this software. 










