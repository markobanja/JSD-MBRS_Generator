
Marko Purić - R2 38/2021
# JSD-MBRS Generator

* DSL language created with **TextX**.
* GUI created with **Python** and **tkinter**.
# Main idea
![image](https://github.com/markobanja/python-DSL/assets/18674783/67c08a85-15e0-48b6-b1f3-86b27882b436)
![image](https://github.com/markobanja/python-DSL/assets/18674783/343f5e5e-d02b-4ad3-a35e-cf3c2d727346)
![image](https://github.com/markobanja/python-DSL/assets/18674783/df294649-3e21-4be2-894c-7c55f589d5ea)

Main idea for this project is to create domain specific language with TextX and Python which will speed up the process of creating and generating code (classes - more specific under [**Functionalities**](#Functionalities)).
User just need to learn syntax (help window will be created inside GUI). Syntax is more human oriented and it will make life easier for developers.

DSL will recognize classes for:
  - Python
  - C#
  - Java

Jinja2 will be used as a template  which will generate codes (classes) for mentioned programming languages.
## What you get with this DSL:
* Automatization
* Time efficiency in coding and deployment
* Less coding syntax errors
* Standardization and consistency
## Visualisation:
* .dot (meta model and model)
* PlantUML (meta model)
# Functionalities:
### With this DSL you will be able to create:
* **Parameters** (for every parameter you will be able to generate get/set methods).

  For every parameters you will be able to generate different **data types** (basic and advanced). For all advanced data types DSL will be able to recognize **imports** too.
* **Constants**
* **Constructors**:
  - Default - where you have all declared parameters.
  - Empty
  - Specific parameters
* **Functions**:
  - Void 
  - Return
      
Logic of the functions should be written manually. It will be prohibited to have same constructors, parameters or functions.
